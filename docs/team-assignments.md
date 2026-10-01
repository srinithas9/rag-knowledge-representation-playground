# Team Assignments

## 1. Purpose

The **RAG Knowledge Representation & Retrieval Playground** is a single integrated project designed to study how different ways of representing knowledge and different retrieval strategies affect the evidence retrieved by a RAG system.

The project uses the same **NovaMart Customer & Operations Policy Handbook — 2026 V3** as the common knowledge source for all teams.

The core research question is:

> **How does the combination of knowledge representation and retrieval strategy affect the evidence retrieved for the same question, and how does that evidence affect the final RAG answer?**

The project is therefore **not four independent RAG applications**.

It is one integrated system with multiple representation approaches that can later be compared under a common retrieval and evaluation framework.

---

# 2. Overall Architecture

The complete project follows this conceptual pipeline:

```text
Same NovaMart Source
        ↓
Parse / Normalize
        ↓
Knowledge Representation
        ↓
Storage / Index
        ↓
User Query
        ↓
Retrieval
        ↓
Evidence[]
       ↙   ↘
Evaluation  LLM
              ↓
            Answer
              ↓
       Answer Evaluation
```

The four representation approaches are:

1. **Text / Chunked Text**
2. **Text + Metadata**
3. **Structured Data**
4. **Knowledge Graph**

The four representations are **parallel alternatives** created from the same source.

```text
                         Common Source
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
            Text        Text + Metadata   Structured
              │               │               │
              └───────────────┼───────────────┘
                              │
                         Knowledge Graph
```

Conceptually, the graph should also be understood as an independent representation derived from the same source, not as something that must be built downstream from another team's representation.

---

# 3. Representation vs Storage vs Retrieval

The most important architectural distinction is:

```text
Representation ≠ Storage / Index ≠ Retrieval
```

### Representation

How knowledge is organized.

Examples:

```text
Text
Text + Metadata
Structured Tables
Knowledge Graph
```

### Storage / Index

Where or how the representation is persisted and made searchable.

Examples:

```text
Text index
Vector store
PostgreSQL
Graph database
```

### Retrieval

How relevant information is found.

Examples:

```text
Keyword
Semantic / Vector
Hybrid
Metadata Filtering
SQL
Graph Traversal
Reranking
```

For example:

```text
Text Representation
        ↓
Storage / Index
        ↓
Semantic Retrieval
        ↓
Evidence[]
```

Similarly:

```text
Structured Representation
        ↓
PostgreSQL
        ↓
SQL Retrieval
        ↓
Evidence[]
```

And:

```text
Graph Representation
        ↓
Graph Store
        ↓
Graph Traversal
        ↓
Evidence[]
```

A vector database, therefore, should not be described as the representation itself.

---

# 4. Team Responsibility Model

The project is divided into two major phases.

## Phase 1 — Representation Ownership

Each pair owns its assigned representation **end-to-end to the point required to make that representation usable, queryable, and capable of returning evidence**.

Every pair is responsible for:

```text
SOURCE
  ↓
REPRESENT
  ↓
STORE / INDEX
  ↓
BASIC / NATIVE RETRIEVAL
  ↓
Evidence[]
```

This means each pair must understand:

* the source knowledge relevant to its representation,
* how the knowledge should be represented,
* how that representation should be stored,
* how it can be queried,
* how retrieved results can be converted into the common `Evidence[]` format,
* what kinds of questions the representation handles well,
* where the representation or basic retrieval fails.

### Phase 1 does NOT mean:

* implementing every retrieval technique,
* building the final RAG application,
* creating a separate evaluation framework,
* creating a separate benchmark,
* comparing all four representations,
* implementing every possible representation × retrieval combination,
* changing shared interfaces without approval.

---

# 5. How Phase 1 Is Tested

The main Phase 1 output is **retrieved evidence**, not the final LLM answer.

The testing flow is:

```text
Source
   ↓
Representation
   ↓
Storage / Index
   ↓
Question
   ↓
Basic / Native Retrieval
   ↓
Top-K Evidence
   ↓
Compare with Ground Truth
```

For example:

```text
Question:
"What is the refund period for a Premium customer in India?"

        ↓

Basic / Native Retriever

        ↓

Top-K Evidence

        ↓

Inspect:
- Was the correct policy retrieved?
- Was it ranked appropriately?
- Is the evidence complete?
- Can it be traced to the source?
- Was the wrong policy version retrieved?
- Was an exception missed?
```

