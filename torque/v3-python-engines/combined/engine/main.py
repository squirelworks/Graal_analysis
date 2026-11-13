#!/usr/bin/env python3
"""One path: local level, a step, inner records, or a framed login.

--listen accepts the newline records from v3-python-repro.
--connect sends the a client routine frame to a host.
--framed-listen reads that frame.
"""

from __future__ import annotations

import argparse
import socket
import threading
from pathlib import Path

from console import Console
from netconnection import FramedHost, LineHost
from protocol import (
    LCG_STATE, apply_board, chat_bytes, file_ask_payload, parse_file_body,
    parse_number, parse_player_buffer, parse_record, parse_remote_player,
    parse_server_list, record, server_line, step_record, gchar_string, unframe,
)


def boot(nw: str | None) -> Console:
    con = Console()
    con.eval("createCanvas(Graal);")
    con.eval("start2D();")
    con.eval("Canvas.setContent(GraalCtrl);")
    if nw:
        text = Path(nw).read_text("latin1")
        assert con.graal is not None
        con.graal.loadLevel(text)
    return con


def apply_list(con: Console, payload: bytes) -> list[str]:
    """List-connection id 0. Fills the server-list lines the dialog draws."""
    assert con.graal is not None
    lines = []
    rows = []
    for fields in parse_server_list(payload):
        line = server_line(fields)
        port = parse_number(fields[7]) if len(fields) > 7 else None
        rows.append({
            "fields": fields,
            "line": line,
            "name": fields[0] if fields else "",
            "host": fields[6] if len(fields) > 6 else "",
            "port": port,
        })
        if line is not None:
            lines.append(line)
    con.graal.play.rows = rows
    con.graal.play.servers = lines
    con.graal.play.server_list_open = True
    con.graal.play.last = "list %d" % len(lines)
    return lines


def apply_game(con: Console, kind: int, payload: bytes) -> str:
    """a client routine. Id 0 replaces tiles. Id 2 places another player."""
    assert con.graal is not None
    if kind == 0:
        if con.graal.level is None:
            return "board no level"
        runs = apply_board(con.graal.level.tiles, payload)
        con.graal.play.last = "board %d" % runs
        return con.graal.play.last
    if kind == 2:
        player = parse_remote_player(payload)
        if player is None:
            return "player empty"
        lookup = player["lookup"]
        found = con.graal.remotes.pop(lookup, None)
        if found is not None:
            for key in ("x", "y", "field_3", "field_7_hi", "field_7_lo"):
                if key not in player and key in found:
                    player[key] = found[key]
        con.graal.remotes[player["id"]] = player
        label = "player %d" % player["id"]
        if label not in con.graal.play.players:
            con.graal.play.players.append(label)
        con.graal.play.player_list_open = True
        if "x" in player and "y" in player:
            con.graal.play.last = "player %d at %.1f,%.1f  stub player_field_3_unnamed" % (
                player["id"], player["x"], player["y"])
        else:
            con.graal.play.last = "player %d  stub position_unread" % player["id"]
        return con.graal.play.last
    if kind == 0x84:
        parsed = parse_file_body(payload)
        if parsed is None:
            return "file short"
        name, body = parsed
        if name not in con.graal.play.files.wanted:
            return "file %s unmatched" % name
        note = con.graal.play.files.write(name, body)
        con.graal.play.last = note
        return note
    return "id %d unread" % kind


def apply_inner(con: Console, body: bytes) -> list[str]:
    notes = []
    for line in body.split(b"\n"):
        if not line:
            continue
        kind, payload = parse_record(line)
        if kind in (0, 2, 0x84):
            notes.append(apply_game(con, kind, payload))
    return notes


def send_inner(host: str, port: int, con: Console, account: str, second: str, follow: str) -> None:
    """Newline records only. a client routine, no a client routine header."""
    assert con.graal is not None
    con.net.connect("%s:%s" % (host, port))
    account = account or con.graal.account or "guest"
    blob = record(5, b"G3D28015" + gchar_string(account) + gchar_string(second), first=True)
    blob += record(0x25, follow.encode("latin1", "replace"), first=False)
    asked = 0
    for name in con.graal.file_asks:
        payload = file_ask_payload(name)
        if payload is None:
            continue
        blob += record(0x17, payload, first=False)
        asked += 1
        if asked >= 4:
            break
    print("inner login %d bytes %s" % (len(blob), blob))
    sock = socket.create_connection((host, port), timeout=3)
    with sock:
        sock.settimeout(3)
        sock.sendall(blob)
        reply = b""
        while b"\n" not in reply:
            chunk = sock.recv(1024)
            if not chunk:
                break
            reply += chunk
    line = reply.split(b"\n", 1)[0]
    print("inner reply %s parsed %s" % (line, parse_player_buffer(line)))
    for note in apply_inner(con, reply):
        print(note)


