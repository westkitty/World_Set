#!/usr/bin/env python3
"""Static server for the WORLD KIT explorer.

Maps:
  /            -> tools/explorer/index.html
  /wk/<path>   -> dist/WORLD_KIT/<path>   (the deliverables)
  /repo/<file> -> <repo>/<file>            (README.md / PIPELINE.md only)

Binds 0.0.0.0 so the Arena live preview (proxied per-port host) can reach it.
Relative URLs only - the browser is not the sandbox.
"""

import http.server
import os
import posixpath
import socketserver
import urllib.parse

PORT = int(os.environ.get("PORT", "8000"))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WK = os.path.join(ROOT, "dist", "WORLD_KIT")
SITE = os.path.join(ROOT, "tools", "explorer")
REPO_ALLOW = {"README.md", "PIPELINE.md"}


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = urllib.parse.urlparse(path).path
        path = posixpath.normpath(urllib.parse.unquote(path))
        parts = [p for p in path.split("/") if p and p not in (".", "..")]

        if parts and parts[0] == "wk":
            base, parts = WK, parts[1:]
        elif parts and parts[0] == "repo":
            name = parts[1] if len(parts) > 1 else "README.md"
            if name not in REPO_ALLOW:
                name = "README.md"
            return os.path.join(ROOT, name)
        else:
            base, parts = SITE, parts

        if not parts:
            return os.path.join(base, "index.html")
        return os.path.join(base, *parts)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):  # quiet
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("0.0.0.0", PORT), Handler) as httpd:
        print(f"[explorer] serving on 0.0.0.0:{PORT}", flush=True)
        httpd.serve_forever()
