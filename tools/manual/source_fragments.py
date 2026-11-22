"""Index supported Markdown source anchors for manual citation checks.

Standard library only. Common ATX/Setext headings and explicit HTML anchors are
supported; complex forms produce diagnostics rather than an assumed match.
This is not a full Markdown renderer and never rewrites source references.
"""
from __future__ import annotations
import html
from html.parser import HTMLParser
import re
import unicodedata

ATX = re.compile(r'^ {0,3}#{1,6}(?:[ \t]+|$)(.*)$')
SETEXT = re.compile(r'^ {0,3}(?:=+|-+)[ \t]*$')
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
HTML_TAG = re.compile(
    r'</[A-Za-z][A-Za-z0-9-]*[ \t\r\n]*>'
    r'|<[A-Za-z][A-Za-z0-9-]*(?:[ \t\r\n]+[A-Za-z_:][A-Za-z0-9_.:-]*'
    r'(?:[ \t\r\n]*=[ \t\r\n]*(?:"[^"]*"|\'[^\']*\'|[^\s"\'=<>`]+))?)*'
    r'[ \t\r\n]*/?>'
)

class CustomAnchors(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value is not None and (key == 'id' or (tag == 'a' and key == 'name')):
                self.anchors.add(value)

def outside_blocks(text: str):
    """Yield line number/text; preserve spaces, suppress comments and code."""
    fence_char = ''
    fence_len = 0
    in_comment = False
    for no, raw in enumerate(text.splitlines(), 1):
        if fence_char:
            close = re.match(r'^ {0,3}(' + re.escape(fence_char) + r'{'+str(fence_len)+r',})[ \t]*$', raw)
            if close:
                fence_char = ''
            yield no, None
            continue
        # A comment inside a code fence is literal, so fence recognition comes first.
        if not in_comment:
            opening = FENCE.match(raw)
            if opening and not (opening[1][0] == '`' and '`' in opening[2]):
                fence_char, fence_len = opening[1][0], len(opening[1])
                yield no, None
                continue
        pieces = []
        rest = raw
        while rest:
            if in_comment:
                end = rest.find('-->')
                if end < 0:
                    rest = ''
                    break
                rest = rest[end+3:]
                in_comment = False
            else:
                # Preserve escaped punctuation and complete inline-code spans
                # before recognizing comment openers in ordinary text.
                pos = 0
                while pos < len(rest):
                    if rest[pos] == '\\' and pos + 1 < len(rest):
                        pos += 2
                        continue
                    if rest[pos] == '`':
                        run = re.match(r'`+', rest[pos:])[0]
                        close = re.search(r'(?<!`)' + re.escape(run) + r'(?!`)', rest[pos+len(run):])
                        if close:
                            pos += len(run) + close.end()
                            continue
                        pos += len(run)
                        continue
                    if rest.startswith('<!--', pos):
                        break
                    pos += 1
                if pos >= len(rest):
                    pieces.append(rest)
                    break
                pieces.append(rest[:pos])
                rest = rest[pos+4:]
                in_comment = True
        line = ''.join(pieces)
        if raw.startswith(('    ', '\t')):
            yield no, None
        else:
            yield no, line

def heading_text(title: str, reference_ids=frozenset()):
    issues = []
    protected = []
    prefix = 'zqprotected'
    while prefix in title:
        prefix += 'z'
    def protect(value):
        token = prefix + str(len(protected)) + 'qz'
        protected.append((token, value))
        return token
    # Equal-length code delimiters; unsupported unmatched delimiters are diagnosed.
    def code(match):
        value = match[2].replace('\n', ' ')
        if value.startswith(' ') and value.endswith(' ') and value.strip(' '):
            value = value[1:-1]
        return protect(value)
    title = re.sub(r'(`+)(.+?)\1(?!`)', code, title)
    if '`' in title:
        issues.append('unmatched or complex inline-code delimiter')
    title = re.sub(r'\\([!"#$%&\'()*+,\-./:;<=>?@\[\]\\^_`{|}~])', lambda m: protect(m[1]), title)
    # Simple inline and reference links use visible labels, not destinations.
    title = re.sub(r'!?\[([^\[\]]*)\]\([^()]*\)', r'\1', title)
    def reference_link(match):
        label = match[2] or match[1]
        return match[1] if label.casefold() in reference_ids else match[0]
    title = re.sub(r'!?\[([^\[\]]*)\]\[([^\[\]]*)\]', reference_link, title)
    if re.search(r'\[[^]]*\]\(|\[\[', title):
        issues.append('nested/complex link syntax')
    if re.search(r'<[!?]', title):
        issues.append('HTML declaration or processing instruction in heading')
    # Autolinks and literal angle-bracket text are not HTML tags. Their visible
    # text must survive; stripping every <...> silently discarded URL headings.
    title = HTML_TAG.sub('', title)
    # Boundary underscores are emphasis; internal word underscores remain literal.
    title = re.sub(r'(?<!\w)(__|_)(?=\S)(.+?)(?<=\S)\1(?!\w)', r'\2', title)
    title = re.sub(r'(?<!\\)(\*{1,3})(?=\S)(.+?)(?<=\S)\1', r'\2', title)
    for token, value in protected:
        title = title.replace(token, value)
    return html.unescape(title), issues

def heading_slug(title: str, reference_ids=frozenset()):
    text, issues = heading_text(title, reference_ids)
    text = text.lower()
    # Unicode letters, marks and numbers are retained; this is not a
    # claim of complete Unicode/symbol/rendering parity.
    slug = ''.join(ch for ch in text if ch in '-_ ' or unicodedata.category(ch)[0] in 'LMN')
    return slug.replace(' ', '-'), issues

def source_anchors(text: str):
    automatic = set()
    custom = set()
    counters = {}
    headings = []
    unsupported = []
    html_candidates = []
    paragraph = []
    parser = CustomAnchors()
    visible = list(outside_blocks(text))
    reference_ids = frozenset(m[1].casefold() for _, line in visible if line is not None
                             for m in [re.match(r'^ {0,3}\[([^]]+)\]:[ \t]*\S', line)] if m)
    def add(title, no, kind):
        base, issues = heading_slug(title, reference_ids)
        slug = base
        while slug in automatic:
            counters[base] = counters.get(base, 0) + 1
            slug = base + '-' + str(counters[base])
        automatic.add(slug)
        headings.append({'line': no, 'kind': kind, 'title': title, 'anchor_id': slug})
        unsupported.extend({'line': no, 'reason': issue} for issue in issues)
    for no, line in visible:
        if line is None:
            paragraph = []
            continue
        html_scan = re.sub(r'(`+)(.+?)\1(?!`)', '', line)
        html_scan = re.sub(r'\\.', '', html_scan)
        try:
            parser.feed(html_scan + '\n')
        except Exception as exc:
            unsupported.append({'line': no, 'reason': 'HTML parse: '+str(exc)})
        if re.search(r'\[[^]]*\]\([^)]*<', html_scan):
            unsupported.append({'line': no, 'reason': 'HTML embedded in a Markdown link destination'})
        for match in re.finditer(r'</?(?:address|article|aside|blockquote|details|dialog|div|dl|fieldset|figure|footer|form|h[1-6]|header|hr|main|nav|ol|p|pre|script|section|style|summary|table|textarea|ul)\b[^>]*>', html_scan, re.I):
            html_candidates.append({'line': no, 'tag': match[0]})
        if html_candidates and html_candidates[-1]['line'] == no:
            unsupported.append({'line': no, 'reason': 'block-HTML Markdown interaction not modeled'})
        atx = ATX.match(line)
        if atx:
            title = re.sub(r'[ \t]+#+[ \t]*$', '', atx[1]).strip(' \t')
            add(title, no, 'ATX')
            paragraph = []
        elif SETEXT.match(line) and paragraph:
            add('\n'.join(s for _, s in paragraph), paragraph[0][0], 'Setext')
            paragraph = []
        elif not line.strip():
            paragraph = []
        elif re.match(r'^ {0,3}(?:>|[-+*][ \t]|\d+[.)][ \t])', line):
            if re.match(r'^ {0,3}(?:>[ \t]*|[-+*][ \t]+|\d+[.)][ \t]+)#{1,6}(?:[ \t]+|$)', line):
                unsupported.append({'line': no, 'reason': 'heading-like syntax nested in list/quote'})
            paragraph = []
        elif re.match(r'^ {0,3}(?:<|\|)', line) or SETEXT.match(line):
            paragraph = []
        else:
            paragraph.append((no, line.strip(' \t')))
    parser.close()
    custom.update(parser.anchors)
    # Custom anchors do not participate in automatic duplicate numbering.
    return {'automatic': sorted(automatic), 'custom': sorted(custom), 'headings': headings, 'unsupported': unsupported, 'html_block_candidates': html_candidates}