def send_framed(host: str, port: int, con: Console, account: str, second: str, follow: str) -> None:
    assert con.graal is not None
    con.net.connect("%s:%s" % (host, port))
    account = account or con.graal.account or "guest"
    print("key state %08x word %d" % (LCG_STATE, con.net.link.word))
    frames = con.net.link.login(account, second, follow, con.graal.file_asks)
    print("torque connect %s" % con.net.getAddress())
    for i, frame in enumerate(frames):
        print("frame %d %d bytes %s" % (i, len(frame), frame))
    sock = socket.create_connection((host, port), timeout=3)
    with sock:
        sock.settimeout(3)
        sock.sendall(b"".join(frames))
        try:
            reply = sock.recv(1024)
        except socket.timeout:
            reply = b""
    if not reply:
        print("no framed reply")
        return
    mode, body, _state = unframe(reply, codec=3)
    print("framed reply mode %d parsed %s" % (mode, parse_player_buffer(body)))
    for note in apply_inner(con, body):
        print(note)


def main() -> None:
    parser = argparse.ArgumentParser(description="v3 combined console and protocol")
    parser.add_argument("--nw", default="")
    parser.add_argument("--steps", default="", help="comma list: up,down,left,right")
    parser.add_argument("--eval", default="", help="one console script")
    parser.add_argument("--listen", type=int, default=0, help="inner-record host on localhost")
    parser.add_argument("--framed-listen", type=int, default=0, help="outer-flush host on localhost")
    parser.add_argument("--inner", default="", help="send inner newline records to this host")
    parser.add_argument("--connect", default="", help="send a framed login to this host")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--account", default="guest")
    parser.add_argument("--second", default="")
    parser.add_argument("--follow", default="")
    parser.add_argument("--chat", default="", help="chat text queued after login")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    nw = args.nw or str(here / "examples" / "tiny.nw")
    con = boot(nw)
    if args.account and con.graal is not None:
        con.graal.setAccountName(args.account)
    if args.eval:
        print(con.eval(args.eval))
    stepped = False
    for step in [part for part in args.steps.split(",") if part]:
        print(con.eval("GraalCtrl.move%s();" % step.title()))
        stepped = True
    if stepped and step_record() is None:
        print("step record stub step_send_not_in_00310b0c")
    assert con.canvas is not None
    print(con.canvas.repaint())
    if con.ts is not None and con.view3d is not None and con.graal is not None:
        print("TS %.1f,%.1f 3D %.1f,%.1f activated %s camera %s" % (
            con.ts.x, con.ts.y, con.view3d.x, con.view3d.y,
            con.view3d.activated, con.camera.getPosition()))

    if args.inner:
        send_inner(args.inner, args.port, con, args.account, args.second, args.follow)
        _chat_after_login(con, args.chat)
        return
    if args.connect:
        host = args.connect
        port = args.port
        if host == "selected" and con.graal is not None and con.graal.play.port:
            host = con.graal.play.host
            port = con.graal.play.port
        send_framed(host, port, con, args.account, args.second, args.follow)
        _chat_after_login(con, args.chat)
        return
    if args.chat and not args.inner and not args.connect:
        _chat_after_login(con, args.chat)
        print(con.canvas.repaint())

    if args.framed_listen:
        host = FramedHost()
        ready = threading.Event()
        thread = threading.Thread(target=host.serve, args=(args.framed_listen, ready), daemon=True)
        thread.start()
        ready.wait(2)
        print("framed listening localhost:%d" % args.framed_listen)
        thread.join()
        return

    if args.listen:
        host = LineHost()
        ready = threading.Event()
        thread = threading.Thread(target=host.serve, args=(args.listen, ready), daemon=True)
        thread.start()
        ready.wait(2)
        print("listening localhost:%d" % args.listen)
        thread.join()


def _chat_after_login(con: Console, text: str) -> None:
    """a client routine after the login flushes. The bytes stay off the TCP socket.

    a client routine writes them through a client routine, and that wrapper is unread.
    """
    if not text or con.graal is None:
        return
    con.graal.setChat(text)
    print("chat id 0x16 inner %s stub udp_datagram_003a9de4" % (chat_bytes(text),))


if __name__ == "__main__":
    main()
