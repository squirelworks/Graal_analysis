"""In-process models of recovered Graal trainer loops.

Each table is the key, the count, and the wait read from the sample.
``replay`` walks a table and records the sequence. It does not open a
socket, call a window API, or start another program.

See ``behaviour-models.md`` for which samples these tables come from.
"""

from __future__ import annotations

import unittest


# AutoIdle, one pass, then the script goes back to the start. No sleep.
AUTOIDLE_KEYS = (
    "LEFT", "RIGHT", "LEFT", "RIGHT", "LEFT", "RIGHT", "LEFT", "RIGHT",
    "LEFT", "RIGHT", "LEFT", "RIGHT", "LEFT", "RIGHT", "RIGHT", "RIGHT",
    "LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT",
    "LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT",
    "LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT",
    "LEFT", "LEFT", "LEFT", "RIGHT",
    "LEFT", "RIGHT", "LEFT", "RIGHT", "LEFT", "RIGHT",
    "LEFT", "RIGHT", "LEFT", "RIGHT",
)

# Random walker: roll 0 sends nothing. Rolls 1..5 send that key five times.
WALKER_ROLL = {
    0: None,
    1: "UP",
    2: "DOWN",
    3: "LEFT",
    4: "RIGHT",
    5: "S",
}

AFK_PHRASES = (
    "I am AFK",
    "I am using an AFK Bot",
    "AFK Bot created by Zorg",
)

# The text file shipped beside Graal Load. One line is one send.
BOMB_LINES = (
    'setshield no-shield.gif',
    'sethead slhead535.gif',
    'setbody body5.png',
    'setnick Bomb',
    'setcoat darkred',
    'setbelt red',
    'setskin darkred',
    'setsleeves red',
    'setshoes brown',
    'Y',
    'Yo',
    'You',
    'You a',
    'You ar',
    'You are',
    'You are g',
    'You are go',
    'You are goi',
    'You are goin',
    'You are going',
    'You are going t',
    'You are going to',
    'You are going to d',
    'You are going to di',
    'You are going to die',
    'You are going to die i',
    'You are going to die in',
    'You are going to die in .',
    'You are going to die in ..',
    'You are going to die in ...',
    'You are going to die in ...',
    'You are going to die in ...',
    'You are going to die in ...',
    '100',
    '99',
    '98',
    '97',
    '96',
    '95',
    '94',
    '93',
    '92',
    '91',
    '90',
    '89',
    '88',
    '87',
    '86',
    '85',
    '84',
    '83',
    '82',
    '81',
    '80',
    '79',
    '78',
    '77',
    '76',
    '75',
    '74',
    '73',
    '72',
    '71',
    '70',
    '69',
    '68',
    '67',
    '66',
    '65',
    '64',
    '63',
    '62',
    '61',
    '60',
    '59',
    '58',
    '57',
    '56',
    '55',
    '54',
    '53',
    '52',
    '51',
    '50',
    '49',
    '48',
    '47',
    '46',
    '45',
    '44',
    '43',
    '42',
    '41',
    '40',
    '39',
    '38',
    '37',
    '36',
    '35',
    '34',
    '33',
    '32',
    '31',
    '30',
    '29',
    '28',
    '27',
    '26',
    '25',
    '24',
    '23',
    '22',
    '21',
    '20',
    '19',
    '18',
    '17',
    '16',
    '15',
    '14',
    '13',
    '12',
    '11',
    '10',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
    '1',
    '0',
    '.0.',
    '..0..',
    '...0...',
    '..BOOM..',
    '.!BOOM!.',
    '!!BOOM!!',
    'setcoat red',
    'setbelt orange',
    'setskin red',
    'setsleeves orange',
    'setshoes dakred',
    'setcoat orange',
    'setbelt yellow',
    'setskin orange',
    'setsleeves yellow',
    'setshoes red',
    'setcoat red',
    'setbelt orange',
    'setskin red',
    'setsleeves orange',
    'setshoes dakred',
    'setcoat black',
    'setbelt brown',
    'setskin black',
    'setsleeves brown',
    'setshoesshoes black',
    '!! oo !!',
    '!!  !!',
    '!!!!',
    '!!',
)


