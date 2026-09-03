"""Reproduce every reported number from the shipped files and check they match.

    python verify.py

- Recomputes Token F1 + BERTScore for all 6 prediction files and asserts they
  equal results.yml (tolerance 0.001).
- Recomputes the dataset statistics and asserts they equal stats.yml.
Prints PASS/FAIL per check and an overall verdict. (accuracy_llm_judge is
LLM-judge, not deterministic, so it is reported but not asserted.)
"""
import pathlib, subprocess, sys, yaml
from evaluate import evaluate

HERE = pathlib.Path(__file__).parent
res = yaml.safe_load((HERE / "results.yml").read_text())
ok = True

print("== metrics (recomputed vs results.yml) ==")
for m in ["qwen0.6b", "qwen1.7b", "qwen4b"]:
    for s in ["raw", "ft"]:
        got = evaluate(HERE / f"models/{m}/{s}.jsonl")
        exp = res[m][s]
        good = abs(got["token_f1"] - exp["token_f1"]) <= 0.001 and abs(got["bertscore"] - exp["bertscore"]) <= 0.001
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {m}/{s}: F1 {got['token_f1']:.3f} (exp {exp['token_f1']}) | "
              f"BERT {got['bertscore']:.3f} (exp {exp['bertscore']}) | acc(judge) {exp['accuracy_llm_judge']}")

print("== dataset stats ==")
r = subprocess.run([sys.executable, str(HERE / "stats.py"), "--check"], capture_output=True, text=True)
print("  " + r.stdout.strip())
if "PASS" not in r.stdout:
    ok = False

print("\n" + ("ALL CHECKS PASS ✅" if ok else "SOME CHECKS FAILED ❌"))
sys.exit(0 if ok else 1)
