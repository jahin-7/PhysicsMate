"""Deterministic evaluation of a predictions file.

Usage:
    python evaluate.py models/qwen4b/ft.jsonl

Prints Token F1 and BERTScore for that file. These are fully reproducible —
running this on the same predictions always gives the same numbers. (Accuracy is
a separate LLM-judge metric; see README.)

Predictions file = one JSON object per line with fields: id, question, gold, pred.
"""
import json, re, sys
from collections import Counter

BANGLA = re.compile(r"[a-zA-Z0-9]+|[ঀ-৿]+")   # same tokenizer as the BM25 index


def token_f1(pred, gold):
    p, g = BANGLA.findall(pred), BANGLA.findall(gold)
    if not p or not g:
        return float(p == g)
    overlap = sum((Counter(p) & Counter(g)).values())
    if overlap == 0:
        return 0.0
    prec, rec = overlap / len(p), overlap / len(g)
    return 2 * prec * rec / (prec + rec)


def evaluate(path):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    preds = [r["pred"] for r in rows]
    golds = [r["gold"] for r in rows]
    f1 = sum(token_f1(p, g) for p, g in zip(preds, golds)) / len(rows)

    from bert_score import score
    # bert-score's version calls a method removed in this transformers; patch it back.
    from transformers.models.bert.tokenization_bert import BertTokenizer
    if not hasattr(BertTokenizer, "build_inputs_with_special_tokens"):
        def _b(self, a, b=None):
            cls, sep = [self.cls_token_id], [self.sep_token_id]
            return cls + a + sep if b is None else cls + a + sep + b + sep
        BertTokenizer.build_inputs_with_special_tokens = _b
    _, _, F = score(preds, golds, model_type="bert-base-multilingual-cased", lang="bn", verbose=False)
    bert = float(F.mean())
    return {"n": len(rows), "token_f1": round(f1, 4), "bertscore": round(bert, 4)}


if __name__ == "__main__":
    path = sys.argv[1]
    m = evaluate(path)
    print(f"{path}")
    print(f"  n = {m['n']}")
    print(f"  Token F1   = {m['token_f1']:.4f}")
    print(f"  BERTScore  = {m['bertscore']:.4f}")
