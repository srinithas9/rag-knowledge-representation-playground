# Team Assignments

## 1. Purpose

The **RAG Knowledge Representation & Retrieval Playground** is a single integrated project designed to study how different ways of representing knowledge and different retrieval strategies affect the evidence retrieved by a RAG system.

The project uses the same **NovaMart Customer & Operations Policy Handbook — 2026 V3** as the common knowledge source for all teams.

The core research question is:

> **How does the combination of knowledge representation and retrieval strategy affect the evidence retrieved for the same question, and how does that evidence affect the final RAG answer?**

The project is therefore not four independent RAG applications.

It is one system with multiple representation approaches that can later be compared under a common retrieval and evaluation framework.

---

# 2. Overall Architecture

The project follows this pipeline:

```text
Same NovaMart Source
        ↓
Knowledge Representation
        ↓
Storage / Index
        ↓
Retrieval
        ↓
Relevant Evidence
        ↓
LLM
        ↓
Answer
        ↓
Evaluation
```

The four representation approaches are:

1. **Text / Chunked Text**
2. **Text + Metadata**
3. **Structured Data**
4. **Knowledge Graph**

The important distinction is:

```text
Representation ≠ Storage ≠ Retrieval
```

For example:

```text
Text
  ↓
Chunked representation
  ↓
Search/index/vector store
  ↓
Keyword / semantic / hybrid retrieval
```

Similarly:

```text
Structured knowledge
  ↓
Tables/entities
  ↓
SQL database
  ↓
SQL retrieval
```

And:

```text
Graph knowledge
  ↓
Nodes + relationships
  ↓
Graph database
  ↓
Graph traversal
```

---

# 3. Team Responsibility Model

The project is divided into two major phases.

## Phase 1 — Representation Ownership

Each pair owns its assigned representation end-to-end **only to the point required to make that representation usable and queryable**.

Every pair is responsible for:

```text
SOURCE
  ↓
REPRESENT
  ↓
STORE
  ↓
BASIC / NATIVE RETRIEVAL
  ↓
Evidence[]
```

This means each pair must understand:

* the source knowledge relevant to its representation
* how the knowledge should be represented
* how that representation should be stored
* how it can be queried
* how retrieved results can be converted into the common `Evidence[]` format

### Phase 1 does NOT mean:

* implementing every retrieval technique
* building the final RAG application
* creating a separate evaluation framework
* creating a separate benchmark
* comparing all four representations
* implementing every possible representation × retrieval combination
* changing shared interfaces without approval

---

# 4. Phase 2 — Shared Retrieval & Evaluation

After the four representations are usable, the project moves into a shared experimentation phase.

The lead/shared layer will investigate applicable retrieval strategies across the representations.

Conceptually:

```text
Same Query
    ↓
Representation A + Retrieval Strategy
Representation B + Retrieval Strategy
Representation C + Retrieval Strategy
Representation D + Retrieval Strategy
    ↓
Evidence[]
    ↓
Common Evaluation
    ↓
Comparison
```

Possible retrieval strategies include:

* keyword retrieval
* semantic/vector retrieval
* hybrid retrieval
* metadata filtering
* reranking
* SQL retrieval
* graph traversal

Not every retrieval strategy must apply to every representation.

For example:

| Representation  | Applicable retrieval examples                            |
| --------------- | -------------------------------------------------------- |
| Text            | Keyword, semantic, hybrid, reranking                     |
| Text + Metadata | Keyword, semantic, hybrid, metadata filtering, reranking |
| Structured      | SQL / structured retrieval                               |
| Knowledge Graph | Graph traversal / graph retrieval                        |

The goal is to compare **meaningful combinations**, not to force every technique onto every representation.

---

# 5. Pair 1 — Text / Chunked Text

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

A useful conceptual representation is:

```text
Source document
      ↓
Clean text
      ↓
Chunks
      ↓
Searchable/indexed storage
      ↓
Basic retrieval
      ↓
Evidence[]
```

The pair should investigate reasonable chunking choices rather than assuming one chunk size is automatically correct.

They may compare a small number of chunking configurations to understand how chunk boundaries affect retrieval readiness.

## Main research question

> How does chunking affect the ability of a text representation to preserve and retrieve useful evidence?

## Do not implement

Pair 1 should not independently build:

* the complete vector retrieval framework
* the complete hybrid retrieval framework
* the common evaluation framework
* the final application
* the cross-representation comparison

Those belong to Phase 2/shared work.

---

# 6. Pair 2 — Text + Metadata

## Ownership

Folder:

```text
representations/text_metadata/
```

Pair 2 owns a representation where textual knowledge is accompanied by useful metadata.

Possible source-supported metadata may include:

* policy area
* customer tier
* region
* product category
* effective dates
* promotion
* seller type
* policy/version information

Metadata must come from the NovaMart source.

**Do not invent metadata simply to make retrieval easier.**

## Responsibilities

The pair should:

1. Understand the source.
2. Identify useful metadata that is explicitly supported by the source.
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
Text unit
   +
Metadata
   ↓
Storage / Index
   ↓
Basic retrieval / filtering
   ↓
