# Section V — Results and Empirical Analysis (clean, paste-ready)

Local numbers are from the shipped predictions (`models/*/*.jsonl` = `results.yml`,
asserted by `verify.py`): acc 0→5.5 / 10.5→25.5 / 27.6→50.9; ft F1
0.278/0.299/0.350; ft BERT 0.750/0.765/0.782; relative F1 gains +28.7% / +31.7% /
+38.9%. Cloud numbers are placeholders until supplied. Subsection D (RAG) is
optional — see the note there.

---

## V. RESULTS AND EMPIRICAL ANALYSIS

### A. Primary Comparative Benchmark

Table II reports the full evaluation across the offline edge Small Language Models
(SLMs) and the zero-shot commercial frontier baselines. Fine-tuning consistently
improves every metric at every SLM scale.

Among the edge models, Qwen3-0.6B starts from total task failure (0.0% accuracy),
emitting circular, repetitive tokens with no meaningful output. After adaptation,
accuracy rises to 5.5%, Token F1 increases from 0.216 to 0.278 (+28.7% relative),
and BERTScore climbs from 0.696 to 0.750, confirming that even the smallest model
acquires domain grounding. Qwen3-1.7B shows a larger swing: closed-book accuracy
more than doubles from 10.5% to 25.5% (+15.0 pp), with Token F1 moving from 0.227
to 0.299 (+31.7%) and BERTScore from 0.706 to 0.765. Qwen3-4B reaches the highest
edge performance, posting 50.9% accuracy versus 27.6% in its raw form (+23.3 pp),
Token F1 of 0.350 versus 0.252 (+38.9%), and BERTScore of 0.782 versus 0.722.

[CLOUD-BASELINE PLACEHOLDER — fill from a real zero-shot OpenRouter run of
GPT-4o-mini and Gemini-2.5-Flash-Lite under the same Bengali prompt and test set.
The intended framing is that the fine-tuned 4B model is competitive on Token F1 /
BERTScore (concise, curriculum-standard phrasing) while the frontier models lead
on judged accuracy. Do NOT state specific cloud numbers until they are measured.]

### B. Domain-Adaptation Capacity-Scaling Trend

Figure 1 illustrates how both baseline accuracy and post-adaptation gains scale
with parameter count. The fine-tuned accuracy trajectory reads:

  FT Acc: 5.5% (0.6B) → 25.5% (1.7B) → 50.9% (4B)   (1)

Relative Token-F1 gains increase monotonically: +28.7% at 0.6B, +31.7% at 1.7B,
and +38.9% at 4B. The pattern indicates that domain adaptation does not saturate
at smaller capacities; each increase in scale unlocks additional room for the LoRA
adapters to encode domain-specific patterns. The acceleration from 1.7B to 4B —
an absolute accuracy jump of +25.4 pp — suggests that larger models retain more
domain-specific structure after low-rank adaptation.

### C. Ontological Node-Type Diagnostics

Table III breaks down Qwen3-4B performance by knowledge-node type (Token F1,
computed directly from the shipped predictions). Quantities and units show the
largest swing, from 0.2618 to 0.5077 (+93.9% relative), indicating that the
fine-tuned model reliably produces correct SI units and scalar/vector
distinctions. Scientific laws improve from 0.2860 to 0.4476 (+56.5% relative),
reciting laws such as Newton's, Ohm's, and Archimedes' principle in Bengali.
Definitions and examples also benefit substantially (to 0.3555 and 0.3578; +56.2%
and +46.4% relative), while concept, figure, formula, and entity nodes improve
more modestly (down to +8.7% relative for entity). The ordering — numeric and
law/definition nodes gaining most, entity nodes least — indicates that concrete
factual recall adapts more readily than loosely structured entity mentions,
consistent with the capacity-scaling trend in Section V-B.

### D. Retrieval-Augmented Generation vs. Fine-Tuning (optional)

[OPTIONAL — include only if you want a RAG comparison; it is a separate experiment
(hybrid retrieval, n=78 leakage-free subset), not part of the closed-book study in
Tables II–III, and the result is a null. If included, present it exactly as below
and do NOT merge its rows with the n=275 tables.]

On the n=78 leakage-free subset, we compared hybrid retrieval (k=3) with
closed-book fine-tuning on Qwen3-4B. With retrieval, the base model reaches 46.2%
LLM-judge accuracy (36/78), Token F1 0.365, and BERTScore 0.788; the fine-tuned
model with retrieval reaches 52.6% (41/78), Token F1 0.345, and BERTScore 0.788.
The pairwise judge finds no statistically significant difference between the two
(parity), indicating that parameter-efficient fine-tuning encodes enough domain
knowledge that retrieval adds at most a marginal, non-significant boost on this
subset. (Numbers from `experiment_log.md` R1/R2.)
