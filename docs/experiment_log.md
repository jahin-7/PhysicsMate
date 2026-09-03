# Experiment log — NCTB Bangla Physics QA (small-model dataset paper)

Fill the Accuracy/F1/BERT columns as each run finishes (step 4 appends them to
`results_tables.csv`; copy them here for the paper). **Closed-book** = no
retrieval, pure model knowledge — this is the cleanest test of what the DATASET
teaches. The delta (FT − raw) per model size is the paper's core evidence.

## Primary matrix — closed-book, held-out test (n=275)

| ID | Model | Params | Retrieval | Fine-tuned? | Accuracy | Token F1 | BERTScore | Notes |
|----|-------|--------|-----------|-------------|----------|----------|-----------|-------|
| E1 | Qwen3-0.6B | 0.6B | none | no  | 0.0%  | 0.216 | 0.696 | raw (degenerate/looping output) |
| E2 | Qwen3-0.6B | 0.6B | none | yes | 5.5%  | 0.278 | 0.750 | LoRA, our dataset |
| E3 | Qwen3-1.7B | 1.7B | none | no  | 10.5% | 0.227 | 0.706 | raw |
| E4 | Qwen3-1.7B | 1.7B | none | yes | 25.5% | 0.299 | 0.765 | LoRA, our dataset |
| E5 | Qwen3-4B | 4B | none | no  | 27.6% | 0.252 | 0.722 | raw |
| E6 | Qwen3-4B | 4B | none | yes | 50.9% | 0.350 | 0.782 | LoRA, our dataset |

Token F1 and BERTScore are the deterministic, reproducible metrics. Accuracy is
an automatic LLM-as-a-judge score (MT-Bench protocol: an answer is correct iff it
conveys the gold's key fact), reported to corroborate them; all 6×275 answers were
scored by the judge under an identical prompt. **Fine-tuning wins all three
metrics at every size.**

**Delta table (the headline evidence):**

| Model | Accuracy raw → FT | Δ Acc | Δ F1 | Δ BERTScore |
|-------|-------------------|-------|------|-------------|
| Qwen3-0.6B | 0.0% → 5.5%   | +5.5pp  | +6.2pp | +5.4pp |
| Qwen3-1.7B | 10.5% → 25.5% | +15.0pp | +7.2pp | +5.9pp |
| Qwen3-4B   | 27.6% → 50.9% | +23.3pp | +9.8pp | +6.0pp |

**Key finding:** the fine-tuning gain *grows with model size* (+5.5 → +15.0 →
+23.3pp accuracy) — the dataset helps more as the model can better absorb it.

## Secondary matrix — RAG (already have 4B; run others locally if time)

| ID | Model | Retrieval | Fine-tuned? | Token F1 | BERTScore | LLM-judge | Notes |
|----|-------|-----------|-------------|----------|-----------|-----------|-------|
| R1 | Qwen3-4B (4-bit, MLX) | hybrid k=3 | no  | 0.365 | 0.788 | 36/78 | leakage-free, n=78 (see reports/clean_eval_report.md) |
| R2 | Qwen3-4B (4-bit, MLX) | hybrid k=3 | yes (answerable-only) | 0.345 | 0.788 | 41/78 | parity; over-refusal fixed by ablation |

> Note on R1/R2: in the RAG setting on a 4-bit base, fine-tuning reached PARITY
> with the base model (not significant). Expect the closed-book + smaller-model
> experiments (E1–E6) to show the real dataset gains — that's the point of this
> matrix.

## Cross-family (optional, strengthens generality)

| ID | Model | Retrieval | Fine-tuned? | Accuracy | Notes |
|----|-------|-----------|-------------|----------|-------|
| L1 | Llama-3.2-1B | none | no  |  |  |
| L2 | Llama-3.2-1B | none | yes |  |  |
| L3 | Llama-3.2-3B | none | no  |  |  |
| L4 | Llama-3.2-3B | none | yes |  |  |
