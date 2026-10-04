# Team Assignments

## 1. Purpose

The **RAG Knowledge Representation & Retrieval Playground** is a single integrated project designed to study how different ways of representing and retrieving the same knowledge affect the evidence available to an LLM and the final RAG answer.

The project uses the same:

**NovaMart Customer & Operations Policy Handbook — 2026 V3**

as the common knowledge source for all teams.

The core research question is:

> **How does the way we represent and retrieve knowledge affect the evidence retrieved for the same question, and how does that evidence affect the final RAG answer?**

The project is therefore **not four independent RAG applications**.

It is one integrated experimentation platform containing four independently developed pipelines that can later be compared using common evaluation and integration layers.

---

# 2. Overall Architecture

The project follows this conceptual flow:

```text
                    SAME NOVAMART SOURCE
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
      TEXT             METADATA          STRUCTURED
        │                  │                  │
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                    KNOWLEDGE GRAPH
```

More accurately, each representation is independently derived from the same source:

```text
                         NovaMart Source
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
     Text Pipeline      Metadata Pipeline    Structured Pipeline
          │                    │                    │
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                         Graph Pipeline
```

Each pipeline follows:

```text
Source
  ↓
Representation
  ↓
Storage / Index
  ↓
Retrieval
  ↓
Evidence[]
```

Later, the shared integration layer connects the pipelines to:

```text
Evidence[]
    ↓
Common Evaluation
    ↓
Common LLM
    ↓
Answer
    ↓
Answer Evaluation
    ↓
Comparison
```

---

# 3. The Four Pipelines

The project currently contains four core pipelines:

```text
pipelines/
├── text/
├── metadata/
├── structured/
└── graph/
```

Each pipeline is a complete vertical slice.

This means the pair does not only build the representation.

The pair owns the complete path:

```text
SOURCE
   ↓
REPRESENTATION
   ↓
STORAGE / INDEX
   ↓
RETRIEVAL
   ↓
EVIDENCE[]
```

The implementation details can differ between pipelines.

---

# 4. Representation, Storage and Retrieval

These are different concepts:

```text
Representation
      ↓
Storage / Index
      ↓
Retrieval
```

### Representation

How the knowledge is organized.

Examples:

```text
Text
Text + Metadata
Structured Data
Knowledge Graph
```

### Storage / Index

How the representation is persisted or made searchable.

Examples:

```text
Text index
Vector index
PostgreSQL
Graph database
```

### Retrieval

How relevant information is found.

Examples:

```text
Keyword
Dense / Semantic
Hybrid
Metadata Filtering
Reranking
SQL
Graph Traversal
```

A storage technology is not automatically a knowledge representation.

For example:

```text
Text Representation
      ↓
Vector Index
      ↓
Semantic Retrieval
```

and:

```text
Structured Representation
      ↓
PostgreSQL
      ↓
SQL Retrieval
```

and:

```text
Graph Representation
      ↓
Graph Store
      ↓
Graph Traversal
```

---

# 5. Team Structure

There are four pairs.

Each pair owns one complete pipeline.

| Pair   | Pipeline            | Folder                  |
| ------ | ------------------- | ----------------------- |
| Pair 1 | Text / Chunked Text | `pipelines/text/`       |
| Pair 2 | Text + Metadata     | `pipelines/metadata/`   |
| Pair 3 | Structured Data     | `pipelines/structured/` |
| Pair 4 | Knowledge Graph     | `pipelines/graph/`      |

The exact pair member names are maintained in the project coordination documents.

---

# 6. Pair Ownership Model

Each pair owns its assigned pipeline end-to-end.

The expected responsibility is:

```text
Understand NovaMart Source
          ↓
Design Representation
          ↓
Build Representation
          ↓
Choose Storage / Index
          ↓
Implement Retrieval
          ↓
Return Evidence[]
          ↓
Test
          ↓
Experiment
          ↓
Document
```

Each pair is responsible for:

