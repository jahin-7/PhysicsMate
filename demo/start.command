#!/bin/bash
# Double-click this file (or run it) to launch the NCTB physics model demo.
# It makes sure Ollama is running, the 3 fine-tuned models exist, then serves
# the page and opens it in your browser. Fully local.
cd "$(dirname "$0")"

echo "▶ NCTB পদার্থবিজ্ঞান demo"

# 1. Ollama running?
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "  · starting Ollama…"
  (ollama serve >/dev/null 2>&1 &)
  for i in $(seq 1 30); do
    curl -s http://localhost:11434/api/tags >/dev/null 2>&1 && break
    sleep 1
  done
fi
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "  ✗ Ollama isn't reachable. Install it from https://ollama.com and try again."
  exit 1
fi

# 2. The 3 fine-tuned models exist? (create from the GGUFs next door if not)
for pair in "qwen0.6b:nctb-0.6b" "qwen1.7b:nctb-1.7b" "qwen4b:nctb-4b"; do
  dir="../models/${pair%%:*}"; name="${pair##*:}"
  if ! ollama list | grep -q "^${name}"; then
    echo "  · creating ${name}…"
    ( cd "$dir" && ollama create "$name" -f Modelfile >/dev/null 2>&1 )
  fi
done
echo "  ✓ models ready: nctb-0.6b, nctb-1.7b, nctb-4b"

# 3. Serve + open
( sleep 1; open http://localhost:8000 ) &
echo "  ▶ http://localhost:8000  (close this window / Ctrl-C to stop)"
python3 server.py
