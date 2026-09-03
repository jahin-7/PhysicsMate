"""Local demo server for the 3 fine-tuned NCTB Bangla-physics models.

Pure Python standard library -- no pip installs, no venv, no framework. Just:

    python3 server.py

then open http://localhost:8000 . Serves the Apple-design chat page and proxies
to a locally-running Ollama (localhost:11434). Fully offline; nothing leaves the
machine.

Endpoints
  GET  /                -> the chat page (index.html)
  GET  /api/models      -> the 3 fine-tuned models, smallest first
  GET  /api/samples     -> curated sample questions (from the held-out test set)
  POST /api/warm        -> {model}          preload a model into memory
  POST /api/chat        -> {model, message} stream the answer back as plain text

Design notes
  - Single-shot: each /api/chat sends just the user's question, no history and no
    system prompt -- these models were fine-tuned as closed-book single-turn QA,
    so that's the distribution they expect. Stateless: the server stores nothing
    between requests.
  - /api/chat relays Ollama's streaming JSON lines, extracting message.content and
    forwarding the raw text deltas, so the browser only has to append strings.
"""
import json
import pathlib
import socket
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = pathlib.Path(__file__).resolve().parent
OLLAMA = "http://localhost:11434"
PORT = 8000

# smallest-first: the switcher reads left-to-right as "capability grows with size"
MODELS = [
    {"id": "nctb-0.6b", "label": "0.6B", "name": "Qwen3-0.6B"},
    {"id": "nctb-1.7b", "label": "1.7B", "name": "Qwen3-1.7B"},
    {"id": "nctb-4b", "label": "4B", "name": "Qwen3-4B"},
]


def _read_json(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if not length:
        return {}
    return json.loads(handler.rfile.read(length) or b"{}")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # keep the console quiet during a live demo

    # ---- helpers -------------------------------------------------------
    def _send(self, code, body, content_type="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ---- routing -------------------------------------------------------
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html = (HERE / "index.html").read_text(encoding="utf-8")
            return self._send(200, html, "text/html; charset=utf-8")
        if self.path == "/api/models":
            return self._send(200, MODELS)
        if self.path == "/api/samples":
            samples = json.loads((HERE / "samples.json").read_text(encoding="utf-8"))
            return self._send(200, samples)
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/api/warm":
            return self._warm()
        if self.path == "/api/chat":
            return self._chat()
        return self._send(404, {"error": "not found"})

    # ---- model ops -----------------------------------------------------
    def _warm(self):
        """Preload a model so the first real message is instant. An empty prompt
        with keep_alive just triggers the load and returns."""
        model = _read_json(self).get("model", "")
        try:
            req = urllib.request.Request(
                f"{OLLAMA}/api/generate",
                data=json.dumps({"model": model, "prompt": "", "keep_alive": "30m"}).encode(),
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=120).read()
            return self._send(200, {"ok": True})
        except Exception as e:
            return self._send(502, {"ok": False, "error": str(e)})

    def _chat(self):
        data = _read_json(self)
        model = data.get("model", "")
        message = (data.get("message") or "").strip()
        if not message:
            return self._send(400, {"error": "empty message"})

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": True,
            "keep_alive": "30m",
            # gentle sampling: enough variety to read naturally, not so much it drifts
            "options": {"temperature": 0.7, "top_p": 0.9, "num_predict": 512},
        }
        try:
            req = urllib.request.Request(
                f"{OLLAMA}/api/chat",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
            )
            upstream = urllib.request.urlopen(req, timeout=300)
        except Exception as e:
            return self._send(502, {"error": f"ollama unreachable: {e}"})

        # stream plain-text deltas to the browser as they arrive
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()
        try:
            for raw in upstream:
                raw = raw.strip()
                if not raw:
                    continue
                obj = json.loads(raw)
                piece = obj.get("message", {}).get("content", "")
                if piece:
                    self.wfile.write(piece.encode("utf-8"))
                    self.wfile.flush()
                if obj.get("done"):
                    break
        except (BrokenPipeError, ConnectionResetError):
            pass  # browser navigated away mid-stream; fine


class DualStackServer(ThreadingHTTPServer):
    """Listen on both IPv4 and IPv6 loopback. macOS often resolves `localhost`
    to ::1 (IPv6) in the browser while an IPv4-only bind sits on 127.0.0.1 --
    the page loads but every fetch() fails. Binding dual-stack makes
    http://localhost:PORT work regardless of how the browser resolves it."""
    address_family = socket.AF_INET6

    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


def main():
    try:
        server = DualStackServer(("::", PORT), Handler)
    except OSError:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)  # IPv6 unavailable
    print(f"NCTB demo -> http://localhost:{PORT}  (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
