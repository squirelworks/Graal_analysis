"""Tests for the local notes navigator."""

import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import navigator  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
OUTSIDE_MARKER = 'OUTSIDE-NOTE-MARKER'
SCRIPT = '<script>alert(1)</script>'


def test_index_includes_readme_protocol_and_formats():
    index = navigator.build_index(REPO)
    by_path = {entry['path']: entry for entry in index}
    assert 'README.md' in by_path
    assert by_path['README.md']['folder'] == 'root'
    assert by_path['README.md']['title']
    protocol = [entry for entry in index if entry['path'].startswith('protocol/')]
    formats = [entry for entry in index if entry['path'].startswith('formats/')]
    assert protocol
    assert formats
    assert protocol[0]['folder'] == 'protocol'
    assert formats[0]['folder'] == 'formats'
    assert all('.git' not in entry['path'].split('/') for entry in index)


def test_index_skips_git_directory(tmp_path):
    git_note = tmp_path / '.git' / 'COMMIT_EDITMSG.md'
    git_note.parent.mkdir()
    git_note.write_text('# secret git\n', encoding='utf-8')
    (tmp_path / 'README.md').write_text('# Home\n', encoding='utf-8')
    paths = [entry['path'] for entry in navigator.build_index(tmp_path)]
    assert paths == ['README.md']


def test_filter_notes_by_title_and_path():
    entries = [
        {'path': 'protocol/packet-ids.md', 'title': 'Packet id tables', 'folder': 'protocol'},
        {'path': 'formats/gmap.md', 'title': 'World map', 'folder': 'formats'},
        {'path': 'tools/lab-setup.md', 'title': 'Lab setup', 'folder': 'tools'},
    ]
    assert navigator.filter_notes(entries, '') == entries
    assert navigator.filter_notes(entries, '   ') == entries
    assert [entry['path'] for entry in navigator.filter_notes(entries, 'packet')] == [
        'protocol/packet-ids.md'
    ]
    assert [entry['path'] for entry in navigator.filter_notes(entries, 'FORMATS/')] == [
        'formats/gmap.md'
    ]
    assert [entry['path'] for entry in navigator.filter_notes(entries, 'LAB SETUP')] == [
        'tools/lab-setup.md'
    ]
    assert navigator.filter_notes(entries, 'no-such-note') == []


def test_render_escapes_script_and_does_not_emit_active_html(tmp_path):
    (tmp_path / 'notes').mkdir()
    text = (
        '# Hello <script>alert(1)</script>\n\n'
        'A paragraph with <script>alert(1)</script> and '
        '<img src="x" onerror="alert(1)">.\n\n'
        '[click](javascript:alert(1))\n\n'
        '![shot](https://example.invalid/a.png)\n\n'
        '```html\n'
        '<script>alert(1)</script>\n'
        '```\n'
    )
    rendered = navigator.render_markdown(text, 'notes/hello.md', tmp_path)
    assert '<script' not in rendered.lower()
    assert '<img' not in rendered.lower()
    assert '&lt;img' in rendered
    assert 'href="javascript:' not in rendered.lower()
    assert 'href="https:' not in rendered.lower()
    assert 'href="http:' not in rendered.lower()
    assert '<p>click</p>' in rendered
    assert '&lt;script&gt;' in rendered
    assert rendered.lower().count('&lt;script&gt;') >= 3


def test_render_links_other_notes(tmp_path):
    protocol = tmp_path / 'protocol'
    formats = tmp_path / 'formats'
    protocol.mkdir()
    formats.mkdir()
    (protocol / 'a.md').write_text(
        '# A\n\nSee [gmap](../formats/gmap.md) and [local](b.md).\n',
        encoding='utf-8',
    )
    (protocol / 'b.md').write_text('# B\n', encoding='utf-8')
    (formats / 'gmap.md').write_text('# Gmap\n', encoding='utf-8')
    rendered = navigator.render_markdown(
        (protocol / 'a.md').read_text(encoding='utf-8'),
        'protocol/a.md',
        tmp_path,
    )
    assert 'href="/note?path=formats/gmap.md"' in rendered
    assert 'data-note="formats/gmap.md"' in rendered
    assert 'href="/note?path=protocol/b.md"' in rendered
    assert '<h1 id="a">A</h1>' in rendered
    anchored = navigator.render_markdown(
        'See [local](b.md#section).\n',
        'protocol/a.md',
        tmp_path,
    )
    assert 'href="/note?path=protocol/b.md#section"' in anchored
    assert 'data-note="protocol/b.md"' in anchored


