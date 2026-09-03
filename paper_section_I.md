# Section I — Introduction (clean, paste-ready)

Local numbers from shipped predictions (`results.yml`): acc 0→5.5 / 10.5→25.5 /
27.6→50.9 (Δ +5.5 / +15.0 / +23.3 pp); 4B ft F1 0.350, BERT 0.782. Deployment
~2.3 GB / ~25 tok/s (measured, Apple M4). Cloud F1/BERT used verbatim from your
text. Fig. 1 = the scaling figure (`figs/scaling.png`), regenerated with these
numbers.

---

## I. INTRODUCTION

**a) The Bengali STEM Gap.** Large language models have enabled conversational
question-answering systems in English and Chinese [1], [2]. Bengali, spoken by
over 300 million native speakers, remains underrepresented in LLM research.
Existing Bengali NLP benchmarks target sentiment analysis, news classification,
and commonsense reasoning [3], yet curriculum-aligned STEM datasets for South
Asian languages at the secondary level remain scarce. The absence of structured
physics corpora grounded in national educational standards leaves a widening gap
between model capability and pedagogical need.

**b) Physics-Specific Difficulty.** Secondary physics in Bangladesh follows the
National Curriculum and Textbook Board (NCTB) Grades 9–10 syllabus, spanning 13
chapters of classical mechanics, electromagnetism, optics, and modern physics.
Correct responses demand strict adherence to named scientific laws, precise
definitions with SI units, dimensional analysis, and numerical derivations in
standard Bengali. Off-the-shelf multilingual models fail on these constraints:
they hallucinate dimensional formulas, output colloquial or code-switched text,
and produce repetitive loops on deterministic calculation questions. The
difficulty is not merely linguistic but ontological, requiring structured
internalization of physical relationships that base models lack. Even when
frontier models are accessible via cloud APIs, their infrastructure requirements
exclude the target deployment sites.

**c) The Cloud-Edge Divide.** Cloud-deployed frontier models cannot serve the
institutions that need them most. Many schools in Bangladesh and across the Global
South operate on minimal technology budgets with intermittent or absent internet
connectivity, rendering API-dependent systems nonfunctional. A ~2.3 GB quantized
Small Language Model (SLM) running at interactive speed on a consumer laptop (we
measure roughly 25 tokens per second; commodity CPUs will be slower), with zero
recurring API costs and no network dependency, represents a viable deployment path
for resource-constrained educational settings — yet no such dedicated system
exists for secondary Bengali physics.

**d) PhysicsMate: Contributions.** We present PhysicsMate, an ontology-grounded
benchmark and parameter-efficient domain-adaptation framework for secondary
physics question answering in Bengali. Our approach formalizes the NCTB Grade 9–10
curriculum into a multi-relational knowledge graph, constructs a stratified QA
benchmark, and fine-tunes small language models at multiple parameter scales. This
work makes four primary contributions:

1) **Curriculum-Grounded Knowledge Graph & Benchmark.** We encode the 13-chapter
   NCTB physics syllabus into a multi-relational Knowledge Graph (KG) of 1,760
   ontology nodes across 10 ontological types and 2,600 directed semantic edges.
   This ontology grounds a stratified benchmark of 1,834 QA pairs in formal
   standard Bengali, with a strictly held-out test set (n = 275).

2) **Empirical Capacity-Scaling Trend.** Using Low-Rank Adaptation (LoRA) [4] on
   three Qwen3 scales (0.6B, 1.7B, 4B), we observe monotonic scaling of domain-
   adaptation efficacy: accuracy gains of +5.5 pp → +15.0 pp → +23.3 pp over the
   base models on the held-out test set (Fig. 1). The base Qwen3-0.6B achieves
   0.0% accuracy — factually incorrect on all 275 test questions — while the
   fine-tuned 4B model reaches 50.9%, confirming that domain-adaptation efficacy
   increases with parametric capacity under identical fine-tuning conditions.

3) **Curriculum Grounding vs. Frontier Cloud Models.** The fine-tuned Qwen3-4B
   achieves 0.350 Token F1 and 0.782 multilingual BERTScore, higher than
   Gemini-2.5-Flash-Lite (0.2665 F1, 0.7329 BERTScore) and GPT-4o-mini (0.2388 F1,
   0.7282 BERTScore) on lexical and semantic alignment with NCTB textbook
   terminology. Frontier models achieve higher raw accuracy but produce verbose,
   code-switched outputs that diverge from curriculum-standard phrasing.

4) **Offline Edge-AI Viability.** We export the fine-tuned 4B model to a 2.3 GB
   4-bit quantized GGUF binary that achieves 50.9% accuracy on the held-out test
   set (n = 275). On a separate leakage-free subset (n = 78), the fine-tuned model
   matches retrieval-augmented generation while requiring no external context at
   inference time.

---

## Fig. 1 caption

Fig. 1. Scaling of domain-adaptation gains across model capacities (0.6B, 1.7B,
4.0B). Fine-tuning produces monotonic accuracy improvements
(+5.5 pp → +15.0 pp → +23.3 pp, left axis) with consistent gains in deterministic
Token F1 (right axis) at every scale. (Figure: `figs/scaling.png`.)
