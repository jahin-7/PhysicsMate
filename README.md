# PhysicsMate — NCTB Bangla Physics QA with Small Language Models

Curriculum-grounded Bengali physics question answering for the NCTB Grade 9–10
syllabus. This repo has everything used to build the system: the dataset, the
per-model predictions, the evaluation scripts that reproduce every number, and an
offline demo that runs the fine-tuned models locally through Ollama.

## Run the models + test questions
See **[`submission/README.md`](submission/README.md)** for the terminal commands
to load all three models in Ollama, launch the offline chat app, and 50+ Bangla
physics test questions.

## Reproduce every number with one command
```bash
python verify.py
```
Recomputes Token F1 + BERTScore for all six models and the dataset statistics, and
checks they match `results.yml` / `stats.yml`. Prints `ALL CHECKS PASS ✅`.
(Needs: `pip install bert-score pyyaml transformers torch`.)

## Results (held-out test set, n = 275)
| Model | Token F1 raw→ft | BERTScore raw→ft | Accuracy raw→ft (LLM-judge) |
|-------|-----------------|------------------|-----------------------------|
| Qwen3-0.6B | 0.216 → 0.278 | 0.696 → 0.750 | 0.0% → 5.5% |
| Qwen3-1.7B | 0.227 → 0.299 | 0.706 → 0.765 | 10.5% → 25.5% |
| Qwen3-4B   | 0.252 → 0.350 | 0.722 → 0.782 | 27.6% → 50.9% |

Fine-tuning wins every metric at every size, and the gain grows with model size.
Token F1 and BERTScore are deterministic (reproduced exactly by the scripts).
Accuracy is an automatic LLM-as-a-judge score under one fixed prompt
(`JUDGE_PROMPT.md` / `grade.py`), reported to corroborate the deterministic metrics.

## Contents
```
data/          closed-book QA + frozen split ids (train/val/test = 1374/185/275)
dataset_src/   source corpus (queries.json, graph.json, dataset.json)
models/qwen{0.6b,1.7b,4b}/
    raw.jsonl  ft.jsonl              275 held-out predictions each
    Modelfile                        Ollama Modelfile (points at the GGUF)
    adapter/adapter_config.json      LoRA adapter config
evaluate.py    python evaluate.py <preds.jsonl>  -> Token F1 + BERTScore
grade.py       python grade.py <preds.jsonl>     -> LLM-as-a-judge Accuracy
JUDGE_PROMPT.md  the exact grading prompt
stats.py       recompute dataset stats  (python stats.py --check)
verify.py      reproduce & check every deterministic number
results.yml    reported per-model metrics
stats.yml      reported dataset numbers
demo/          offline chat app (local server -> Ollama, 3-model switcher)
submission/    how to run the models + 50 test questions
LICENSE-DATA   dataset license (CC BY-NC 4.0)
```

## Running a model directly
```bash
cd models/qwen4b
ollama create nctb-4b -f Modelfile
ollama run nctb-4b
```

## Repository notes
**Model binaries are not in this repo.** The `.gguf` files (0.4 / 1.1 / 2.5 GB)
and the LoRA `adapter/*.safetensors` are over GitHub's file-size limit and are
excluded via `.gitignore`. Rebuild them from training, or download from the repo's
**Releases** page / a Hugging Face mirror.

**Data provenance.** The dataset is derived from the NCTB Grade 9–10 Physics
textbook (© NCTB) and is shared for non-commercial research and educational use
only. The QA pairs, knowledge graph, and code are the authors' own work.

## License
The dataset (`data/` and `dataset_src/`) is licensed under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — see
[`LICENSE-DATA`](LICENSE-DATA). You may share and adapt it for non-commercial
purposes with attribution. The license covers only the authors' contributions;
the underlying NCTB textbook remains © NCTB.