def test_real_note_emits_only_known_tags():
    text = (REPO / 'protocol' / 'packet-ids.md').read_text(encoding='utf-8')
    text += '\n\n<script>alert(1)</script>\n'
    rendered = navigator.render_markdown(text, 'protocol/packet-ids.md', REPO)
    allowed = re_allowed_tag()
    leftover = allowed.sub('', rendered)
    assert '<' not in leftover
    assert '>' not in leftover
    assert '<script' not in rendered.lower()
    assert '&lt;script&gt;' in rendered
    assert '<table>' in rendered
    assert '<h1' in rendered


def re_allowed_tag():
    import re
    return re.compile(
        r'</?(?:h[1-6]|p|ul|ol|li|pre|code|a|strong|em|table|thead|tbody|tr|th|td|'
        r'blockquote|hr|br)(?:\s[^<>]*)?>',
        re.IGNORECASE,
    )


def _serve(repo: Path):
    server = navigator.make_server(repo, navigator.LOOPBACK, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop(server, thread):
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)


def _get(port: int, path: str) -> tuple[int, str]:
    url = 'http://%s:%d%s' % (navigator.LOOPBACK, port, path)
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode('utf-8')


def _write_corpus(tmp_path: Path) -> Path:
    outside = tmp_path.parent / f'{tmp_path.name}-outside.md'
    outside.write_text(f'# Secret\n\n{OUTSIDE_MARKER}\n{SCRIPT}\n', encoding='utf-8')
    (tmp_path / 'README.md').write_text('# Readme\n', encoding='utf-8')
    protocol = tmp_path / 'protocol'
    formats = tmp_path / 'formats'
    protocol.mkdir()
    formats.mkdir()
    (protocol / 'a.md').write_text(
        f'# Protocol note\n\nSee [formats](../formats/b.md).\n\n{SCRIPT}\n',
        encoding='utf-8',
    )
    (formats / 'b.md').write_text('# Formats note\n', encoding='utf-8')
    (tmp_path / 'secret.txt').write_text('SECRET-TEXT-MARKER\n', encoding='utf-8')
    link = tmp_path / 'linked.md'
    link.symlink_to(outside)
    return outside


def test_server_refuses_path_outside_repo(tmp_path):
    outside = _write_corpus(tmp_path)
    server, thread = _serve(tmp_path)
    try:
        port = server.server_address[1]
        outside_name = urllib.parse.quote(outside.name)
        cases = [
            '/note?path=' + urllib.parse.quote('../' + outside.name),
            '/note?path=' + urllib.parse.quote(str(outside)),
            '/note?path=' + urllib.parse.quote('protocol/../../' + outside.name),
            '/note?path=linked.md',
            '/note?path=' + urllib.parse.quote('protocol/a.md/' + '../' * 8 + outside.name),
        ]
        for path in cases:
            status, body = _get(port, path)
            assert status == 403, path
            assert OUTSIDE_MARKER not in body
            assert '<script' not in body.lower()
        status, body = _get(port, '/note?path=secret.txt')
        assert status == 404
        assert 'SECRET-TEXT-MARKER' not in body
        status, body = _get(port, '/note?path=protocol/a.md')
        assert status == 200
        assert OUTSIDE_MARKER not in body
        assert '&lt;script&gt;' in body
    finally:
        _stop(server, thread)
        outside.unlink(missing_ok=True)


def test_server_escapes_script_in_served_note(tmp_path):
    outside = _write_corpus(tmp_path)
    server, thread = _serve(tmp_path)
    try:
        port = server.server_address[1]
        status, body = _get(port, '/note?path=protocol/a.md&fragment=1')
        assert status == 200
        assert '<script' not in body.lower()
        assert '&lt;script&gt;' in body
        assert 'href="/note?path=formats/b.md"' in body
        status, page = _get(port, '/')
        assert status == 200
        assert page.lower().count('<script') == 1
        assert 'function noteMatches' in page
        assert 'id="search"' in page
        assert '/search' not in page
        assert 'data-path="README.md"' in page
        assert 'data-path="protocol/a.md"' in page
        assert 'data-path="formats/b.md"' in page
        status, missing = _get(port, '/search?q=protocol')
        assert status == 404
        assert 'protocol note' not in missing.lower()
    finally:
        _stop(server, thread)
        outside.unlink(missing_ok=True)


def test_server_refuses_non_loopback(tmp_path):
    (tmp_path / 'README.md').write_text('# Home\n', encoding='utf-8')
    try:
        navigator.make_server(tmp_path, host='example.invalid', port=0)
        raised = False
    except ValueError:
        raised = True
    assert raised
    assert navigator.main(['--host', 'example.invalid', '--repo', str(tmp_path)]) == 2
    assert navigator.is_loopback_host(navigator.LOOPBACK)
    assert navigator.DEFAULT_PORT == 8765