* Technical research.
* Representation design.
* Storage/index design.
* Retrieval design.
* Implementation.
* Testing.
* Source traceability.
* Retrieval experiments.
* Failure analysis.
* Pipeline documentation.
* Pull Request preparation.

---

# 7. Pipeline Folder Structure

Each pipeline should follow this structure:

```text
pipelines/<pipeline-name>/
│
├── __init__.py
├── README.md
├── representation.py
├── retriever.py
├── pipeline.py
├── evaluator.py
└── tests/
```

The files have the following responsibilities.

### `representation.py`

Responsible for creating the pipeline's knowledge representation.

### `retriever.py`

Responsible for retrieving relevant information from that representation.

### `pipeline.py`

Responsible for orchestrating the complete pipeline.

Conceptually:

```text
Representation
      ↓
Storage / Index
      ↓
Retriever
      ↓
Evidence[]
```

### `evaluator.py`

Contains pipeline-specific evaluation or helper logic needed to understand the pipeline's behavior.

The common project evaluation framework remains under:

```text
evaluation/
```

### `README.md`

Documents the design, experiments, results and limitations.

### `tests/`

Contains tests for the pipeline.

---

# 8. Pair 1 — Text / Chunked Text

## Ownership

```text
pipelines/text/
```

## Research Question

> **How does a text/chunk-based representation affect the ability to retrieve useful evidence from the NovaMart handbook?**

## Responsibilities

Pair 1 should:

1. Understand the NovaMart source.
2. Extract and clean textual knowledge where appropriate.
3. Design a meaningful chunking strategy.
4. Preserve source traceability.
5. Store/index the resulting text representation.
6. Implement appropriate basic retrieval.
7. Return results using `Evidence`.
8. Test representative questions.
9. Experiment with relevant chunking/retrieval choices.
10. Document findings and limitations.

Conceptually:

```text
NovaMart Handbook
       ↓
Text Extraction
       ↓
Chunking
       ↓
Text Storage / Index
       ↓
Retrieval
       ↓
Evidence[]
```

### Important

Do not assume that a fixed chunk size is automatically correct.

The pair should investigate whether chunk boundaries preserve enough context for retrieval.

If a policy is naturally a coherent unit, that should be considered during chunking decisions.

---

# 9. Pair 2 — Text + Metadata

## Ownership

```text
pipelines/metadata/
```

## Research Question

> **Can explicit metadata help preserve and retrieve contextual constraints that may be difficult to distinguish using text similarity alone?**

Potential metadata supported by the NovaMart source includes:

* Policy area.
* Customer tier.
* Region.
* Product category.
* Effective dates.
* Promotion.
* Seller type.
* Policy/version information.

Only source-supported metadata should be used.

## Responsibilities

Pair 2 should:

1. Understand the source.
2. Identify useful source-supported metadata.
3. Design the text + metadata representation.
4. Decide how metadata should be stored/indexed.
5. Build the representation.
6. Implement appropriate retrieval/filtering.
7. Return `Evidence`.
8. Preserve source traceability.
9. Test representative questions.
10. Investigate cases where metadata can distinguish similar evidence.
11. Document limitations.

Conceptually:

```text
NovaMart Source
      ↓
Text
 +
Metadata
      ↓
Storage / Index
      ↓
Metadata-aware Retrieval
      ↓
Evidence[]
```

### Important distinction

The representation is:

```text
Text + Metadata
```

Using metadata during query processing is a retrieval behavior.

For example:

```text
region = India
customer_tier = Premium
```

may be used as retrieval constraints.

Do not invent metadata merely to improve retrieval.

---

# 10. Pair 3 — Structured Data

## Ownership

```text
pipelines/structured/
```

## Research Question

> **Which NovaMart knowledge becomes easier to represent and retrieve when entities, attributes and relationships are explicitly structured?**

PostgreSQL is the preferred storage technology unless the pair has a documented technical reason to use another solution.

Potential entities include:

* Customer.
* Customer Tier.
* Product.
* Category.
* Manufacturer.
* Seller.
* Policy.
* Promotion.
* Region.
* Order.
* Support Case.

The final schema must be based on the actual NovaMart source.

