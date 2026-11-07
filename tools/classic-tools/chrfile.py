"""`CHR:1.00` character lines from Graal Character Designer and GChar.

A file is one text line:

    CHR:1.00<name>=<head.gif>,<sex>,<colour>,<colour>,<colour>,<colour>,<colour>

Sex is `male` or `female`. The five colour names are stored in order and are
not labelled in the file. Sample lines shipped with the tools use names such
as black, gray, red, and cynober. See `character-designer.md`.
"""


def parse_chr(text):
    line = text.strip().splitlines()[0].strip()
    prefix = 'CHR:1.00'
    if not line.startswith(prefix) or '=' not in line:
        raise ValueError('not a CHR:1.00 line')
    name, rest = line[len(prefix):].split('=', 1)
    parts = rest.split(',')
    if len(parts) != 7 or not name:
        raise ValueError('CHR line needs a name, a head, a sex and five colours')
    head, sex = parts[0], parts[1]
    colours = parts[2:]
    if sex not in ('male', 'female'):
        raise ValueError('sex must be male or female')
    if not head or any(not colour for colour in colours):
        raise ValueError('empty head or colour')
    return {
        'name': name,
        'head': head,
        'sex': sex,
        'colours': colours,
    }