Each pair should demonstrate that its representation can actually retrieve meaningful evidence.

### Important: LLM is not required for Phase 1

Do **not** depend on an LLM to prove that the representation works.

The important Phase 1 question is:

> **Can our representation retrieve the right evidence?**

The LLM comes downstream:

```text
Question
   ↓
Retrieval
   ↓
Evidence[]
   ↓
LLM
   ↓
Answer
```

This separation is important because a strong LLM can sometimes produce a plausible answer even when the retrieved evidence is incorrect or incomplete.

---

# 6. Phase 2 — Shared Retrieval & Evaluation

After the four representations are usable, the project moves into shared experimentation.

The shared layer investigates applicable retrieval strategies across the representations.

Conceptually:

```text
Same Query
    ↓
Representation
    +
Applicable Retrieval Strategy
    ↓
Evidence[]
    ↓
Common Evaluation
    ↓
Comparison
    ↓
LLM
    ↓
Answer
```

Possible retrieval strategies include:

* Keyword retrieval
* Semantic / Vector retrieval
* Hybrid retrieval
* Metadata filtering
* Reranking
* SQL / Structured retrieval
* Graph traversal

Not every retrieval strategy must apply to every representation.

| Representation  | Applicable retrieval examples                            |
| --------------- | -------------------------------------------------------- |
| Text            | Keyword, semantic, hybrid, reranking                     |
| Text + Metadata | Keyword, semantic, hybrid, metadata filtering, reranking |
| Structured      | SQL / structured retrieval                               |
| Knowledge Graph | Graph traversal / graph retrieval                        |

The goal is to compare **meaningful combinations**, not force every technique onto every representation.

---

# 7. Pair 1 — Text / Chunked Text

## Ownership

Folder:

```text
representations/text/
```

Pair 1 owns the plain text representation of the NovaMart handbook.

## Responsibilities

The pair should:

1. Read and understand the NovaMart source.
2. Extract the relevant textual knowledge.
3. Clean and normalize the text where appropriate.
4. Design a chunking strategy.
5. Preserve source traceability.
6. Store the resulting text representation in an appropriate searchable/indexed form.
7. Implement a basic/native retrieval path.
8. Convert retrieved results into the common `Evidence[]` format.
9. Test the representation using representative questions.
10. Document important design decisions and limitations.

Conceptually:

```text
Source Document
      ↓
Clean Text
      ↓
Chunks
      ↓
Searchable / Indexed Storage
      ↓
Basic Retrieval
      ↓
Evidence[]
```

The pair should investigate reasonable chunking choices rather than assuming one chunk size is automatically correct.

They may compare a small number of chunking configurations to understand how chunk boundaries affect retrieval readiness.

## Main research question

> **How does chunking affect the ability of a text representation to preserve and retrieve useful evidence?**

## Do not implement independently

Pair 1 should not independently build:

* the complete vector retrieval framework,
* the complete hybrid retrieval framework,
* the common evaluation framework,
* the final application,
* the cross-representation comparison.

Those belong to Phase 2/shared work.

---

# 8. Pair 2 — Text + Metadata

## Ownership

Folder:

```text
representations/text_metadata/
```

Pair 2 owns a representation where textual knowledge is accompanied by useful metadata.

Possible source-supported metadata may include:

* policy area,
* customer tier,
* region,
* product category,
* effective dates,
* promotion,
* seller type,
* policy/version information.

Metadata must come from the NovaMart source.

> **Do not invent metadata simply to make retrieval easier.**

## Responsibilities

The pair should:

1. Understand the source.
2. Identify useful metadata explicitly supported by the source.
3. Design the text + metadata representation.
4. Decide how text and metadata should be stored/indexed.
5. Populate the representation.
6. Implement a basic/native retrieval or filtering path.
7. Return retrieved results through `Evidence[]`.
8. Test representative queries.
9. Document why particular metadata fields were selected.
10. Document limitations.

Conceptually:

```text
Source
   ↓
Text Unit
   +
Metadata
   ↓
Storage / Index
   ↓
Basic Retrieval / Filtering
   ↓
Evidence[]
```

## Main research question

> **Can metadata-rich representation preserve constraints and context that plain text alone may not make explicit?**

## Important distinction

Metadata representation and metadata retrieval are different things.