## Responsibilities

Pair 3 should:

1. Identify naturally structured entities.
2. Identify attributes.
3. Identify relationships.
4. Design the schema.
5. Create the database.
6. Load source-supported data.
7. Preserve source identifiers.
8. Implement appropriate SQL retrieval.
9. Return `Evidence`.
10. Test representative questions.
11. Investigate multi-table and constraint-heavy questions.
12. Document design decisions and limitations.

Conceptually:

```text
NovaMart Source
      ↓
Entities + Attributes + Relationships
      ↓
Relational Schema
      ↓
PostgreSQL
      ↓
SQL Retrieval
      ↓
Evidence[]
```

### Important

Do not turn every sentence in the handbook into a database row.

Represent information that naturally benefits from structured storage.

Do not hardcode benchmark answers into SQL queries.

---

# 11. Pair 4 — Knowledge Graph

## Ownership

```text
pipelines/graph/
```

## Research Question

> **Can explicit relationships and graph traversal improve retrieval for relationship-heavy and multi-hop questions?**

Potential entities include:

* Customer.
* Customer Tier.
* Product.
* Category.
* Manufacturer.
* Seller.
* Policy.
* Promotion.
* Region.
* Order.
* Support Case.
* Escalation Level.

Potential relationships include:

```text
Customer ──HAS_TIER──────> Tier

Customer ──PLACED────────> Order

Order ──CONTAINS─────────> Product

Product ──MANUFACTURED_BY> Manufacturer

Product ──PART_OF────────> Category

Product ──QUALIFIES_FOR──> Promotion

Promotion ──USES─────────> Policy

Policy ──APPLIES_TO──────> Region
```

These are examples only.

The final graph must contain relationships supported by the NovaMart source.

## Responsibilities

Pair 4 should:

1. Identify entities.
2. Identify relationships.
3. Design the graph model.
4. Choose appropriate graph storage.
5. Build the graph.
6. Preserve source identifiers.
7. Implement graph retrieval/traversal.
8. Return `Evidence`.
9. Test one-hop questions.
10. Test two-hop questions.
11. Investigate appropriate multi-hop questions.
12. Document failure cases and limitations.

Conceptually:

```text
NovaMart Source
      ↓
Entities + Relationships
      ↓
Graph Store
      ↓
Graph Retrieval / Traversal
      ↓
Evidence[]
```

### Important

Do not invent relationships simply because they make a query easier.

The graph must represent actual source knowledge.

---

# 12. Phase 1 — Pair-Owned Pipeline

Phase 1 is the implementation phase owned by each pair.

Each pair must make its pipeline usable and queryable:

```text
Source
   ↓
Representation
   ↓
Storage / Index
   ↓
Basic / Native Retrieval
   ↓
Evidence[]
```

The purpose of Phase 1 is to establish a reliable baseline for each representation.

Phase 1 does **not** require every pair to implement every possible retrieval technique.

---

# 13. Phase 2 — Shared Experimentation

After the four pipelines are working, the project moves into cross-pipeline experimentation.

The shared experiment layer can evaluate meaningful combinations such as:

```text
Text
  ×
Keyword

Text
  ×
Dense Retrieval

Text
  ×
Hybrid Retrieval

Metadata
  ×
Dense + Metadata Filtering

Structured
  ×
SQL Retrieval

Graph
  ×
Graph Traversal
```

Potential retrieval techniques across the project include:

* Keyword / BM25.
* Dense / semantic retrieval.
* Hybrid retrieval.
* Metadata filtering.
* Reranking.
* SQL / structured retrieval.
* Graph traversal.

Not every technique must be implemented for every representation.

The project should compare **technically meaningful combinations**, not artificially force the same method onto every pipeline.

---

# 14. Common Evidence Contract

All pipelines must ultimately return:

```python
@dataclass
class Evidence:
    content: str
    source_id: str
    score: float
    metadata: dict[str, Any]
```

The purpose is to make the pipelines compatible with the common integration and evaluation layers.

### `content`

The retrieved information.

### `source_id`

