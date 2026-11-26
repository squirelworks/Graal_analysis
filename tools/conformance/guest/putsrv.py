#!/usr/bin/env python3
"""Receive the client VM's run artefacts (lab only): `curl -T FILE
http://<server>:PORT/NAME` writes DIR/NAME. The client VM has no other way
out: it sits on the VM-only lab link.

    putsrv.py PORT DIR
"""
import http.server
import os
import sys

D = sys.argv[2]


class H(http.server.BaseHTTPRequestHandler):
    def do_PUT(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        p = os.path.join(D, os.path.basename(self.path))
        with open(p, "wb") as f:
            f.write(body)
        self.send_response(201)
        self.end_headers()
        print("got", p, n, flush=True)


http.server.HTTPServer(("", int(sys.argv[1])), H).serve_forever()
