# Conference Paper — NCTB Bangla Physics QA

Everything needed for the paper: the dataset, the per-model predictions, the
evaluation scripts that reproduce every number, and the write-up docs.

## Reproduce every number with one command
```bash
python verify.py
```
Recomputes Token F1 + BERTScore for all 6 models and the dataset statistics, and
asserts they match `results.yml` / `stats.yml`. Prints `ALL CHECKS PASS ✅`.
(Needs: `pip install bert-score pyyaml transformers torch`.)

## Results (held-out test set, n=275)
| Model | Token F1 raw→ft | BERTScore raw→ft | Accuracy raw→ft (LLM-judge) |
|-------|-----------------|------------------|-----------------------------|
| Qwen3-0.6B | 0.216 → 0.278 | 0.696 → 0.750 | 0.0% → 5.5% |
| Qwen3-1.7B | 0.227 → 0.299 | 0.706 → 0.765 | 10.5% → 25.5% |
| Qwen3-4B   | 0.252 → 0.350 | 0.722 → 0.782 | 27.6% → 50.9% |

Fine-tuning on the dataset wins every metric at every size, and the gain grows
with model size. Token F1 & BERTScore are deterministic (reproduced exactly by
the scripts); Accuracy is an automatic LLM-as-a-judge score under a single fixed
prompt (`JUDGE_PROMPT.md` / `grade.py`), reported to corroborate the deterministic
metrics.

## Contents
```
data/          closed-book SFT data + frozen split ids (train/val/test = 1374/185/275)
dataset_src/   source corpus (queries.json, graph.json, dataset.json)
models/qwen{0.6b,1.7b,4b}/
    raw.jsonl  ft.jsonl              275 held-out predictions each
    <model>.Q4_K_M.gguf  Modelfile   the fine-tuned model (runnable in Ollama)
    adapter/                          the LoRA adapter (base + this = full model)
evaluate.py    python evaluate.py <preds.jsonl>  → Token F1 + BERTScore (deterministic)
grade.py       python grade.py <preds.jsonl>     → LLM-as-a-judge Accuracy (fixed prompt)
JUDGE_PROMPT.md  the exact grading prompt put to the judge (also embedded in grade.py)
stats.py       recompute dataset stats  (python stats.py --check)
verify.py      reproduce & check EVERY deterministic number
results.yml    reported per-model metrics
stats.yml      reported dataset numbers
docs/
  dataset_stats.md         corpus numbers (Data Construction section)
  experiment_log.md        the E1–E6 results table
  scaling_results.md       full results + methodology
```

## Write the paper in this order (mentor's rule)
Data Construction → Experiments & Results → **Introduction (last)** → Related Work.

## The trained models
Each `models/<m>/` folder contains the fine-tuned model: a `.gguf` (Q4_K_M,
runnable in Ollama) plus the LoRA `adapter/` (base model + this = the full
fine-tune). To run one:
```bash
cd models/qwen4b
ollama create nctb-4b -f Modelfile     # Modelfile: FROM ./qwen3-4b.Q4_K_M.gguf
ollama run nctb-4b
```
(The models are not needed to reproduce the numbers — predictions + scripts suffice.)

## Repository notes

**Model binaries are not in this repo.** The `.gguf` files (0.4/1.1/2.5 GB) and
the LoRA `adapter/*.safetensors` exceed GitHub's file-size limit and are excluded
via `.gitignore`. Rebuild them from the training scripts, or download them from
the repo's **Releases** page / a Hugging Face mirror (link once uploaded).

**Data provenance.** The dataset is derived from the NCTB Grade 9–10 Physics
textbook (© NCTB) and is shared here for non-commercial research and educational
use only. The QA pairs, knowledge graph, and code are the authors' own work.