Identifier that allows the evidence to be traced back to the NovaMart source.

### `score`

The retrieval relevance score when the retrieval method provides one.

### `metadata`

Additional source or retrieval information useful for analysis and traceability.

The exact internal representation can differ between pipelines.

The output contract must remain compatible.

---

# 15. Evaluation

Evaluation is shared at the project level.

The common evaluation code belongs under:

```text
evaluation/
```

Pairs may have pipeline-specific evaluation helpers under their own:

```text
pipelines/<pipeline>/evaluator.py
```

but they should not create competing evaluation frameworks.

The evaluation flow is:

```text
Question
   ↓
Expected Evidence / Source IDs
   ↓
Pipeline Retrieval
   ↓
Retrieved Evidence[]
   ↓
Retrieval Evaluation
   ↓
Common LLM
   ↓
Answer
   ↓
Answer Evaluation
```

Potential retrieval metrics include:

* Recall@K.
* Precision@K.
* MRR.
* nDCG@K where appropriate.
* Retrieval latency.
* Evidence coverage.

The appropriate metrics depend on the experiment.

---

# 16. Development Questions vs Official Benchmark

The official benchmark contains:

```text
40 evaluation questions
40 ground-truth entries
```

These questions are the controlled basis for formal comparison.

However, pairs should not develop only against those questions.

During development, teams may create additional questions to test:

* Edge cases.
* Unseen questions.
* Failure cases.
* Boundary conditions.
* Representation-specific behavior.

The distinction is:

```text
Development
    ↓
Open-ended experimentation
    ↓
Pipeline improvement

Formal Evaluation
    ↓
Same 40 benchmark questions
    ↓
Fair comparison
```

The benchmark must not be changed to improve results.

---

# 17. Failure Analysis

Failures are important experimental results.

Examples include:

```text
Wrong policy version
Wrong region
Wrong customer tier
Similar but incorrect policy
Missed exception
Incomplete relationship
Irrelevant evidence
Insufficient evidence
Poor chunking
Missing metadata
Incorrect entity modeling
Incorrect relationship modeling
```

Important failures should be documented as:

```text
Query
  ↓
Expected Evidence
  ↓
Retrieved Evidence
  ↓
What went wrong?
  ↓
Why did it happen?
  ↓
What could improve it?
```

Do not hide failures.

The project is specifically designed to understand why retrieval succeeds or fails.

---

# 18. Common LLM

The final project uses a common LLM layer.

The common LLM belongs to:

```text
llm/
```

Individual pairs should not build separate final applications or separate LLM pipelines.

The pair's responsibility ends at:

```text
Evidence[]
```

The integrated flow is:

```text
Pipeline
   ↓
Evidence[]
   ↓
Common LLM
   ↓
Answer
```

This allows the project to investigate whether different retrieved evidence leads to different answer quality.

---

# 19. Integration Ownership

The integration layer belongs to the project lead/shared implementation.

Relevant areas include:

```text
integration/
llm/
evaluation/
app/
```

The integration layer will eventually handle:

* Pipeline registration.
* Running selected pipelines.
* Running experiments.
* Passing queries to pipelines.
* Collecting `Evidence[]`.
* Common evaluation.
* Sending evidence to the common LLM.
* Comparing results.
* Producing final application output.

Pairs should not create their own competing integration system.

---

# 20. Final Application

The final application lives under:

```text
app/
```

The application is shared.

The goal is to provide a simple experimentation interface where the same question can be evaluated through different pipelines.

Conceptually:

```text
User Question
      ↓
Run Comparison
      ↓
┌───────────────┐
│ Text          │
│ Metadata      │
│ Structured    │
│ Graph         │
└───────────────┘
      ↓
Evidence Comparison
      ↓
Common LLM
      ↓
Answer Comparison
```

The final application should make the retrieved evidence visible rather than showing only the final answer.

---

# 21. Shared Areas

The following are shared project areas:

```text
data/
shared/
evaluation/
integration/
llm/
app/
docs/
```

Do not modify these areas casually.

