# Results — fine-tuning improves small models, and the gain scales

**Setup.** Closed-book QA: each model answers a physics question with no
retrieved context. Test set = 275 held-out questions, stratified by chapter,
**never seen in training** (train/val/test disjoint by question id, seed=42).
Each model evaluated **raw** (base weights) and **fine-tuned** (LoRA on our NCTB
dataset), identical decoding. Metrics: **Token F1** and **BERTScore**
(multilingual, both deterministic), plus **Accuracy** — an automatic
LLM-as-a-judge score (MT-Bench protocol) that marks each answer correct/incorrect
vs gold — reported to corroborate the deterministic metrics.

## Main table (n=275)
| Model | Params | Acc raw | Acc ft | Δ Acc | F1 raw | F1 ft | BERT raw | BERT ft |
|-------|--------|---------|--------|-------|--------|-------|----------|---------|
| Qwen3-0.6B | 0.6B | 0.0%  | 5.5%  | +5.5  | 0.216 | 0.278 | 0.696 | 0.750 |
| Qwen3-1.7B | 1.7B | 10.5% | 25.5% | +15.0 | 0.227 | 0.299 | 0.706 | 0.765 |
| Qwen3-4B   | 4B   | 27.6% | 50.9% | +23.3 | 0.252 | 0.350 | 0.722 | 0.782 |

## Findings
1. **Fine-tuning wins every metric at every size** — no exceptions.
2. **The improvement grows with model capacity** (Δ accuracy +5.5 → +15.0 →
   +23.3pp). The dataset helps more as the model is better able to absorb it.
3. **Absolute accuracy also scales** — raw 0→10.5→27.6%, fine-tuned
   5.5→25.5→50.9%. The 4B fine-tune reaches a genuinely useful **50.9%**
   closed-book, i.e. an offline Bangla physics tutor.
4. **Qualitative:** raw 0.6B produces degenerate/looping text (≈0% correct);
   raw 1.7B/4B are coherent, so their ~2× accuracy gains reflect real *content*
   the dataset teaches, not just answer formatting.

## Methodology notes (for reviewers)
- **No leakage:** the split is frozen and asserted disjoint (train/val/test have
  no shared question ids); `stats.py`/`verify.py` re-check this at run time.
- **Accuracy grading:** an automatic LLM-as-a-judge (MT-Bench protocol) scored
  each of the 6×275 answers as correct iff it conveyed the gold answer's key
  fact; Token F1 and BERTScore are the deterministic metrics and Accuracy
  corroborates them — all three move the same direction at every size.
- **Reproducibility:** all predictions in `../predictions/`, data + split in
  `../dataset/`, training/eval/grading scripts in `../scripts/`.
