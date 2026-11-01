"""Account files read by the 1999 `gserverstat` tools.

The on-disk layout is the one `SaveAccount` writes for `accounts/accN.txt`:
a length-prefixed account name, a length-prefixed password, a length-prefixed
property list, a flag byte, two unused zero counts, then weapons, action
flags and opened chests. Length bytes are stored as the count plus 32.
Counts that need more than one byte are 7-bit groups, high group first.

`page_row` is what the HTML leaderboard shows. It does not include the
password. See `gserverstat.md`.
"""


def _store(count):
    if not 0 <= count <= 223:
        raise ValueError('count does not fit in one length byte')
    return bytes([count + 32])


def gstr(text):
    if isinstance(text, str):
        text = text.encode('latin1')
    return _store(len(text)) + text


def _g7(value, width):
    out = bytearray()
    for shift in range((width - 1) * 7, -1, -7):
        out.append(((value >> shift) & 127) + 32)
    return bytes(out)


def _take(buf, index):
    if index >= len(buf):
        raise ValueError('truncated account')
    return buf[index] - 32, index + 1


def _take_gstr(buf, index):
    count, index = _take(buf, index)
    if count < 0 or index + count > len(buf):
        raise ValueError('bad string in account')
    return buf[index:index + count], index + count


def _take_g7(buf, index, width):
    value = 0
    for _ in range(width):
        piece, index = _take(buf, index)
        value = (value << 7) | (piece & 127)
    return value, index


def _take_list(buf, index, width):
    count, index = _take_g7(buf, index, width)
    items = []
    for _ in range(count):
        item, index = _take_gstr(buf, index)
        items.append(item)
    return items, index


def encode_account(name, password, proplist=b'', onlyload=False, adminlevel=0,
                   blocked=False, weapons=(), action_flags=(), opened_chests=()):
    if isinstance(name, str):
        name = name.encode('latin1')
    if isinstance(password, str):
        password = password.encode('latin1')
    if isinstance(proplist, str):
        proplist = proplist.encode('latin1')
    flags = (1 if onlyload else 0) | ((adminlevel & 7) << 1) | (16 if blocked else 0)
    out = gstr(name) + gstr(password) + gstr(proplist) + _store(flags)
    out += _store(0) + _store(0)
    weapons = list(weapons)
    out += _store(len(weapons))
    for weapon in weapons:
        if isinstance(weapon, str):
            weapon = weapon.encode('latin1')
        out += _g7(len(weapon), 2) + weapon
    out += _g7(len(action_flags), 2)
    for flag in action_flags:
        out += gstr(flag)
    out += _g7(len(opened_chests), 2)
    for chest in opened_chests:
        out += gstr(chest)
    return out


def decode_account(buf):
    name, index = _take_gstr(buf, 0)
    password, index = _take_gstr(buf, index)
    proplist, index = _take_gstr(buf, index)
    flags, index = _take(buf, index)
    # Two legacy counts. The writer stores zero. A non-zero count is a list
    # of length-prefixed strings, which is how older files were shaped.
    _legacy_actions, index = _take_list(buf, index, 1)
    _legacy_chests, index = _take_list(buf, index, 1)
    weapon_count, index = _take(buf, index)
    weapons = []
    for _ in range(weapon_count):
        size, index = _take_g7(buf, index, 2)
        if index + size > len(buf):
            raise ValueError('truncated weapon')
        weapons.append(buf[index:index + size])
        index += size
    action_flags, index = _take_list(buf, index, 2)
    opened_chests, index = _take_list(buf, index, 2)
    if index != len(buf):
        raise ValueError('trailing bytes in account')
    return {
        'name': name,
        'password': password,
        'proplist': proplist,
        'onlyload': bool(flags & 1),
        'adminlevel': (flags >> 1) & 7,
        'blocked': bool(flags & 16),
        'weapons': weapons,
        'action_flags': action_flags,
        'opened_chests': opened_chests,
    }


def encode_props(nickname=b'', rupees=0, kills=0, deaths=0, onlinesecs=0,
                 maxpower=3, alignment=0):
    """Property list for the leaderboard fields, in property-id order."""
    if isinstance(nickname, str):
        nickname = nickname.encode('latin1')

    def triple(value):
        if not 0 <= value < (1 << 21):
            raise ValueError('value does not fit in three 7-bit groups')
        return _g7(value, 3)

    parts = [
        _store(0) + gstr(nickname),
        _store(1) + _store(maxpower),
        _store(3) + triple(rupees),
        _store(27) + triple(kills),
        _store(28) + triple(deaths),
        _store(29) + triple(onlinesecs),
        _store(32) + _store(alignment),
    ]
    return b''.join(parts)


def decode_props(buf):
    """Decode a property list limited to the leaderboard fields."""
    names_one = {1: 'maxpower', 32: 'alignment'}
    names_three = {3: 'rupees', 27: 'kills', 28: 'deaths', 29: 'onlinesecs'}
    out = {}
    index = 0
    while index < len(buf):
        prop, index = _take(buf, index)
        if prop == 0:
            text, index = _take_gstr(buf, index)
            out['nickname'] = text
        elif prop in names_one:
            value, index = _take(buf, index)
            out[names_one[prop]] = value
        elif prop in names_three:
            value, index = _take_g7(buf, index, 3)
            out[names_three[prop]] = value
        else:
            raise ValueError('property %s is not a leaderboard field' % prop)
    return out


def page_row(account):
    """One leaderboard row. The password stays out of it."""
    props = decode_props(account['proplist'])
    nick = props.get('nickname', b'')
    row = {
        'nickname': nick.decode('latin1') if nick else '',
        'onlyload': account['onlyload'],
        'account': account['name'].decode('latin1'),
    }
    for key in ('maxpower', 'rupees', 'kills', 'deaths', 'onlinesecs', 'alignment'):
        if key in props:
            row[key] = props[key]
    return row


def select_page(accounts, key, limit=50):
    """Top `limit` rows for one column, highest value first.

    Skips only-load accounts and the account named super. An empty nickname
    is left blank. This is the public page for the simple columns (kills,
    deaths, rupees, and the rest of the single-field sorts). High and low
    alignment also break ties on kills; that rule is in the note, not here.
    """
    kept = []
    for account in accounts:
        row = page_row(account) if 'proplist' in account else account
        if row.get('onlyload'):
            continue
        if row.get('account') == 'super' or row.get('name') == 'super':
            continue
        kept.append(row)
    kept.sort(key=lambda row: row.get(key, 0), reverse=True)
    page = []
    for place, row in enumerate(kept[:limit], start=1):
        page.append({
            'place': place,
            'nickname': row.get('nickname') or '',
            key: row.get(key, 0),
        })
    return page
