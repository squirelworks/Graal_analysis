"""Tests for gs1lint. Run: python -m pytest tools/gs1-lint -q"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gs1lint  # noqa: E402

TABLE = gs1lint.load_table()
REPO = Path(__file__).resolve().parents[2]


def errors(src):
    return [f for f in gs1lint.lint_text(src, table=TABLE) if f.level == 'error']


def warnings(src):
    return [f for f in gs1lint.lint_text(src, table=TABLE) if f.level == 'warning']


class TableFromManual(unittest.TestCase):
    def test_161_commands(self):
        self.assertEqual(len(TABLE.commands), 161)

    def test_known_signatures(self):
        self.assertEqual(TABLE.commands['setlevel2'], ('MRR',))
        self.assertEqual(TABLE.commands['hide'], ('',))
        self.assertEqual(TABLE.commands['showimg'], ('RMRR', 'RFRR'))

    def test_lists(self):
        self.assertIn('setfocus', TABLE.ignored)
        self.assertIn('showtext', TABLE.later_only)
        self.assertIn('random', TABLE.functions)
        self.assertIn('glove2', TABLE.names['I'])
        self.assertIn('lizardon', TABLE.names['B'])


class GoodScripts(unittest.TestCase):
    def test_event_skeleton(self):
        src = '''
        // a sign
        if (playerenters) { setimg sign.png; dontblock; }
        if (playertouchsme && playerdir == 0) {
          say2 Welcome to the#bsquare;
        }
        '''
        self.assertEqual(errors(src), [])

    def test_loops_functions_timer(self):
        src = '''
        function step() {
          this.n++;
          for (this.i = 0; this.i < 4; this.i++) { x += 0.5; }
          if (onwall(x + 1, y)) return;
        }
        if (playerenters) { this.n = 0; timeout = 0.05; }
        if (timeout) { step(); timeout = 0.05; }
        '''
        self.assertEqual(errors(src), [])
        self.assertEqual(warnings(src), [])

    def test_strings_and_codes(self):
        src = '''
        if (playerchats && strequals(#c, buy)) {
          setstring this.last,#c;
          message You said #s(this.last), #v(playerrupees) left;
          setcharani idle,;
        }
        if (this.mode in {1,2,3} && x in |0,64|) { lay2 greenrupee,x,y+2; }
        '''
        self.assertEqual(errors(src), [])

    def test_disputed_signature_either_reading(self):
        self.assertEqual(errors('if (created) { showimg 1,@title,10,10; }'), [])


class BadScripts(unittest.TestCase):
    def test_unknown_command(self):
        self.assertTrue(errors('if (created) { warp level.graal,30,30; }'))

    def test_later_only_command(self):
        msg = errors('if (created) { showtext 1,1,1,Arial,,hi; }')[0].msg
        self.assertIn('2.22', msg)

    def test_ignored_command(self):
        msg = errors('if (created) { setfocus 10,10; }')[0].msg
        self.assertIn('ignored', msg)

    def test_arg_count(self):
        self.assertTrue(errors('if (playertouchsme) { setlevel2 a.graal,30; }'))
        self.assertTrue(errors('if (playertouchsme) { hide 1; }'))

    def test_bad_name_argument(self):
        self.assertTrue(errors('if (created) { lay2 bluediamond,x,y; }'))
        self.assertTrue(errors('if (created) { putcomp dragonfly,10,10; }'))

    def test_unbalanced(self):
        self.assertTrue(errors('if (created) { hide;'))
        self.assertTrue(errors('if (created { hide; }'))

    def test_missing_semicolon(self):
        self.assertTrue(errors('if (created) { hide }'))

    def test_unknown_expression_function(self):
        self.assertTrue(errors('if (distance(x,y) < 2) { hide; }'))

    def test_undefined_user_function(self):
        self.assertTrue(errors('if (created) { reward(); }'))

    def test_timeout_without_timer(self):
        self.assertTrue(warnings('if (timeout) { hide; }'))


class Library(unittest.TestCase):
    """Every script in the original NPC library must lint clean."""

    def test_library_scripts(self):
        root = REPO / 'npc-library' / 'scripts'
        files = sorted(root.rglob('*.gs1')) if root.is_dir() else []
        bad = []
        for f in files:
            bad += [str(x) for x in gs1lint.lint_text(f.read_text(encoding='utf-8'), str(f.relative_to(REPO)), TABLE)]
        self.assertEqual(bad, [])


if __name__ == '__main__':
    unittest.main()