For example:

```text
Text + region + customer tier
```

is the **representation**.

Using:

```text
region = "India"
customer_tier = "Premium"
```

to restrict retrieval is a **retrieval strategy**.

The pair should implement only the basic/native path necessary to prove its representation works. More advanced metadata retrieval experiments belong to Phase 2.

---

# 9. Pair 3 — Structured Data

## Ownership

Folder:

```text
representations/structured_table/
```

Pair 3 owns the structured representation of the NovaMart knowledge.

PostgreSQL is the preferred database unless there is a documented technical reason to use another solution.

## Candidate entities

The pair should investigate natural entities such as:

* Customer
* Product
* Manufacturer
* Seller
* Policy
* Promotion
* Region
* Support Case
* Order

The final schema should be based on the actual NovaMart source.

## Responsibilities

The pair should:

1. Identify naturally structured entities.
2. Identify attributes.
3. Identify relationships.
4. Design the relational schema.
5. Create the database tables.
6. Load source-supported data.
7. Preserve stable source identifiers.
8. Create representative SQL retrieval queries.
9. Convert retrieved information into `Evidence[]`.
10. Test the representation.
11. Document schema and design decisions.

Conceptually:

```text
NovaMart Source
      ↓
Entities + Relationships
      ↓
Relational Schema
      ↓
PostgreSQL
      ↓
Basic SQL Retrieval
      ↓
Evidence[]
```

## Main research question

> **Which types of NovaMart knowledge are naturally represented and queried as structured entities and relationships?**

## Important restriction

Do not turn every sentence in the handbook into an arbitrary database row.

The objective is to identify knowledge that naturally benefits from structured representation.

Do not hardcode answers directly into SQL queries.

The database should contain the knowledge; queries should retrieve it.

---

# 10. Pair 4 — Knowledge Graph

## Ownership

Folder:

```text
representations/knowledge_graph/
```

Pair 4 owns the graph representation of NovaMart knowledge.

## Candidate entities

Examples include:

* Customer
* Tier
* Product
* Category
* Manufacturer
* Seller
* Policy
* Promotion
* Region
* Order
* Support Case
* Escalation Level

## Candidate relationships

Examples:

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

The final graph must be based on relationships supported by the NovaMart source.

## Responsibilities

The pair should:

1. Identify entities.
2. Identify relationships.
3. Design the graph model.
4. Choose an appropriate graph storage solution.
5. Populate the graph.
6. Preserve source identifiers.
7. Implement basic/native graph traversal retrieval.
8. Return retrieved evidence through `Evidence[]`.
9. Test one-hop, two-hop, and where appropriate multi-hop questions.
10. Document the graph design and limitations.

Conceptually:

```text
NovaMart Source
      ↓
Nodes + Relationships
      ↓
Graph Storage
      ↓
Basic Graph Traversal
      ↓
Evidence[]
```

## Main research question

> **Can graph structure preserve relationship-heavy knowledge that may be difficult to retrieve from flat text?**

## Important restriction

Do not invent relationships.

Do not hardcode the answer to a question into the graph or traversal query.

The graph must represent actual knowledge from the NovaMart source.

---

# 11. Common Evidence Contract

All four pairs must return evidence in the same conceptual format.

```python
@dataclass
class Evidence:
    content: str
    source_id: str
    score: float
    metadata: dict[str, Any]
```

The purpose is to make the four representations interchangeable from the perspective of the rest of the system.

The integration layer should be able to receive:

```text
Evidence[]
```

without needing to know how that evidence was originally stored.

Each result must preserve source traceability wherever possible.

---

# 12. Evaluation Ownership

Evaluation is a **shared responsibility**, not four independent pair projects.

The common evaluation layer lives under:

```text
evaluation/
```

The project evaluates retrieval primarily at the evidence level before judging the final LLM answer.

Conceptually:

```text
Question
   ↓
Expected Evidence / Source IDs
   ↓
Retrieved Evidence[]
   ↓
Retrieval Evaluation
   ↓
Evidence Sufficiency
   ↓
LLM
   ↓
Answer
   ↓
Answer Evaluation
```

Possible retrieval metrics include:

* Precision@K
* Recall@K
* MRR
* nDCG@K where applicable
* Retrieval latency

The evaluation should also examine:

* source traceability,
* whether required evidence was retrieved,
* whether evidence was sufficient,
* incorrect near-matches,
* temporal/version mistakes,
* ignored exceptions,
* missing multi-hop evidence,
* irrelevant evidence overload,
* representation-specific failure modes.

Pairs may create **local tests** for their own representation, but they should not create separate competing evaluation frameworks.

---

# 13. Same Benchmark

All representations use the same NovaMart evaluation questions.

The benchmark is provided under:

```text
data/queries/
```

Teams must not create their own independent benchmark as a replacement.

This is important because the final comparison must be fair.

The question should remain the same while the representation and/or retrieval method changes.

For example:

```text
Question Q001
   ↓
Text Representation
   ↓
Evidence A
```

```text
Question Q001
   ↓
Text + Metadata Representation
   ↓
Evidence B
```

```text
Question Q001
   ↓
Structured Representation
   ↓
Evidence C
```

```text
Question Q001
   ↓
Graph Representation
   ↓
Evidence D
```

The common evaluator can then compare the evidence.

---

# 14. Phase 1 vs Phase 2

This distinction is mandatory.

## Phase 1 — Pair-owned

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

Each pair owns this part.

The purpose is to prove:

> **Our representation is correctly built, stored, queryable, and capable of returning traceable evidence.**

## Phase 2 — Lead/shared

```text
Same Query
 ↓
Applicable Representation
 +
Applicable Retrieval Strategy
 ↓
Evidence[]
 ↓
Common Evaluation
 ↓
Comparison
 ↓
LLM
 ↓
Answer
```

The lead/shared layer owns the cross-representation experiments.

---

# 15. What Teams Must NOT Do

Without discussion with the lead, teams should not:

* modify `shared/schemas.py`,
* modify `shared/interfaces.py`,
* redesign the common Evidence contract,
* modify the benchmark,
* replace the NovaMart dataset,
* create a separate dataset,
* create a separate application,
* create a separate evaluation framework,
* implement unrelated retrieval systems,
* hardcode answers,
* invent source knowledge,
* add dependencies without discussion,
* modify another pair's representation,
* redesign the overall architecture.

If a team discovers that a shared interface genuinely needs to change, raise the issue before modifying it.

---

# 16. Shared Areas vs Pair Ownership

## Shared Areas

```text
shared/
data/
evaluation/
app/
retrieval/
docs/architecture.md
```

These areas affect the integrated project and require coordination.

## Pair Ownership

Each pair owns its representation folder:

```text
Pair 1 → representations/text/

Pair 2 → representations/text_metadata/

Pair 3 → representations/structured_table/

Pair 4 → representations/knowledge_graph/
```

Teams may add supporting tests and documentation within their ownership area.

---

# 17. Definition of Done — Phase 1

A pair is considered complete when:

* [ ] Source understanding is documented.
* [ ] Representation design is documented.
* [ ] Representation is implemented.
* [ ] Appropriate storage/index is created.
* [ ] Source data is loaded correctly.
* [ ] Source identifiers are preserved.
* [ ] Basic/native retrieval works.
* [ ] Retrieval returns the common `Evidence[]` structure.
* [ ] Representative queries have been tested.
* [ ] Retrieved evidence has been inspected.
* [ ] Ground-truth comparison has been performed for representative questions.
* [ ] At least some failure/limitation cases are documented.
* [ ] No unsupported knowledge has been invented.
* [ ] Code is contained within the team's ownership boundary.
* [ ] Documentation explains important technical decisions.
* [ ] Changes are committed to the team's branch.
* [ ] Pull request is ready for integration review.

---

# 18. Final Project Goal

The final project should allow us to demonstrate something more meaningful than:

> "Here are four different RAG implementations."

Instead, we want to demonstrate:

```text
Knowledge Representation
          ×
Retrieval Strategy
          ↓
Retrieved Evidence
          ↓
Evidence Evaluation
          ↓
LLM Answer
          ↓
Answer Evaluation
```

The same question can produce different evidence depending on how the underlying knowledge is represented and how that representation is searched.

That difference is the core subject of this project.

---

# 19. Golden Rule

> **Each pair owns its representation from Source → Representation → Storage → Basic/Native Retrieval → Evidence[].**

> **Advanced retrieval experimentation, cross-representation comparison, common evaluation, integration, and the final application belong to the shared Phase 2.**

This boundary keeps the project integrated while giving every pair genuine ownership of a technically meaningful component.
