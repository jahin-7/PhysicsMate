# Accuracy grading — the exact judge prompt

Accuracy is an automatic **LLM-as-a-judge** score (MT-Bench protocol). Every one
of the 6 × 275 predictions was graded **CORRECT / INCORRECT** against its gold
answer using the single fixed prompt below, at **temperature 0**. This is the
"question put to the judge" — it is embedded verbatim in `grade.py`
(`JUDGE_PROMPT`) so the grading is fully specified and re-runnable.

## The prompt (Bengali — as used)
```
তুমি একজন কঠোর পদার্থবিজ্ঞান পরীক্ষক।
প্রশ্ন: {question}
সঠিক উত্তর: {gold}
শিক্ষার্থীর উত্তর: {prediction}

শিক্ষার্থীর উত্তরটি কি অর্থগতভাবে সঠিক ও সঠিক উত্তরের সাথে সামঞ্জস্যপূর্ণ?
শুধু একটি শব্দে উত্তর দাও: CORRECT অথবা INCORRECT।
```

## English gloss
```
You are a strict physics examiner.
Question: {question}
Correct answer: {gold}
Student's answer: {prediction}

Is the student's answer semantically correct and consistent with the correct
answer? Answer in one word only: CORRECT or INCORRECT.
```
An answer counts as correct iff it conveys the gold answer's key fact. The judge
returns one token; `CORRECT` → 1, else 0; Accuracy is the mean over the file.

## Reproducing it
```bash
# any strong instruction-following LLM can be the judge; set one backend:
JUDGE_MODEL=<model> OPENAI_API_KEY=<key> python grade.py models/qwen4b/ft.jsonl \
    --out models/qwen4b/ft.verdicts.jsonl
```
Note: Token F1 and BERTScore are deterministic and reproduce **exactly**
(`verify.py`). Accuracy is judge-dependent — the *protocol and prompt* are fixed
and released here, but the number is not asserted bit-for-bit because different
judge models may differ at the margin. It is reported to corroborate the two
deterministic metrics, which move in the same direction at every model size.
