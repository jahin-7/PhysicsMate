# Section VI — Discussion and Qualitative Case Analysis (clean, paste-ready)

Local numbers from shipped predictions (`results.yml`, n=275). Deployment numbers
(~25 tok/s, ~3.5 GB) measured on this machine (Apple M4, Ollama/llama.cpp). Cloud
numbers used verbatim from the text you provided (not verified by us). Table V is
built from real Qwen3-4B outputs (ids verified in the test set); Bengali is shown
with an English gloss (typeset the Bengali with XeLaTeX).

---

## VI. DISCUSSION AND QUALITATIVE CASE ANALYSIS

The core tension in our results is accuracy versus accessibility. The fine-tuned
Qwen3-4B reaches 50.9% closed-book LLM-judge accuracy, while the frontier cloud
model Gemini-2.5-Flash-Lite reaches 82.91% (zero-shot). The cloud models require
stable internet and per-token billing; the fine-tuned 4B model runs entirely
offline. Quantized to a 2.3 GB Q4_K_M GGUF, the fine-tuned model sustains roughly
25 tokens per second with an approximately 3.5 GB resident memory footprint (2.3 GB
weights plus KV cache) on a consumer Apple M4 laptop, measured via
llama.cpp/Ollama — comfortably interactive and well within an 8 GB machine,
enabling offline classroom deployment without internet infrastructure. (Throughput
on commodity x86 CPUs will be lower and should be measured on the target device.)

### A. Qualitative Analysis and Failure Modes

Table V gives representative case studies. Zero-shot base models fail in three
recurring ways that fine-tuning corrects. (1) Factual hallucination: on positron
decay (ch13_q045) the base model invents that "a positron is a modern version of
the proton" and never names the emitted neutrino, whereas the fine-tuned model
answers exactly — "a positron and a neutrino are emitted." (2) Wrong physical
property with verbose padding: for an object between a convex lens and its focus
(ch09_q084) the base model calls the image "real" (it is virtual) and pads with
irrelevant bullets, while the fine-tuned model gives the correct, concise
"virtual, erect, and magnified." (3) Incomplete derivation: asked to express power
via current and resistance (ch11_q031) the base model recites V = IR but never
reaches the target, while the fine-tuned model returns P = I²R directly.

Fine-tuning thus enforces concise, curriculum-standard terminology and direct
algebraic answers. By contrast, frontier models produce strong reasoning but often
over-explain or introduce Bengali-terminology inconsistencies.

Cross-referencing the per-type F1 in Table III, the smallest fine-tuning gains
fall on entity and figure nodes (+0.021 and +0.057 F1), while the largest fall on
quantity and scientific-law nodes (+0.246 and +0.162 F1, reaching 0.508 and
0.448). This indicates that concrete, well-structured facts (units, named laws)
adapt most readily, whereas loosely structured entity mentions adapt least.

A model that is correct roughly half the time (50.9%, i.e. wrong 49.1% of the
time) carries real pedagogical risk. We therefore scope the system as a
supplementary study aid rather than an authoritative tutor, and recommend
topic-gating to the categories where fine-tuning is strongest (quantities and
scientific laws) together with answer-confidence flagging for classroom use.

---

## Table V (real Qwen3-4B outputs; English gloss)

```
ch13_q045 — Positron decay: which particles are emitted?
  Gold : a positron and a neutrino (a proton converts to a neutron).
  Base : hallucinates ("a positron is a modern version of the proton"); omits neutrino. [WRONG]
  FT   : "a positron and a neutrino are emitted." [CORRECT, concise]

ch09_q084 — Object between a convex lens and its focus: image properties?
  Gold : virtual, erect, magnified.
  Base : says image is "real", adds irrelevant bullets. [WRONG property]
  FT   : "virtual, erect, and larger than the object." [CORRECT]

ch11_q031 — Express power via current and resistance (Ohm's law)?
  Gold : P = I²R (dissipated as heat in the resistor).
  Base : states V = IR but never derives power. [INCOMPLETE]
  FT   : "P = I²R (or P = V²/R)." [CORRECT]
```
(Bengali originals are in `models/qwen4b/{raw,ft}.jsonl` for these three ids;
render them with XeLaTeX + a Bengali font if the table should show Bangla.)
