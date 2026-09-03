"""grade.py — LLM-as-a-judge Accuracy for a predictions file.

Token F1 and BERTScore are DETERMINISTic and reproduced exactly by evaluate.py /
verify.py. Accuracy is an automatic **LLM-as-a-judge** score (MT-Bench protocol):
each prediction is graded CORRECT / INCORRECT against the gold answer using the
FIXED prompt below, at temperature 0.

The prompt (JUDGE_PROMPT) is the reproducible artifact — it is exactly the
question put to the judge for every one of the 6 x 275 answers. Any sufficiently
strong instruction-following LLM can serve as the judge; the reported numbers were
produced with one such judge under this prompt. Because LLM judging is not
bit-identical across judges, verify.py does NOT assert Accuracy — it is reported
to corroborate the two deterministic metrics.

Usage
-----
  python grade.py models/qwen4b/ft.jsonl
  python grade.py models/qwen4b/ft.jsonl --out models/qwen4b/ft.verdicts.jsonl

Pick ONE judge backend via environment variables:
  OpenAI-compatible:  JUDGE_MODEL=<model>  OPENAI_API_KEY=<key>  [OPENAI_BASE_URL=<url>]
  Google Gemini:      JUDGE_PROVIDER=gemini  JUDGE_MODEL=<model>  GEMINI_API_KEY=<key>

Each input line is JSON with fields: id, question, gold, pred.
Writes per-item verdicts (with --out) and prints Accuracy over the file.
"""
import argparse, json, os, re, sys, time
from collections import Counter

# ------------------------------------------------------------------ the judge
# EXACT prompt used to grade every prediction. Bengali; English gloss in comment.
#   "You are a strict physics examiner.
#    Question: {q}
#    Correct answer: {gold}
#    Student's answer: {pred}
#    Is the student's answer semantically correct and consistent with the correct
#    answer? Answer in one word only: CORRECT or INCORRECT."
def JUDGE_PROMPT(q, gold, pred):
    return (
        "তুমি একজন কঠোর পদার্থবিজ্ঞান পরীক্ষক।\n"
        f"প্রশ্ন: {q}\n"
        f"সঠিক উত্তর: {gold}\n"
        f"শিক্ষার্থীর উত্তর: {pred}\n\n"
        "শিক্ষার্থীর উত্তরটি কি অর্থগতভাবে সঠিক ও সঠিক উত্তরের সাথে সামঞ্জস্যপূর্ণ? "
        "শুধু একটি শব্দে উত্তর দাও: CORRECT অথবা INCORRECT।"
    )

def verdict_from_text(text):
    return 1 if text.strip().upper().startswith("CORRECT") else 0

def judge_openai(q, gold, pred):
    from openai import OpenAI
    cli = OpenAI(base_url=os.environ.get("OPENAI_BASE_URL") or None)
    r = cli.chat.completions.create(
        model=os.environ["JUDGE_MODEL"], temperature=0,
        messages=[{"role": "user", "content": JUDGE_PROMPT(q, gold, pred)}],
    )
    return verdict_from_text(r.choices[0].message.content)

def judge_gemini(q, gold, pred):
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    m = genai.GenerativeModel(os.environ.get("JUDGE_MODEL", "gemini-2.0-flash"))
    for _ in range(4):
        try:
            return verdict_from_text(m.generate_content(
                JUDGE_PROMPT(q, gold, pred),
                generation_config={"temperature": 0}).text)
        except Exception as e:
            print("retry:", e, file=sys.stderr); time.sleep(3)
    return 0

def pick_backend():
    provider = os.environ.get("JUDGE_PROVIDER", "openai").lower()
    if provider == "gemini" and os.environ.get("GEMINI_API_KEY"):
        return judge_gemini
    if provider == "openai" and os.environ.get("OPENAI_API_KEY") and os.environ.get("JUDGE_MODEL"):
        return judge_openai
    return None

# ------------------------------------------------------------- deterministic F1
_BANGLA = re.compile(r"[a-zA-Z0-9]+|[ঀ-৿]+")
def token_f1(pred, gold):
    p, g = _BANGLA.findall(pred), _BANGLA.findall(gold)
    if not p or not g: return float(p == g)
    ov = sum((Counter(p) & Counter(g)).values())
    if ov == 0: return 0.0
    prec, rec = ov / len(p), ov / len(g)
    return 2 * prec * rec / (prec + rec)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("predfile")
    ap.add_argument("--out", help="write per-item verdicts here (jsonl)")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.predfile, encoding="utf-8") if l.strip()]
    f1 = sum(token_f1(r["pred"], r["gold"]) for r in rows) / len(rows)
    print(f"file: {args.predfile}  (n={len(rows)})")
    print(f"Token F1 (deterministic): {f1:.3f}")

    judge = pick_backend()
    if judge is None:
        print("\nAccuracy: SKIPPED — no judge backend configured.")
        print("Set a backend, e.g.:  JUDGE_MODEL=<model> OPENAI_API_KEY=<key> python grade.py " + args.predfile)
        print("The exact grading prompt is JUDGE_PROMPT() in this file (temperature 0).")
        return

    verdicts, correct = [], 0
    for r in rows:
        v = judge(r["question"], r["gold"], r["pred"])
        correct += v
        verdicts.append({"id": r.get("id"), "verdict": "CORRECT" if v else "INCORRECT"})
    acc = correct / len(rows)
    print(f"Accuracy (LLM-as-a-judge): {acc:.3f}  ({correct}/{len(rows)})")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for v in verdicts:
                f.write(json.dumps(v, ensure_ascii=False) + "\n")
        print(f"verdicts -> {args.out}")

if __name__ == "__main__":
    main()
