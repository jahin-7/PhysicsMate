# Section VII — Conclusion and Future Work (clean, paste-ready)

Local numbers from shipped predictions (`results.yml`); deployment numbers
measured on Apple M4 (Ollama/llama.cpp). No fabricated figures.

---

## VII. CONCLUSION AND FUTURE WORK

PhysicsMate is an ontology-grounded benchmark and parameter-efficient
fine-tuning framework for secondary-school physics in Bengali. We constructed a
knowledge graph of 1,760 nodes across 10 ontological types with 2,600 edges,
paired with 1,834 question–answer pairs. Fine-tuning yielded monotonic accuracy
gains at every scale: Qwen3-0.6B from 0.0% to 5.5%, Qwen3-1.7B from 10.5% to
25.5%, and Qwen3-4B from 27.6% to 50.9%. The 4B model quantizes to a 2.3 GB
Q4_K_M GGUF and generates at roughly 25 tokens per second with a ~3.5 GB memory
footprint on a consumer Apple M4 laptop, enabling fully offline deployment.

### A. Future Work

Four directions follow. First, integrating visual reasoning over physics diagrams
(ray diagrams, free-body sketches, circuit schematics) that the current text-only
pipeline cannot process. Second, augmenting the model with a calculator tool to
handle arithmetic, addressing the calculation errors observed on formula-heavy
questions without additional training. Third, expanding to chemistry and biology
under the same NCTB ontology framework. Fourth, validating the LLM-as-judge metric
against human expert evaluation with inter-annotator agreement reporting.
