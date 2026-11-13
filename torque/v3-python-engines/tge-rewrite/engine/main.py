#!/usr/bin/env python3
"""Terminal canvas: create the GuiCanvas, load a local .nw, walk, or host.

Usage from this directory's parent is not required. Run this file.
--listen speaks the v3 Python client's newline records.
"""

from __future__ import annotations

import argparse
import threading
from pathlib import Path

from console import Console
from netconnection import LineHost


def boot(nw: str | None) -> Console:
    con = Console()
    con.eval("createCanvas(Graal);")
    con.eval("start2D();")
    con.eval("Canvas.setContent(GraalCtrl);")
    # setContent resolves the name GraalCtrl to the control.
    if nw:
        text = Path(nw).read_text("latin1")
        assert con.graal is not None
        con.graal.loadLevel(text)
    return con


def main() -> None:
    parser = argparse.ArgumentParser(description="v3 Torque surface, terminal canvas")
    parser.add_argument("--nw", default="")
    parser.add_argument("--steps", default="", help="comma list: up,down,left,right")
    parser.add_argument("--eval", default="", help="one console line")
    parser.add_argument("--listen", type=int, default=0, help="host the v3 Python client on localhost")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    nw = args.nw or str(here / "examples" / "tiny.nw")
    con = boot(nw)
    if args.eval:
        print(con.eval(args.eval))
    for step in [part for part in args.steps.split(",") if part]:
        print(con.eval("GraalCtrl.move%s();" % step.title()))
    assert con.canvas is not None
    print(con.canvas.repaint())

    if args.listen:
        host = LineHost()
        ready = threading.Event()
        thread = threading.Thread(target=host.serve, args=(args.listen, ready), daemon=True)
        thread.start()
        ready.wait(2)
        print("listening localhost:%d" % args.listen)
        thread.join()


if __name__ == "__main__":
    main()