Evidence[]
```

## Main research question

> Can metadata-rich representation preserve constraints and context that plain text alone may not make explicit?

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

# 7. Pair 3 — Structured Data

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
6. Load the source-supported data.
7. Preserve stable source identifiers.
8. Create representative SQL retrieval queries.
9. Convert retrieved information into `Evidence[]`.
10. Test the representation.
11. Document schema and design decisions.

Conceptually:

```text
NovaMart source
      ↓
Entities + relationships
      ↓
Relational schema
      ↓
PostgreSQL
      ↓
Basic SQL retrieval
      ↓
Evidence[]
```

## Main research question

> Which types of NovaMart knowledge are naturally represented and queried as structured entities and relationships?

## Important restriction

Do not turn every sentence in the handbook into an arbitrary database row.

The objective is to identify knowledge that naturally benefits from structured representation.

Do not hardcode answers directly into SQL queries.

The database should contain the knowledge; queries should retrieve it.

---

# 8. Pair 4 — Knowledge Graph

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
Customer ──HAS_TIER──> Tier

Customer ──PLACED──> Order

Order ──CONTAINS──> Product

Product ──MANUFACTURED_BY──> Manufacturer

Product ──PART_OF──> Category

Product ──QUALIFIES_FOR──> Promotion

Promotion ──USES──> Policy

Policy ──APPLIES_TO──> Region
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
NovaMart source
      ↓
Nodes + relationships
      ↓
Graph storage
      ↓
Basic graph traversal
      ↓
Evidence[]
```

## Main research question

> Can graph structure preserve relationship-heavy knowledge that may be difficult to retrieve from flat text?

## Important restriction

Do not invent relationships.

Do not hardcode the answer to a question into the graph or traversal query.

The graph must represent actual knowledge from the NovaMart source.

---

# 9. Common Evidence Contract

All four pairs must eventually return evidence in the same conceptual format.

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

# 10. Evaluation Ownership

Evaluation is a **shared responsibility**, not four independent pair projects.

The common evaluation layer lives under:

```text
evaluation/
```

The project will evaluate retrieval primarily at the evidence level before judging the final LLM answer.

Conceptually:

```text
Question
   ↓
Expected evidence
   ↓
Retrieved Evidence[]
   ↓
Retrieval evaluation
   ↓
Evidence sufficiency
   ↓
LLM answer
   ↓
Answer evaluation
```

Possible retrieval metrics include:

* Precision@K
* Recall@K
* MRR
* nDCG@K where applicable
* retrieval latency

The evaluation should also examine:

* source traceability
* whether required evidence was retrieved
* whether evidence was sufficient
* failure cases
* incorrect near-matches
* temporal/version mistakes
* ignored exceptions
* missing multi-hop evidence
* irrelevant evidence overload

Pairs may create **local tests** for their own representation, but they should not create separate competing evaluation frameworks.

---

# 11. Same Benchmark

All representations use the same NovaMart evaluation questions.

The benchmark is already provided under:

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
Text representation
   ↓
Evidence A

Question Q001
   ↓
Text + Metadata representation
   ↓
Evidence B

Question Q001
   ↓
Structured representation
   ↓
Evidence C

Question Q001
   ↓
Graph representation
   ↓
Evidence D
```

The common evaluator can then compare the evidence.

---

# 12. Phase 1 vs Phase 2

This distinction is mandatory.

## Phase 1 — Pair-owned

```text
Source
 ↓
Representation
 ↓
Storage
 ↓
Basic / Native Retrieval
 ↓
Evidence[]
```

Each pair owns this part.

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
```

The lead/shared layer owns the cross-representation experiments.

---

# 13. What Teams Must NOT Do

Without discussion with the lead, teams should not:

* modify `shared/schemas.py`
* modify `shared/interfaces.py`
* redesign the common Evidence contract
* modify the benchmark
* replace the NovaMart dataset
* create a separate dataset
* create a separate application
* create a separate evaluation framework
* implement unrelated retrieval systems
* hardcode answers
* invent source knowledge
* add dependencies without discussion
* modify another pair's representation
* redesign the overall architecture

If a team discovers that a shared interface genuinely needs to change, raise the issue before modifying it.



Shared areas include:

```text
shared/
data/
evaluation/
app/
docs/architecture.md
```

## Pair Ownership

Each pair owns only its representation folder:

```text
Pair 1 → representations/text/
Pair 2 → representations/text_metadata/
Pair 3 → representations/structured_table/
Pair 4 → representations/knowledge_graph/
```

Teams may add supporting tests and documentation within their ownership area.

---

# 15. Definition of Done — Phase 1

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
* [ ] At least some failure/limitation cases are documented.
* [ ] No unsupported knowledge has been invented.
* [ ] Code is contained within the team's ownership boundary.
* [ ] Documentation explains important technical decisions.
* [ ] Changes are committed to the team's branch.
* [ ] Pull request is ready for integration review.

---

# 16. Final Project Goal

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
LLM Answer
          ↓
Evaluation
```

The same question can produce different evidence depending on how the underlying knowledge is represented and how that representation is searched.

That difference is the core subject of this project.

---

# 17. Golden Rule

> **Each pair owns its representation from Source → Representation → Storage → Basic/Native Retrieval → Evidence[].**

> **Advanced retrieval experimentation, cross-representation comparison, common evaluation, integration, and the final application belong to the shared Phase 2.**

This boundary keeps the project integrated while giving every pair genuine ownership of a technically meaningful component.
