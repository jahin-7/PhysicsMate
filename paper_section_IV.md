# Section IV — Experimental Methodology (clean, paste-ready)

Local values are from the shipped predictions (`models/*/*.jsonl` = `results.yml`,
asserted by `verify.py`; Table III is computed from the same files, so the tables
agree). Cloud-baseline cells are `TBD` — fill from a real zero-shot run before
submission. Citation numbers ([4], [19], [20]) follow the draft's bibliography.

---

## IV. EXPERIMENTAL METHODOLOGY

### A. Foundation Models and LoRA Fine-Tuning

We fine-tune three scales of the Qwen3 family — 0.6B, 1.7B, and 4B parameters —
chosen to bracket the feasibility boundary for edge inference. The 0.6B model
tests whether a sub-billion model can retain Bengali physics terminology after
low-rank adaptation, while the 4B model approaches the upper bound of what a
consumer GPU can serve at interactive speed under 4-bit quantization. All three
models are loaded in 4-bit NormalFloat (NF4) quantization through the BitsAndBytes
integration within the Unsloth framework, which reduces peak memory enough to
fine-tune every scale on a single free-tier GPU.

We apply LoRA [4] to all seven linear projection layers of each transformer block
(the query, key, value, and output projections of the attention module, and the
gate, up, and down projections of the feed-forward module). Following Biderman et
al., we set rank r = 16, scaling factor α = 32, and dropout p = 0.05, with no bias
terms; the base weights remain frozen and only the adapters are trained (roughly
1.7% of parameters for the 0.6B model). Each training instance is formatted with
the model's chat template under a Bengali pedagogical system prompt, and the loss
is computed only over the answer (response) tokens.

We train for 3 epochs with the 8-bit AdamW optimizer at a learning rate of
2×10⁻⁴ under a cosine schedule (warmup ratio 0.05) and weight decay 0.01. We use a
per-device batch size of 8 with 2 gradient-accumulation steps, giving an effective
batch size of 16, and a maximum sequence length of 512 tokens (closed-book answers
are short). All fine-tuning is performed on a single NVIDIA T4 GPU (free-tier
Colab/Kaggle), and the identical recipe is applied across all three scales so that
the base model is the only independent variable.

### B. Evaluation Protocol and Metrics

All models are evaluated in closed-book mode on the 275 held-out test questions,
drawn from a chapter-stratified, leakage-controlled split (train/validation/test
disjoint by question id). To attribute any observed difference to the adapter
alone, the raw and fine-tuned conditions are served from the same 4-bit base with
the LoRA adapter simply toggled on or off; decoding is greedy (sampling disabled)
and capped at 160 new tokens.

We report three complementary metrics. Token F1 measures word-level lexical
overlap using a Bengali Unicode regex tokenizer. Multilingual BERTScore [19]
provides paraphrase tolerance via cosine similarity in a multilingual embedding
space. Neither metric captures factual correctness, so we additionally report an
LLM-as-a-Judge Accuracy [20]: a binary correctness judge, prompted at temperature
0 under a single fixed rubric, compares each prediction against the gold reference
and marks it correct if and only if it conveys the reference's key fact. Strict
exact match is uninformative in this free-form Bengali setting — it is
approximately 0 for all conditions — so we do not report it. Cloud baselines
(GPT-4o-mini, Gemini-2.5-Flash-Lite) are evaluated zero-shot via OpenRouter under
the same Bengali system prompt and the same test questions as the local models.

---

## LaTeX — Table II (Master benchmark)

```latex
\begin{table}[t]
\caption{Master Benchmark Results on Held-Out Test Set ($n=275$)}
\label{tab:master}
\centering
\begin{tabular}{lccccccc}
\toprule
 & & \multicolumn{2}{c}{Accuracy (\%)} & \multicolumn{2}{c}{Token F1} & \multicolumn{2}{c}{BERTScore}\\
\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(lr){7-8}
Model & Params & Raw & FT & Raw & FT & Raw & FT\\
\midrule
\multicolumn{8}{l}{\textit{Frontier / Commercial Cloud Baselines (Zero-Shot)}}\\
GPT-4o-mini            & $>$8B$^{\ast}$  & \multicolumn{2}{c}{TBD} & \multicolumn{2}{c}{TBD} & \multicolumn{2}{c}{TBD}\\
Gemini-2.5-Flash-Lite  & $>$10B$^{\ast}$ & \multicolumn{2}{c}{TBD} & \multicolumn{2}{c}{TBD} & \multicolumn{2}{c}{TBD}\\
\midrule
\multicolumn{8}{l}{\textit{Edge Small Language Models (Local / Offline)}}\\
Qwen3-0.6B & 0.6B & 0.0  & 5.5  & 0.216 & 0.278 & 0.696 & 0.750\\
Qwen3-1.7B & 1.7B & 10.5 & 25.5 & 0.227 & 0.299 & 0.706 & 0.765\\
Qwen3-4B   & 4.0B & 27.6 & 50.9 & 0.252 & 0.350 & 0.722 & 0.782\\
\bottomrule
\end{tabular}
\end{table}
```

## LaTeX — Table III (4B breakdown by knowledge node type)

```latex
\begin{table}[t]
\caption{Qwen3-4B Token-F1 Breakdown by Knowledge Node Type ($n=275$)}
\label{tab:bytype}
\centering
\begin{tabular}{lcccc}
\toprule
Knowledge Node Type & Count ($n$) & Raw F1 & FT F1 & $\Delta$F1\\
\midrule
Quantity        & 29 & 0.2618 & 0.5077 & +0.2459\\
Scientific Law  &  8 & 0.2860 & 0.4476 & +0.1616\\
Definition      & 28 & 0.2276 & 0.3555 & +0.1279\\
Example         & 35 & 0.2444 & 0.3578 & +0.1134\\
Concept         & 65 & 0.2496 & 0.3424 & +0.0928\\
Figure          & 67 & 0.2634 & 0.3204 & +0.0570\\
Formula         &  8 & 0.2803 & 0.3318 & +0.0515\\
Entity          & 35 & 0.2408 & 0.2618 & +0.0210\\
\bottomrule
\end{tabular}
\end{table}
```
Counts sum to 275; weighted-mean FT F1 = 0.350, matching Table II's 4B row.