In particular, coordinate with the project lead before changing:

```text
shared/schemas.py
shared/interfaces.py
shared/config.py
data/
evaluation/
integration/
llm/
app/
```

A change to shared infrastructure can affect every pipeline.

---

# 22. What Each Pair Must NOT Modify

Without discussion with the project lead, pairs must not:

* Modify the NovaMart source.
* Modify normalized source data.
* Modify official benchmark questions.
* Modify ground truth.
* Change the common Evidence contract.
* Change shared interfaces.
* Modify another pair's pipeline.
* Create a separate application.
* Create a separate benchmark.
* Hardcode benchmark answers.
* Invent source knowledge.
* Add unnecessary dependencies.
* Redesign the project architecture.

If a legitimate requirement requires a shared change, raise it with the project lead first.

---

# 23. Git Workflow

All team members work from the same GitHub repository.

Do not download a ZIP and work as an isolated project.

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd rag-knowledge-representation-playground
```

Synchronize with `main`:

```bash
git checkout main
git pull origin main
```

Create a feature branch.

Examples:

```bash
git checkout -b feature/text-pipeline
```

```bash
git checkout -b feature/metadata-pipeline
```

```bash
git checkout -b feature/structured-pipeline
```

```bash
git checkout -b feature/graph-pipeline
```

Work inside the assigned pipeline.

Commit focused changes:

```bash
git add .
git commit -m "Implement text pipeline"
```

Push:

```bash
git push -u origin feature/<your-feature>
```

Create a Pull Request into:

```text
main
```

---

# 24. Pull Request Requirements

The Pull Request should explain:

* What was implemented.
* Why the representation was chosen.
* Why the storage/index was chosen.
* Why the retrieval method was chosen.
* How evidence is generated.
* How source traceability works.
* What was tested.
* What experiments were performed.
* What was learned.
* Known limitations.
* Representative failure cases.

Before requesting review:

```text
[ ] Work is inside assigned pipeline
[ ] Common dataset unchanged
[ ] Official benchmark unchanged
[ ] No hardcoded answers
[ ] Evidence contract followed
[ ] Source traceability works
[ ] Representation documented
[ ] Storage/index documented
[ ] Retrieval documented
[ ] Tests added
[ ] Tests pass
[ ] Experiments documented
[ ] Failure cases documented
[ ] README updated
[ ] Dependencies justified
[ ] No unrelated changes
[ ] Both pair members understand the implementation
```

---

# 25. Definition of Done

A pair's Phase 1 work is complete when:

```text
Research
   ↓
Design
   ↓
Representation
   ↓
Storage / Index
   ↓
Retrieval
   ↓
Evidence[]
   ↓
Tests
   ↓
Experiments
   ↓
Failure Analysis
   ↓
Documentation
   ↓
Pull Request
   ↓
Review
   ↓
Integration
```

Both pair members should be able to answer:

> What did we build?

> Why did we choose this representation?

> Why did we choose this storage/index?

> Why did we choose this retrieval method?

> How is evidence generated?

> How is evidence traced to the source?

> Which questions does it handle well?

> Where does it fail?

> Why does it fail?

> What did we learn?

---

# 26. Final Team Principle

We are **not building four unrelated RAG systems**.

We are building one controlled experimentation playground.

The same NovaMart knowledge and the same benchmark questions must pass through different pipelines.

The central comparison is:

```text
Knowledge Representation
          ×
Retrieval Strategy
          ↓
Retrieved Evidence
          ↓
Evidence Evaluation
          ↓
Common LLM
          ↓
Answer
          ↓
Answer Evaluation
          ↓
Comparison
```

The goal is not to prove:

> "Our pipeline is the best."

The goal is to discover:

> **Which representation and retrieval approaches work well for which types of questions, where they fail, and why.**

---

# 27. Golden Rule

> **Each pair owns its pipeline from Source → Representation → Storage / Index → Retrieval → Evidence[].**

> **The project lead/shared layer owns cross-pipeline experimentation, common evaluation, the common LLM, comparison, integration, and the final application.**
