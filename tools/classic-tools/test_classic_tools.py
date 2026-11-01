"""In-process checks for the classic-tool references. No sockets."""

import socket
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from account13 import decode_account, decode_props, encode_account, encode_props, page_row, select_page
from chrfile import parse_chr
from listframe import (
    client_lines, gserver_login_line, pack_frame, parse_client_line,
    parse_gserver_login, unpack_frames,
)


class NoSocket(unittest.TestCase):
    def test_modules_do_not_bind(self):
        for name in ('listframe', 'account13', 'chrfile'):
            module = sys.modules[name]
            self.assertFalse(hasattr(module, 'socket'))
            self.assertNotIn('socket', module.__dict__)
        # Importing socket here is the test, not the reference.
        self.assertTrue(callable(socket.socket))


class ListFrame(unittest.TestCase):
    def test_client_login_round_trip(self):
        lines = client_lines(b'classic', b'ada', b'secret')
        raw = pack_frame(lines)
        parsed = [parse_client_line(line) for line in unpack_frames(raw)]
        self.assertEqual(parsed[0], {'id': 0, 'edition': b'classic'})
        self.assertEqual(parsed[1]['id'], 1)
        self.assertEqual(parsed[1]['account'], b'ada')
        self.assertEqual(parsed[1]['password'], b'secret')

    def test_two_frames(self):
        first = pack_frame(client_lines(b'a', b'n', b'p'))
        second = pack_frame([gserver_login_line(0, b'GLSER001', b'world')])
        lines = list(unpack_frames(first + second))
        self.assertEqual(len(lines), 3)
        login = parse_gserver_login(lines[2])
        self.assertEqual(login['kind'], 0)
        self.assertEqual(login['token'], b'GLSER001')
        self.assertEqual(login['world'], b'world')

    def test_gserver_kind_and_token(self):
        raw = gserver_login_line(1, b'GLSER002', b'other')
        self.assertEqual(parse_gserver_login(raw)['kind'], 1)
        with self.assertRaises(ValueError):
            gserver_login_line(2, b'GLSER001', b'world')
        with self.assertRaises(ValueError):
            parse_gserver_login(bytes([32]) + b'NOTATOKN' + b'world')


class AccountFile(unittest.TestCase):
    def test_round_trip_and_hidden_password(self):
        props = encode_props(nickname='Ada', rupees=12, kills=4, deaths=1,
                             onlinesecs=90, maxpower=3, alignment=7)
        blob = encode_account(
            'ada', 'secret', props, weapons=[b'sword'],
            action_flags=['been.north'], opened_chests=['chest.one'],
        )
        account = decode_account(blob)
        self.assertEqual(account['name'], b'ada')
        self.assertEqual(account['password'], b'secret')
        self.assertEqual(account['weapons'], [b'sword'])
        self.assertEqual(decode_props(account['proplist'])['kills'], 4)
        row = page_row(account)
        self.assertEqual(row['nickname'], 'Ada')
        self.assertNotIn('password', row)
        self.assertNotIn(b'secret', str(row).encode('latin1'))

    def test_page_skips_onlyload_and_super_and_caps_at_fifty(self):
        accounts = []
        for i in range(60):
            props = encode_props(nickname='n%d' % i, kills=i)
            accounts.append(encode_account('p%d' % i, 'x', props))
        accounts.append(encode_account('super', 'x', encode_props(nickname='nope', kills=1000)))
        accounts.append(encode_account('quiet', 'x', encode_props(nickname='skip', kills=999),
                                       onlyload=True))
        decoded = [decode_account(blob) for blob in accounts]
        page = select_page(decoded, 'kills')
        self.assertEqual(len(page), 50)
        self.assertEqual(page[0]['kills'], 59)
        self.assertEqual(page[0]['place'], 1)
        names = [row['nickname'] for row in page]
        self.assertNotIn('nope', names)
        self.assertNotIn('skip', names)
        blank = decode_account(encode_account('blank', 'x', encode_props(nickname='', kills=3)))
        self.assertEqual(page_row(blank)['nickname'], '')


class ChrLine(unittest.TestCase):
    def test_sample_shape(self):
        parsed = parse_chr('CHR:1.00Blade=head189.gif,male,black,black,gray,gray,red\n')
        self.assertEqual(parsed['name'], 'Blade')
        self.assertEqual(parsed['head'], 'head189.gif')
        self.assertEqual(parsed['sex'], 'male')
        self.assertEqual(parsed['colours'], ['black', 'black', 'gray', 'gray', 'red'])

    def test_female_and_reject(self):
        parsed = parse_chr('CHR:1.00Anna=head225.gif,female,orange,white,white,darkred,red')
        self.assertEqual(parsed['sex'], 'female')
        with self.assertRaises(ValueError):
            parse_chr('CHR:1.00Nope=head1.gif,other,black,black,black,black,black')
        with self.assertRaises(ValueError):
            parse_chr('not a character')


if __name__ == '__main__':
    unittest.main()
