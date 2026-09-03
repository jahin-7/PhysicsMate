# Abstract (clean, paste-ready)

Numbers from shipped predictions (`results.yml`): closed-book accuracy 0→5.5 /
10.5→25.5 / 27.6→50.9 (n=275). RAG stated as parity only, to avoid mixing the
n=275 closed-book test with the n=78 retrieval subset (the AI draft's "50.9% on
the 78-subset" was wrong — 50.9% is the n=275 number). GGUF 2.3 GB.

---

## Abstract

Bengali remains underrepresented in educational language-model research,
particularly for curriculum-specific science question answering. We present
PhysicsMate, a curriculum-grounded benchmark and parameter-efficient adaptation
framework for secondary-school physics question answering in Bengali, based on the
National Curriculum and Textbook Board (NCTB) Grade 9–10 syllabus. We construct an
ontology-grounded knowledge graph containing 1,760 nodes and 2,600 multi-relational
edges, and use it to organize 1,834 curriculum-aligned question–answer pairs across
13 physics chapters, with a strictly held-out test set of 275 questions. We
evaluate LoRA-based adaptation of 4-bit quantized Qwen3 models at 0.6B, 1.7B, and
4B parameters. Fine-tuning consistently improves closed-book accuracy at every
scale — from 0.0% to 5.5%, 10.5% to 25.5%, and 27.6% to 50.9%, respectively — with
the gain growing with model capacity. On a separate leakage-free retrieval subset,
the fine-tuned 4B model reaches parity with retrieval-augmented generation,
indicating that parametric adaptation can reduce dependence on external retrieval
at inference time. These results show that parameter-efficient adaptation
substantially improves curriculum-specific Bengali physics performance while
enabling offline deployment: the 4B model quantizes to a 2.3 GB GGUF binary that
runs offline on a consumer laptop, providing a practical foundation for
resource-constrained educational settings.

**Index Terms**—Natural Language Processing, Low-Resource Languages, Knowledge
Graphs, Question Answering, Small Language Models, Parameter-Efficient Fine-Tuning,
Retrieval-Augmented Generation, STEM Education, Bengali.