def expand_send(key, count, gap_ms):
    """One Send of ``count`` taps, with ``gap_ms`` between taps."""
    events = []
    for i in range(count):
        events.append(("key", key))
        if gap_ms and i + 1 < count:
            events.append(("sleep", gap_ms))
    return events


def autod(cycles):
    """Sleep 1 ms, send ``d``, forever."""
    events = []
    for _ in range(cycles):
        events.append(("sleep", 1))
        events.extend(expand_send("d", 1, 0))
    return events


def autos(cycles):
    """Send ``s#`` with no script-level sleep."""
    events = []
    for _ in range(cycles):
        events.extend(expand_send("s#", 1, 0))
    return events


def autoidle(cycles):
    events = []
    for _ in range(cycles):
        for key in AUTOIDLE_KEYS:
            events.extend(expand_send(key, 1, 0))
    return events


def autokey():
    """Rename the active window. Sends no game key."""
    return [("sleep", 2000), ("rename", "Graal Auto")]


def water_v11(cycles):
    """Down twice (300 ms between), then ``a``, then sleep 2000 ms."""
    events = []
    for _ in range(cycles):
        events.extend(expand_send("DOWN", 2, 300))
        events.extend(expand_send("a", 1, 300))
        events.append(("sleep", 2000))
    return events


def water_v10(cycles, direction1="LEFT", direction2="RIGHT", active=True):
    """v1.0 water loop. Sends nothing while ``Graal Auto`` is not active."""
    if not active:
        return [("sleep", 1000)]
    events = []
    for _ in range(cycles):
        for _s in range(19):
            events.extend(expand_send("S", 1, 100))
            events.append(("sleep", 1000))
        events.append(("sleep", 2000))
        events.extend(expand_send(direction1, 2, 50))
        events.append(("sleep", 500))
        events.extend(expand_send(direction2, 2, 50))
        events.append(("sleep", 500))
    return events


def random_walker(rolls, active=True):
    """One decision per roll. Inactive window: wait 1000 ms, no keys."""
    events = []
    for roll in rolls:
        if not active:
            events.append(("sleep", 1000))
            continue
        key = WALKER_ROLL[roll]
        if key is not None:
            events.extend(expand_send(key, 5, 200))
    return events


def prayer_helper():
    """The ``data`` helper: Up ten times, 100 ms between taps, then it exits."""
    return expand_send("UP", 10, 100)


def prayer(cycles, weapon="R", naginata="E", direction="LEFT", active=True):
    """One Prayer pass. The helper's Up taps are included where it is started."""
    if not active:
        return [("sleep", 1000)]
    events = []
    for _ in range(cycles):
        events.extend(expand_send("TAB", 1, 100))
        for _use in range(3):
            events.append(("text", "/use_skill praying"))
            events.append(("return", None))
            events.append(("sleep", 2000))
        events.append(("sleep", 500))
        events.extend(expand_send("TAB", 1, 100))
        events.append(("sleep", 500))
        events.extend(expand_send(naginata, 1, 100))
        events.append(("sleep", 1000))
        events.extend(prayer_helper())
        events.extend(expand_send(direction, 1, 0))
        events.extend(expand_send("s", 10, 100))
        events.append(("sleep", 500))
        events.extend(expand_send(weapon, 1, 100))
        events.append(("sleep", 500))
        events.extend(expand_send("RIGHT", 1, 100))
        events.append(("sleep", 500))
        events.extend(expand_send(direction, 2, 100))
        events.append(("sleep", 1000))
    return events


def afk_bot(cycles, phrases=AFK_PHRASES):
    """One phrase every 3000 ms, cycling the list."""
    events = []
    for i in range(cycles):
        events.append(("sleep", 3000))
        events.append(("text", phrases[i % len(phrases)]))
        events.append(("return", None))
    return events


def graal_load(lines):
    """Each line is written, Return is pressed down, then 150 ms."""
    events = []
    for line in lines:
        events.append(("text", line))
        events.append(("return", None))
        events.append(("sleep", 150))
    return events


def keys_of(events):
    return [value for kind, value in events if kind == "key"]


def texts_of(events):
    return [value for kind, value in events if kind == "text"]


def sleep_total(events):
    return sum(value for kind, value in events if kind == "sleep")


