#!/usr/bin/env python3
"""Static checker for GS1 NPC scripts against the 2.05 rev 2 command table.

The command table, argument signatures, expression functions and the lists of
no-op and later-only commands are read from the manual (§8.2,
`manual/08-scripting/02-gs1-reference.md`), so the checker follows the manual
when the manual changes. Nothing here comes from a client binary.

What it checks:

- the script tokenises: strings closed, brackets balanced
- every statement is a known 2.05 command, a keyword (`if`, `else`, `for`,
  `while`, `function`, `return`, `break`, `continue`), an assignment, an
  increment or a call of a function the script defines
- each command gets the number of arguments its signature asks for
  (a trailing `S` or `M` argument may contain commas)
- name arguments (`I` item, `B` baddy, `L` carry object, `D` direction,
  `C` colour) use a name from the table when they are a bare word
- commands that 2.05 parses but ignores (§8.2.4.9), and commands that only
  later builds have (§8.2.7.3), are reported
- calls in expressions name a 2.05 expression function (§8.2.5)
- user functions are defined before the script ends and are not called
  without a definition
- a script that tests `timeout` also sets `timeout` or uses `sleep`

Rules from the real-client lab run (2.05 rev 2 on a GServer-v2 lab,
2026-11-04):

- no "quoted" strings: 2.05 keeps the quote marks as part of the text, so
  `strequals(#c,"buy bombs")` never matches; write the words bare
- the word `toweapons` must not appear in a comment: the server takes the
  first `toweapons` in the script text as the command and names the weapon
  after the comment
- each `say2` line fits the box: 2.05 does not wrap, so text past about 32
  characters runs off the edge (`#v(...)` counts as 4, `#s(...)` and `#c`
  as 12). `#b` breaks the line; the box shows three lines and pages on
- an empty `setcharprop #c,` does not clear the chat bubble; `message ;`
  clears the text an NPC shows with `message`
- scripts placed with `putnpc` must carry no `//` comments (see
  `putnpc_targets`): putnpc joins the lines before comments are removed, so
  the first comment swallows the rest of the script

Usage: gs1lint.py [--dialect 2.05] FILE_OR_DIR ...
Exit status 1 when any error is found.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANUAL = REPO / 'manual' / '08-scripting' / '02-gs1-reference.md'

KEYWORDS = {'if', 'else', 'for', 'while', 'function', 'return', 'break', 'continue'}

# App. E#201: both readings of the four disputed signatures are accepted.
DISPUTED = {
    'toinventory': ('S', 'M'),
    'puthorse': ('MRR', 'FRR'),
    'showimg': ('RMRR', 'RFRR'),
    'replaceani': ('MM', 'SS'),
}


@dataclass
class Table:
    commands: dict[str, tuple[str, ...]] = field(default_factory=dict)
    ignored: set[str] = field(default_factory=set)
    later_only: set[str] = field(default_factory=set)
    functions: set[str] = field(default_factory=set)
    names: dict[str, set[str]] = field(default_factory=dict)


def _names_from_row(text: str) -> set[str]:
    return set(re.findall(r'\d+ ([a-z][a-z0-9]*)', text))


def load_table(path: Path = MANUAL) -> Table:
    t = Table()
    section = ''
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('#'):
            section = line
            continue
        m = re.match(r'^\| (\d{3}) \| `([a-z0-9]+)`[^|]*\| ([^|]*)\|', line)
        if m:
            name, args = m.group(2), m.group(3).strip()
            if name in DISPUTED:
                sigs = DISPUTED[name]
            elif args in ('—', '-', ''):
                sigs = ('',)
            else:
                sigs = (args.strip('`'),)
            t.commands[name] = sigs
            if '8.2.4.9' in section:
                t.ignored.add(name)
            continue
        if '8.2.5' in section and line.startswith('| ') and '–' in line.split('|')[1]:
            ids = line.split('|')[1].strip()
            if ids.split('–')[0].isdigit() and int(ids.split('–')[0]) < 600:
                for fn in re.findall(r'`([a-z0-9]+)\(', line):
                    t.functions.add(fn)
        if '8.2.2' in section and line.startswith('| '):
            cells = [c.strip() for c in line.split('|')]
            if len(cells) > 2:
                key = cells[1]
                if key.startswith('items'):
                    t.names['I'] = _names_from_row(cells[2])
                elif key.startswith('baddies'):
                    t.names['B'] = _names_from_row(cells[2])
                elif key.startswith('colours'):
                    t.names['C'] = _names_from_row(cells[2])
                elif key.startswith('carry objects'):
                    t.names['L'] = _names_from_row(cells[2])
                elif key.startswith('directions'):
                    t.names['D'] = {'up', 'left', 'down', 'right'}
        if '8.2.7.3' in section and 'absent in 2.05' in line:
            cell = line.split('|')[2]
            t.later_only = set(re.findall(r'`([a-z0-9]+)`', cell))
    t.later_only -= set(t.commands)
    if len(t.commands) != 161:
        raise RuntimeError(f'expected 161 commands in {path}, read {len(t.commands)}')
    return t


# ---------------------------------------------------------------- tokens

TOKEN_RE = re.compile(r'''
    (?P<ws>\s+)
  | (?P<comment>//[^\n]*|/\*.*?\*/)
  | (?P<string>"(?:[^"\\\n]|\\.)*")
  | (?P<code>\#[A-Za-z0-9]+(?:\([^()]*(?:\([^()]*\)[^()]*)*\))?)
  | (?P<number>\d+\.\d*|\.\d+|\d+)
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)
  | (?P<op>\+\+|--|\+=|-=|\*=|/=|==|!=|<=|>=|&&|\|\||[-+*/%^<>=!(){}\[\];,.|:@?])
  | (?P<other>.)
''', re.VERBOSE | re.DOTALL)


@dataclass
class Tok:
    kind: str
    text: str
    line: int


class LintError(Exception):
    def __init__(self, line: int, msg: str):
        super().__init__(msg)
        self.line = line
        self.msg = msg


def tokenize(src: str) -> list[Tok]:
    toks, pos, line = [], 0, 1
    while pos < len(src):
        m = TOKEN_RE.match(src, pos)
        if not m:
            raise LintError(line, f'cannot read {src[pos:pos + 12]!r}')
        kind = m.lastgroup
        text = m.group()
        if kind not in ('ws', 'comment'):
            toks.append(Tok(kind, text, line))
        line += text.count('\n')
        pos = m.end()
    toks.append(Tok('eof', '', line))
    return toks


# ---------------------------------------------------------------- parser

class Parser:
    def __init__(self, toks: list[Tok], table: Table, report):
        self.t = toks
        self.i = 0
        self.table = table
        self.report = report
        self.defined: set[str] = set()
        self.called: dict[str, int] = {}
        self.uses_timeout_event = 0
        self.sets_timer = False

    # helpers
    @property
    def cur(self) -> Tok:
        return self.t[self.i]

    def peek(self, k: int = 1) -> Tok:
        return self.t[min(self.i + k, len(self.t) - 1)]

    def take(self) -> Tok:
        tok = self.t[self.i]
        self.i += 1
        return tok

    def expect(self, text: str) -> Tok:
        if self.cur.text != text:
            raise LintError(self.cur.line, f'expected {text!r}, found {self.cur.text or "end of file"!r}')
        return self.take()

    # statements
    def script(self):
        while self.cur.kind != 'eof':
            self.statement()

    def block_or_statement(self):
        if self.cur.text == '{':
            self.take()
            while self.cur.text != '}':
                if self.cur.kind == 'eof':
                    raise LintError(self.cur.line, "missing '}'")
                self.statement()
            self.take()
        else:
            self.statement()

    def statement(self):
        tok = self.cur
        if tok.text == ';':
            self.take()
            return
        if tok.text == '{':
            self.block_or_statement()
            return
        if tok.kind == 'name' and tok.text in KEYWORDS:
            return self.keyword()
        if tok.kind == 'name' and tok.text in self.table.commands:
            return self.command()
        if tok.kind == 'name' and tok.text in self.table.later_only:
            raise LintError(tok.line, f'`{tok.text}` is not in the 2.05 command table (2.22 documentation only)')
        return self.expression_statement()

    def keyword(self):
        tok = self.take()
        kw = tok.text
        if kw in ('if', 'while'):
            self.expect('(')
            self.condition_expr()
            self.expect(')')
            self.block_or_statement()
            if kw == 'if' and self.cur.text == 'else':
                self.take()
                self.block_or_statement()
        elif kw == 'for':
            self.expect('(')
            if self.cur.text != ';':
                self.simple_statement()
            self.expect(';')
            if self.cur.text != ';':
                self.expr()
            self.expect(';')
            if self.cur.text != ')':
                self.simple_statement()
            self.expect(')')
            self.block_or_statement()
        elif kw == 'function':
            name = self.take()
            if name.kind != 'name':
                raise LintError(name.line, 'function needs a name')
            if name.text in self.table.commands:
                raise LintError(name.line, f'function name `{name.text}` is a command')
            self.defined.add(name.text)
            self.expect('(')
            self.expect(')')
            if self.cur.text != '{':
                raise LintError(self.cur.line, 'function body must be a block')
            self.block_or_statement()
        elif kw == 'else':
            raise LintError(tok.line, '`else` without `if`')
        else:  # return, break, continue
            self.expect(';')

    def condition_expr(self):
        start = self.i
        self.expr()
        names = [t.text for t in self.t[start:self.i] if t.kind == 'name']
        if 'timeout' in names:
            self.uses_timeout_event = self.uses_timeout_event or self.t[start].line

    def simple_statement(self):
        """Assignment, increment or call, without the closing ';'."""
        tok = self.cur
        if tok.text in ('++', '--'):
            self.take()
            self.lvalue()
            return
        if tok.kind != 'name':
            raise LintError(tok.line, f'unexpected {tok.text!r} at start of statement')
        if self.peek().text == '(' and '.' not in tok.text:
            self.take()
            self.expect('(')
            self.expect(')')
            self.called.setdefault(tok.text, tok.line)
            return
        target = self.lvalue()
        op = self.cur
        if op.text in ('++', '--'):
            self.take()
            return
        if op.text in ('=', '+=', '-=', '*=', '/=', ':='):
            self.take()
            if target == 'timeout':
                self.sets_timer = True
            self.expr()
            return
        raise LintError(tok.line, f'`{tok.text}` is not a 2.05 command and the statement is not an assignment')

    def expression_statement(self):
        self.simple_statement()
        self.expect(';')

    def lvalue(self) -> str:
        tok = self.take()
        if tok.kind != 'name':
            raise LintError(tok.line, f'expected a variable, found {tok.text!r}')
        while self.cur.text == '[':
            self.take()
            self.expr()
            self.expect(']')
            if self.cur.text == '.':
                self.take()
                self.take()
        return tok.text

    # commands
    def command(self):
        tok = self.take()
        name = tok.text
        if name in self.table.ignored:
            raise LintError(tok.line, f'`{name}` is parsed but ignored by the 2.05 client (§8.2.4.9)')
        if name == 'sleep':
            self.sets_timer = True
        args: list[list[Tok]] = [[]]
        depth = 0
        while True:
            t = self.cur
            if t.kind == 'eof':
                raise LintError(tok.line, f'`{name}` is missing its closing ";"')
            if t.text == ';' and depth == 0:
                self.take()
                break
            if t.text in '([{':
                depth += 1
            elif t.text in ')]}':
                depth -= 1
                if depth < 0:
                    raise LintError(t.line, f'unbalanced {t.text!r} in `{name}`')
            if t.text == ',' and depth == 0:
                args.append([])
            else:
                args[-1].append(t)
            self.take()
        if args == [[]]:
            args = []
        sigs = self.table.commands[name]
        errors = []
        for sig in sigs:
            err = self.check_args(name, sig, args, tok.line)
            if err is None:
                return
            errors.append(err)
        raise LintError(tok.line, errors[0])

    def check_args(self, name: str, sig: str, args: list[list[Tok]], line: int):
        n = len(sig)
        if len(args) < n:
            if not (len(args) == n - 1 and sig and sig[-1] in 'SM'):
                return f'`{name}` takes {n} argument(s) ({sig or "none"}), got {len(args)}'
        if len(args) > n:
            if not (sig and sig[-1] in 'SM'):
                return f'`{name}` takes {n} argument(s) ({sig or "none"}), got {len(args)}'
        for letter, arg in zip(sig, args):
            if letter in 'RD' or (letter in 'C' and arg and arg[0].kind != 'name'):
                if letter == 'D' and len(arg) == 1 and arg[0].text in self.table.names['D']:
                    continue
                err = self.check_expr(arg, line)
                if err:
                    return f'`{name}`: {err}'
            elif letter in 'IBLC':
                if not arg:
                    return f'`{name}`: empty {letter} argument'
                if len(arg) == 1 and arg[0].kind == 'name':
                    table = self.table.names.get(letter, set())
                    if arg[0].text not in table and not arg[0].text.startswith('this.'):
                        return f'`{name}`: `{arg[0].text}` is not a name in table {letter}'
        return None

    def check_expr(self, arg: list[Tok], line: int):
        if not arg:
            return 'empty numeric argument'
        sub = Parser(arg + [Tok('eof', '', line)], self.table, self.report)
        try:
            sub.expr()
            if sub.cur.kind != 'eof':
                return f'unexpected {sub.cur.text!r} in numeric argument'
        except LintError as e:
            return e.msg
        return None

    # expressions
    def expr(self):
        self.binary(0)

    LEVELS = [('||',), ('&&',), ('==', '!=', '<', '>', '<=', '>=', 'in'), ('+', '-'), ('*', '/', '%'), ('^',)]

    def binary(self, level: int):
        if level == len(self.LEVELS):
            return self.unary()
        self.binary(level + 1)
        while self.cur.text in self.LEVELS[level]:
            op = self.take().text
            if op == 'in' and self.cur.text in ('|', '{'):
                self.range_or_set()
            else:
                self.binary(level + 1)

    def range_or_set(self):
        close = '|' if self.cur.text == '|' else '}'
        self.take()
        self.expr()
        while self.cur.text == ',':
            self.take()
            self.expr()
        self.expect(close)

    def unary(self):
        if self.cur.text in ('!', '-', '+'):
            self.take()
            return self.unary()
        return self.primary()

    def primary(self):
        tok = self.cur
        if tok.text == '(':
            self.take()
            self.expr()
            self.expect(')')
            return
        if tok.text == '{':
            self.range_or_set()
            return
        if tok.kind in ('number', 'string', 'code'):
            self.take()
            return
        if tok.kind == 'name':
            self.take()
            if self.cur.text == '(':
                if tok.text not in self.table.functions:
                    raise LintError(tok.line, f'`{tok.text}(...)` is not a 2.05 expression function')
                self.take()
                if self.cur.text != ')':
                    self.call_arg()
                    while self.cur.text == ',':
                        self.take()
                        self.call_arg()
                self.expect(')')
                return
            while self.cur.text == '[':
                self.take()
                self.expr()
                self.expect(']')
                if self.cur.text == '.':
                    self.take()
                    self.take()
            if self.cur.text in ('++', '--'):
                self.take()
            return
        raise LintError(tok.line, f'unexpected {tok.text or "end of line"!r} in expression')

    def call_arg(self):
        # String arguments may be bare `#` codes or plain words, several words
        # included (strequals(#c,buy bombs)); 2.05 takes the text up to the
        # next `,` or `)` as it is.
        start = self.i
        try:
            self.expr()
            if self.cur.text in (',', ')'):
                return
        except LintError:
            pass
        self.i = start
        depth = 0
        while True:
            t = self.cur
            if t.kind == 'eof' or t.text == ';':
                raise LintError(t.line, 'unterminated function argument')
            if t.text == '(':
                depth += 1
            elif t.text == ')':
                if depth == 0:
                    return
                depth -= 1
            elif t.text == ',' and depth == 0:
                return
            self.take()


# ---------------------------------------------------------------- driver

@dataclass
class Finding:
    path: str
    line: int
    level: str
    msg: str

    def __str__(self) -> str:
        return f'{self.path}:{self.line}: {self.level}: {self.msg}'


SAY2_WIDTH = 32


def _say2_width(text: str) -> int:
    text = re.sub(r'#v\([^()]*(?:\([^()]*\)[^()]*)*\)', 'x' * 4, text)
    text = re.sub(r'#s\([^()]*\)', 'x' * 12, text)
    text = text.replace('#c', 'x' * 12)
    return len(text.strip())


def lab_checks(src: str, toks: list[Tok]) -> list[tuple[int, str, str]]:
    """Checks that come from the real-client lab run rather than the manual."""
    found = []
    for t in toks:
        if t.kind == 'string':
            found.append((t.line, 'error', f'quoted text {t.text}: 2.05 keeps the quote marks, so it never matches; write the words bare'))
    for m in re.finditer(r'//[^\n]*|/\*.*?\*/', src, re.DOTALL):
        if re.search(r'\btoweapons\b', m.group()):
            line = src.count('\n', 0, m.start()) + 1
            found.append((line, 'error', 'the word `toweapons` in a comment: the server takes the comment text as the weapon name'))
    for i, t in enumerate(toks[:-3]):
        if t.text == 'setcharprop' and toks[i + 1].text == '#c' and toks[i + 2].text == ',' and toks[i + 3].text == ';':
            found.append((t.line, 'error', 'an empty `setcharprop #c,` does not clear the chat bubble on 2.05; use `message` and an empty `message ;`'))
    for i, t in enumerate(toks):
        if t.kind == 'name' and t.text == 'say2' and (i == 0 or toks[i - 1].text in (';', '{', '}', ')', 'else')):
            # rebuild the text from the source line(s) up to the closing ';'
            start = sum(len(l) + 1 for l in src.split('\n')[:t.line - 1])
            m = re.compile(r'\bsay2\s+([^;]*);').search(src, start)
            if m:
                for part in m.group(1).split('#b'):
                    if _say2_width(part) > SAY2_WIDTH:
                        found.append((t.line, 'warning', f'`say2` line is {_say2_width(part)} characters; 2.05 does not wrap and cuts it off past about {SAY2_WIDTH}; break it with #b'))
                        break
    return found


def putnpc_targets(src: str) -> list[str]:
    """Script file names this script passes to `putnpc`."""
    return re.findall(r'^\s*putnpc\s+[^,;]*,\s*([^,;\s]+)', src, re.MULTILINE)


def lint_text(src: str, path: str = '<text>', table: Table | None = None) -> list[Finding]:
    table = table or load_table()
    out: list[Finding] = []
    try:
        toks = tokenize(src)
    except LintError as e:
        return [Finding(path, e.line, 'error', e.msg)]
    lab = [Finding(path, line, level, msg) for line, level, msg in lab_checks(src, toks)]
    try:
        p = Parser(toks, table, out.append)
        p.script()
    except LintError as e:
        return lab + [Finding(path, e.line, 'error', e.msg)]
    out = lab + out
    for fn, line in p.called.items():
        if fn not in p.defined:
            out.append(Finding(path, line, 'error', f'`{fn}()` is called but never defined'))
    if p.uses_timeout_event and not p.sets_timer:
        out.append(Finding(path, p.uses_timeout_event, 'warning', 'tests `timeout` but never sets `timeout` or calls `sleep`'))
    return out


def iter_files(paths: list[str]):
    for p in map(Path, paths):
        if p.is_dir():
            yield from sorted(p.rglob('*.gs1'))
        else:
            yield p


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('paths', nargs='+')
    ap.add_argument('-q', '--quiet', action='store_true', help='print errors only')
    args = ap.parse_args(argv)
    table = load_table()
    errors = 0
    count = 0
    for f in iter_files(args.paths):
        count += 1
        for finding in lint_text(f.read_text(encoding='utf-8'), str(f), table):
            if finding.level == 'error':
                errors += 1
            if finding.level == 'error' or not args.quiet:
                print(finding)
    print(f'{count} file(s), {errors} error(s)', file=sys.stderr)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
