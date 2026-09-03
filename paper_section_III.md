# Section III — The PhysicsMate Benchmark & Knowledge Graph (clean, paste-ready)

All figures verified against `dataset_src/` + `stats.yml`. Corrections vs the AI
draft: pages 359 (not "330+"); chapter names in D fixed (Ch.6 = Effect of Heat,
Ch.12 = Magnetic Effects of Current — there is no "Vectors" chapter); Fig. 2
formula gain +18% (not +24%). Node-type and edge counts were already correct.

---

## III. THE PHYSICSMATE BENCHMARK & KNOWLEDGE GRAPH

### A. Curriculum Corpus Extraction & Semantic Chunking

PhysicsMate is extracted from the official NCTB secondary physics curriculum,
which covers 13 chapters across 359 pages. We digitized and normalized the source
material, then partitioned it into 811 semantic chunks using topic-boundary
detection rather than fixed-length splitting. Each chunk preserves a
self-contained conceptual unit: mathematical notation, SI-unit conventions, and
cross-references to the 218 textbook figures stay within chunk boundaries. This
coherence matters because downstream RAG systems index chunks independently; a
chunk that splits a derivation across boundaries loses the logical chain a model
needs to answer correctly [18].

### B. Ontological Knowledge Graph Architecture

We model the curriculum as a directed multi-relational Knowledge Graph with 1,760
nodes across 10 ontological types, where each type maps to a retrieval action
(e.g., figures are retrieved for visualization, formulas for calculation). We
derived this taxonomy by analyzing the NCTB chapter structure and collapsing
adjacent types until each mapped to a unique retrieval action [14]:

- **Concept (397 nodes):** fundamental physical principles (e.g., inertia,
  refraction, kinetic energy) forming the backbone of each chapter.
- **Question (252 nodes):** standard conceptual questions embedded in the
  textbook, serving as natural QA seed points.
- **Quantity (224 nodes):** physical quantities with their scalar/vector
  classification, dimensional formulas, and SI units.
- **Figure (218 nodes):** diagrammatic nodes for optical ray paths, circuit
  schematics, and experimental setups.
- **Example (188 nodes):** worked examples and problem solutions from the textbook.
- **Entity (176 nodes):** scientific apparatus, measuring instruments, and
  historical figures referenced in the curriculum.
- **Definition (136 nodes):** formal textbook definitions and postulates.
- **Formula (83 nodes):** algebraic formulations (F = ma, T = 2π√(l/g),
  v = u + at).
- **Law (65 nodes):** named physical laws (e.g., Newton's Laws, Snell's Law,
  Ohm's Law, Hooke's Law).
- **HSC Topic (21 nodes):** bridge topics linking secondary physics to the higher
  secondary curriculum.

These types correspond to four cognitive levels students engage: declarative
recall (definitions, laws), procedural application (formulas, examples), visual
interpretation (figures), and curricular scaffolding (HSC topics).

### C. Semantic Edge Typology

The 2,600 directed edges connecting these nodes carry 30 relational types. Two
relations dominate the graph: part_of (585 edges) captures curricular hierarchy,
linking sub-topics to their parent chapters, and applies_to (531) binds laws and
formulas to the physical situations where they operate. illustrates (361) connects
figures to the concepts they visualize, and example_of (268) links concrete
problems to abstract principles. depends_on (215) encodes prerequisite
relationships between topics, while derived_from (118) traces formula genealogies
back to their source laws. These relations enable multi-hop traversal: a query
about Ohm's Law can follow applies_to to reach relevant circuit quantities, then
illustrates to locate the corresponding schematic figure.

### D. Grounded QA Benchmark & Leakage-Free Splitting

We constructed 1,834 QA pairs in standard formal Bengali, where each question is
grounded in a specific graph node and its source text chunk, linking to
prerequisite concepts, related formulas, and illustrative figures for multi-hop
evidence retrieval [18]. The benchmark covers all 13 curriculum chapters. Chapter 1
(Physical Quantities and Measurement) contains the most pairs (302), reflecting its
density of definitions and unit conversions. Several mid-curriculum chapters —
Effect of Heat (146), Refraction of Light (146), Reflection of Light (144), Motion
(140), and Waves and Sound (140) — cluster around 140–146 pairs, while Chapter 12
(Magnetic Effects of Current) has the fewest (82).

To prevent test-set contamination, we partitioned the corpus into training
(n = 1,374; 74.9%), validation (n = 185; 10.1%), and held-out test (n = 275;
15.0%) sets, stratified by chapter. Each question ID appears in exactly one
partition; we verified this programmatically before any model training. These
splits form the basis for evaluating domain-adaptation efficacy across the three
model scales.

---

## LaTeX — Table I (structural & ontological statistics)

```latex
\begin{table}[t]
\caption{Structural and Ontological Statistics of PhysicsMate}
\label{tab:stats}
\centering
\begin{tabular}{lr@{\hskip 2em}lr}
\toprule
Corpus Dimension & Count & Ontology / Relation & Count\\
\midrule
Curriculum Chapters     & 13    & Concepts (concept)      & 397\\
Clean Text Chunks       & 811   & Questions (question)    & 252\\
Document Figures        & 218   & Quantities (quantity)   & 224\\
Total KG Nodes          & 1{,}760 & Figures (figure)      & 218\\
Total KG Edges          & 2{,}600 & Examples (example)    & 188\\
Total QA Pairs          & 1{,}834 & Entities (entity)     & 176\\
Train Set (74.9\%)      & 1{,}374 & Definitions (definition) & 136\\
Validation Set (10.1\%) & 185   & Formulas (formula)      & 83\\
Held-Out Test (15.0\%)  & 275   & Scientific Laws (law)   & 65\\
Avg. Question Length    & 50.3 ch & HSC Topics (hsc\_topic) & 21\\
Avg. Answer Length      & 117.2 ch & Top edge: part\_of / applies\_to & 585 / 531\\
\bottomrule
\end{tabular}
\end{table}
```

## Fig. 2 caption

Fig. 2. Token F1 by knowledge node type, base vs. fine-tuned Qwen3-4B.
Fine-tuning delivers the largest gains on structured quantities (+93.9%) and
scientific laws (+56.5%), and the smallest on entity nodes (+8.7%).
(Figure: `figs/nodetype.png`.)