class ReplayTests(unittest.TestCase):
    def test_autod_is_one_millisecond_between_digs(self):
        events = autod(4)
        self.assertEqual(keys_of(events), ["d", "d", "d", "d"])
        self.assertEqual(sleep_total(events), 4)
        self.assertEqual(events[0], ("sleep", 1))
        self.assertEqual(events[1], ("key", "d"))

    def test_autos_has_no_script_sleep(self):
        events = autos(3)
        self.assertEqual(keys_of(events), ["s#", "s#", "s#"])
        self.assertEqual(sleep_total(events), 0)

    def test_autoidle_pass_is_48_arrows_and_no_sleep(self):
        events = autoidle(1)
        self.assertEqual(len(AUTOIDLE_KEYS), 48)
        self.assertEqual(keys_of(events), list(AUTOIDLE_KEYS))
        self.assertEqual(sleep_total(events), 0)
        self.assertEqual(keys_of(autoidle(2))[:48], list(AUTOIDLE_KEYS))

    def test_autokey_renames_and_sends_nothing(self):
        events = autokey()
        self.assertEqual(keys_of(events), [])
        self.assertEqual(events, [("sleep", 2000), ("rename", "Graal Auto")])

    def test_water_v11_faces_down_then_uses(self):
        events = water_v11(1)
        self.assertEqual(
            events,
            [
                ("key", "DOWN"),
                ("sleep", 300),
                ("key", "DOWN"),
                ("key", "a"),
                ("sleep", 2000),
            ],
        )

    def test_water_v10_nineteen_uses_then_a_wiggle(self):
        events = water_v10(1, direction1="LEFT", direction2="RIGHT", active=True)
        self.assertEqual(keys_of(events).count("S"), 19)
        self.assertEqual(keys_of(events)[-4:], ["LEFT", "LEFT", "RIGHT", "RIGHT"])
        self.assertEqual(water_v10(3, active=False), [("sleep", 1000)])

    def test_walker_roll_table(self):
        events = random_walker([0, 1, 5], active=True)
        self.assertEqual(keys_of(events), ["UP"] * 5 + ["S"] * 5)
        self.assertEqual(events[0], ("key", "UP"))
        self.assertEqual(events[1], ("sleep", 200))
        self.assertEqual(random_walker([1, 2], active=False), [("sleep", 1000), ("sleep", 1000)])
        self.assertEqual(WALKER_ROLL[4], "RIGHT")

    def test_prayer_pass_and_helper(self):
        events = prayer(1, weapon="R", naginata="E", direction="LEFT", active=True)
        self.assertEqual(texts_of(events), ["/use_skill praying"] * 3)
        self.assertEqual(keys_of(events).count("UP"), 10)
        self.assertEqual(keys_of(events).count("s"), 10)
        self.assertEqual(keys_of(events).count("E"), 1)
        self.assertEqual(keys_of(events).count("R"), 1)
        self.assertIn(("return", None), events)
        self.assertEqual(prayer(2, active=False), [("sleep", 1000)])

    def test_afk_cycles_three_phrases(self):
        events = afk_bot(4)
        self.assertEqual(
            texts_of(events),
            [
                "I am AFK",
                "I am using an AFK Bot",
                "AFK Bot created by Zorg",
                "I am AFK",
            ],
        )
        self.assertEqual(sleep_total(events), 12000)
        self.assertEqual(events[0], ("sleep", 3000))

    def test_graal_load_writes_each_line_then_waits(self):
        self.assertEqual(len(BOMB_LINES), 164)
        self.assertEqual(BOMB_LINES[3], "setnick Bomb")
        self.assertEqual(BOMB_LINES[33], "100")
        self.assertEqual(BOMB_LINES[139], "!!BOOM!!")
        events = graal_load(BOMB_LINES[:2])
        self.assertEqual(
            events,
            [
                ("text", "setshield no-shield.gif"),
                ("return", None),
                ("sleep", 150),
                ("text", "sethead slhead535.gif"),
                ("return", None),
                ("sleep", 150),
            ],
        )
        self.assertEqual(sleep_total(graal_load(BOMB_LINES)), 164 * 150)


if __name__ == "__main__":
    unittest.main()
