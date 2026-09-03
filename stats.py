"""Recompute the dataset statistics from source, and write/verify stats.yml.

Usage:
    python stats.py            # prints stats, writes stats.yml if missing
    python stats.py --check    # recompute and assert they match stats.yml

Reads the source corpus in dataset_src/ (queries.json, graph.json, dataset.json)
and the frozen split ids in data/. Every reported dataset number is regenerated
here — nothing is hand-typed.
"""
import json, pathlib, sys
from collections import Counter

HERE = pathlib.Path(__file__).parent
SRC = HERE / "dataset_src"
DATA = HERE / "data"


def compute():
    queries = json.loads((SRC / "queries.json").read_text())["queries"]
    graph = json.loads((SRC / "graph.json").read_text())
    chunks = json.loads((SRC / "dataset.json").read_text())["chunks"]
    n_train = len([l for l in (DATA / "split_train_ids.txt").read_text().splitlines() if l.strip()])
    n_val = len([l for l in (DATA / "split_val_ids.txt").read_text().splitlines() if l.strip()])
    n_test = len([l for l in (DATA / "split_test_ids.txt").read_text().splitlines() if l.strip()])
    chapters = sorted({q["id"].split("_")[0] for q in queries})
    ntypes = Counter(n.get("type", "?") for n in graph["nodes"])
    return {
        "qa_pairs": len(queries),
        "knowledge_nodes": len(graph["nodes"]),
        "graph_edges": len(graph.get("edges", [])),
        "cleaned_chunks": len(chunks),
        "chapters": len(chapters),
        "split_train": n_train,
        "split_val": n_val,
        "split_test": n_test,
        "avg_question_chars": round(sum(len(q["question_bn"]) for q in queries) / len(queries), 1),
        "avg_answer_chars": round(sum(len(q["answer_bn"]) for q in queries) / len(queries), 1),
        "node_types": dict(sorted(ntypes.items(), key=lambda kv: -kv[1])),
    }


def dump_yaml(d):
    out = []
    for k, v in d.items():
        if isinstance(v, dict):
            out.append(f"{k}:")
            for kk, vv in v.items():
                out.append(f"  {kk}: {vv}")
        else:
            out.append(f"{k}: {v}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    s = compute()
    yml = HERE / "stats.yml"
    if "--check" in sys.argv:
        assert yml.exists(), "stats.yml missing — run `python stats.py` first"
        expected = yml.read_text().strip()
        if dump_yaml(s).strip() == expected:
            print("stats.yml: PASS (recomputed values match)")
        else:
            print("stats.yml: FAIL — recomputed values differ from stats.yml"); sys.exit(1)
    else:
        yml.write_text(dump_yaml(s))
        print(dump_yaml(s))
        print("wrote -> stats.yml")
