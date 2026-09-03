# NCTB Physics — Fine-tuned Model Demo

A local, offline chat app for demoing the three fine-tuned Qwen3 models
(0.6B / 1.7B / 4B) from the paper. Ask a Bangla physics question, switch models
live, and watch the answers change with model size.

## Run it

**Easiest:** double-click **`start.command`**. It starts Ollama, makes sure the
three models exist, serves the page, and opens your browser.

**Manual:**
```bash
python3 server.py        # then open http://localhost:8000
```
(Requires Ollama running and the models created — `start.command` does both.)

Nothing here needs the internet. No pip installs, no build step — the server is
pure Python standard library.

## What it does

- **Model switcher** — 0.6B / 1.7B / 4B, deepest-red tag = largest model. Picking
  one pre-warms it so the first reply is instant. Defaults to 4B (strongest).
- **Streaming replies**, each tagged with the model that wrote it, in one thread —
  so answers from different sizes stack up as a live comparison.
- **Sample questions** (✨) drawn from the paper's held-out test set, plus free
  typing for your own.
- **Settings** (⚙) — System / Light / Dark theme, default model, clear chat.

## Notes

- **Single-shot & closed-book:** each question is sent on its own, with no chat
  history and no system prompt — that's how these models were fine-tuned. Nothing
  is stored between messages.
- **Small models answer poorly on purpose:** 0.6B (and often 1.7B) produce weak or
  garbled Bangla. That's the paper's scaling finding showing up live, not a bug —
  quality climbs with size.

## Files

| File | What |
|------|------|
| `server.py` | stdlib server: serves the page + streams from Ollama |
| `index.html` | the whole frontend (self-contained, offline) |
| `samples.json` | curated questions from the 275-question test set |
| `start.command` | one-click launcher (Ollama + models + server + browser) |

Models live in `../models/qwen{0.6b,1.7b,4b}/` and are served through Ollama as
`nctb-0.6b`, `nctb-1.7b`, `nctb-4b`.
