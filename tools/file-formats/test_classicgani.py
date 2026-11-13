import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classicgani import decode, encode, file_key

# First block of Classic 1.8's offline idle.gani and the matching 1.7 plain text.
IDLE_BLOCK0 = bytes.fromhex('2b40909017ffea2d')


def test_known_plaintext_block():
    assert decode('idle.gani', IDLE_BLOCK0) == b'SPRITE  '
    assert encode('idle.gani', b'SPRITE  ') == IDLE_BLOCK0


def test_key_uses_lower_case_base_name():
    assert file_key('levels/ganis/IDLE.GANI') == file_key('idle.gani')
    assert file_key('idle.gani') != file_key('walk.gani')


def test_tail_kept_and_round_trip():
    data = b'GANI0001\r\nSPRITE 0 SPRITES 0 0 24 16 shadow\r\n'
    enc = encode('emoticon.gani', data)
    assert len(enc) == len(data)
    assert enc[len(data) & ~7:] == data[len(data) & ~7:]
    assert decode('emoticon.gani', enc) == data
