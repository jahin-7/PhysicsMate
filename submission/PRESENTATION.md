# PhysicsMate — 10-Minute Presentation
### Slide-by-slide outline · target 10:00 total

> Keep it to **10 slides**. One idea per slide. Timings in brackets add to ~10 min.
> Speaker notes are the plain lines under each slide — say them, don't read the slide.

---

### Slide 1 — Title  ⏱ 0:30
**PhysicsMate: Curriculum-Grounded Bengali Physics QA with Small Language Models**
NCTB Grade 9–10 · Team names · Date
> "We built a Bengali physics tutor small enough to run offline on a laptop, and
> studied how much fine-tuning helps at three model sizes."

---

### Slide 2 — The problem  ⏱ 1:00
- Bengali ≈ 230M speakers, tiny presence in educational NLP
- No curriculum-specific Bengali physics QA resource
- Target users (BD classrooms) often have **no reliable internet / weak hardware**
> "So the constraint isn't just accuracy — it's *offline, on cheap hardware*."

---

### Slide 3 — Research question  ⏱ 0:45
> *Can a small, curriculum-grounded dataset teach a small model enough Bengali
> physics to be useful offline — and how does the benefit scale with size?*
- Two outputs: a **benchmark** + a **deployable model**

---

### Slide 4 — Data pipeline  ⏱ 1:15
NCTB book scans → vision OCR → clean Markdown → **811 chunks (13 chapters)**
→ **Knowledge graph: 1,760 nodes / 2,600 edges** → **1,834 QA pairs**
→ split **1374 / 185 / 275** (seed 42, held-out test)
> "Every QA pair is anchored to a graph node, so answers are traceable to a
> curriculum location. The test set is never seen in training."

---

### Slide 5 — Method  ⏱ 1:00
- **LoRA fine-tuning** of 4-bit **Qwen3** at **0.6B / 1.7B / 4B**
- **Closed-book** (no retrieval) → isolates what the *dataset* teaches
- Only small adapters trained → feasible on one consumer machine
> "Closed-book is deliberate: it's the cleanest test of the dataset's value."

---

### Slide 6 — Headline result  ⏱ 1:30  *(the money slide)*
**Fine-tuning wins at every size — and the gain grows with size:**

| Model | Accuracy raw → FT | Δ |
|-------|------------------|---|
| 0.6B | 0.0% → 5.5% | +5.5 pp |
| 1.7B | 10.5% → 25.5% | +15.0 pp |
| 4B | 27.6% → 50.9% | **+23.3 pp** |

> "Same dataset, bigger model, bigger payoff — capacity lets the model absorb
> more of what we taught it." (Show `figs/scaling.png` here.)

---

### Slide 7 — It's honest & reproducible  ⏱ 0:45
- Token-F1 + BERTScore are **deterministic** — `verify.py` re-derives & asserts them
- Accuracy = LLM-judge (MT-Bench protocol) to corroborate
- n = 275, one fixed judge prompt for all 6 variants
> "One command reproduces every deterministic number in the paper."

---

### Slide 8 — Deployment (live demo)  ⏱ 1:30
- Each model → **Q4_K_M GGUF** (0.4 / 1.1 / **2.5 GB**) → Ollama, **fully offline**
- Live web app: switch 0.6B ↔ 1.7B ↔ 4B, streaming, Bangla/English
> **DEMO:** ask one question, switch model sizes, show quality climbing with size.
> (Have it pre-warmed on 4B. 30-second demo, not more.)

---

### Slide 9 — Also built: hybrid RAG  ⏱ 0:45
- BM25 + dense (BGE-M3) + graph → RRF, with dedup / verifier / refusal gate
- Fine-tuned 4B reaches **parity with RAG** on a leakage-free subset
> "Adaptation can reduce dependence on retrieval at inference time."

---

### Slide 10 — Takeaways & future  ⏱ 0:30
- A reusable **Bengali curriculum QA benchmark** (1,834 QA, KG-grounded)
- Fine-tuning helps at every size; **payoff scales with capacity**
- **Offline, 2.5 GB** deployment for real classrooms
- Next: HSC (11–12) via the KG bridge; human-rated test set
> "Thank you — questions?"

---

## Delivery tips
- **Rehearse to 9:00** so Q&A/overruns fit in 10.
- Slides 4 + 6 + 8 are the core; if you're short on time, compress 2, 7, 9.
- The **live demo (Slide 8)** is the memorable moment — practise it so it can't
  fail (models pre-warmed, `start.command` already running before you present).
- One figure per data slide: `figs/scaling.png` (Slide 6), `figs/nodetype.png`
  (optional on Slide 4).
