# Team Assignments

## 1. Purpose

The **RAG Knowledge Representation & Retrieval Playground** is a single integrated project designed to study how different ways of representing knowledge and different retrieval strategies affect the evidence retrieved by a RAG system.

The project uses the same **NovaMart Customer & Operations Policy Handbook — 2026 V3** as the common knowledge source for all teams.

The core research question is:

> **How does the combination of knowledge representation and retrieval strategy affect the evidence retrieved for the same question, and how does that evidence affect the final RAG answer?**

The project is **not four independent RAG applications**.

It is one integrated system containing multiple representation pipelines that can later be compared under a common evaluation and integration framework.

---

# 2. Overall Architecture

The complete project follows this conceptual pipeline:

```text
                    SAME NOVAMART KNOWLEDGE
                              │
                              ▼
                     Common Source Data
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼                 ▼
          TEXT          STRUCTURED          GRAPH              VISUAL
            │                 │                 │                 │
            ▼                 ▼                 ▼                 ▼
      Pair-owned         Pair-owned       Pair-owned         Pair-owned
       pipeline            pipeline         pipeline           pipeline
            │                 │                 │                 │
            ▼                 ▼                 ▼                 ▼
      PipelineResult    PipelineResult   PipelineResult    PipelineResult
            └─────────────────┼─────────────────┘
                              ▼
                    Common Evaluation
                              │
                              ▼
                         Common LLM
                              │
                              ▼
                      Answer Evaluation
                              │
                              ▼
                         Comparison
                              │
                              ▼
                          Final UI
```

The four core representation approaches are:

1. **Text / Chunked Text**
2. **Structured / Relational Data**
3. **Knowledge Graph**
4. **Visual / Multimodal Document Representation**

These are parallel alternatives created from the same NovaMart source.

```text
                         Common NovaMart Source
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼                    ▼
           TEXT              STRUCTURED             GRAPH               VISUAL
             │                    │                    │                    │
             ▼                    ▼                    ▼                    ▼
          Pipeline             Pipeline             Pipeline             Pipeline
```

No representation is required to be built downstream from another representation.

Each pair builds its assigned representation directly from the common source knowledge.

---

# 3. Representation vs Storage vs Retrieval

The most important architectural distinction is:

```text
Representation ≠ Storage / Index ≠ Retrieval
```

## Representation

Representation describes:

> **How the knowledge is organized.**

Our four core representations are:

```text
Text / Chunked Text
Structured / Relational Data
Knowledge Graph
Visual / Multimodal Document
```

Metadata can be attached to a representation where useful, but **metadata is not a separate core representation in this project**.

For example:

```text
Text chunk
+
region
+
customer tier
+
policy version
```

is still a text representation with metadata.

---

## Storage / Index

Storage or indexing describes:

> **Where or how the representation is persisted and made searchable.**

Examples:

```text
Text index
Vector store
PostgreSQL
Graph database
Multimodal / vector index
```

The storage technology is a design decision of the relevant pair.

---

## Retrieval

Retrieval describes:

> **How relevant information is found from the representation.**

Examples include:

```text
Keyword retrieval
Semantic / vector retrieval
Hybrid retrieval
Metadata filtering
Reranking
SQL retrieval
Graph traversal
Multimodal retrieval
```

Not every retrieval method applies naturally to every representation.

For example:

```text
Text
  ↓
Semantic / Keyword / Hybrid Retrieval
```

```text
Structured
  ↓
SQL / Structured Retrieval
```

```text
Graph
  ↓
Graph Traversal
```

```text
Visual
  ↓
Multimodal / Multi-vector Retrieval
```

The project should compare **meaningful representation + retrieval combinations**, not force every retrieval method onto every representation.

---

# 4. Team Responsibility Model

The project follows a **vertical-slice ownership model**.

Each pair owns its assigned representation end-to-end through basic/native retrieval and evidence generation.

Every pair is responsible for:

```text
SOURCE
   ↓
REPRESENTATION
   ↓
STORAGE / INDEX
   ↓
BASIC / NATIVE RETRIEVAL
   ↓
Evidence[]
   ↓
PipelineResult
```

This means each pair should understand:

* the source knowledge relevant to its representation,
* how the knowledge should be represented,
* how the representation should be stored,
* how it can be queried,
* how retrieved results can be converted into the common `Evidence` format,
* what kinds of questions the representation handles well,
* where the representation or basic retrieval fails.

---

## Phase 1 does NOT mean

Pairs are **not** expected to independently build:

* the complete final RAG application,
* the common evaluation framework,
* the common benchmark,
* the cross-representation comparison engine,
* every possible retrieval technique,
* every possible representation × retrieval combination,
* separate applications,
* separate datasets,
* independent evaluation frameworks.

The purpose of Phase 1 is to prove that the assigned representation can be built, queried, and used to return traceable evidence.

---

# 5. Common Pipeline Contract

All four pipelines must eventually expose the same external contract.

Conceptually:

```python
result = pipeline.run(
    query=query,
    top_k=5
)
```

The common result is:

```text
PipelineResult
├── pipeline_id
├── representation
├── retrieval_method
├── evidence[]
└── latency_ms
```

Each evidence item follows the common structure:

```text
Evidence
├── content
├── source_id
├── score
└── metadata
```

The internal implementation can be completely different between pairs.

For example:

```text
Text
→ chunks
→ embeddings
→ vector search
→ Evidence[]
```

while:

```text
Structured
→ relational tables
→ SQL query
→ Evidence[]
```

and:

```text
Graph
→ nodes + relationships
→ graph traversal
→ Evidence[]
```

and:

```text
Visual
→ page/document representations
→ multimodal retrieval
→ Evidence[]
```

The common interface is what allows these different implementations to be integrated.

---

# 6. Phase 1 — Pair-Owned Pipeline

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
Inspect / Test Evidence
```

For example:

```text
Question:
"What is the refund period for a Premium customer in India?"
        ↓
Pair's native retrieval
        ↓
Top-K Evidence
        ↓
Inspect:
- Was relevant evidence retrieved?
- Is it traceable?
- Is the evidence complete?
- Was the wrong policy version retrieved?
- Was an exception missed?
```

The LLM is **not required to prove that the representation works in Phase 1**.

The important question is:

> **Can our representation retrieve meaningful, traceable evidence?**

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

This separation is important because a strong LLM may sometimes produce a plausible answer even when retrieval was incorrect or incomplete.

---

# 7. Pair 1 — Text / Chunked Text

## Ownership

Folder:

```text
pipelines/text/
```

Pair 1 owns the plain text representation of the NovaMart handbook.

## Responsibilities

The pair should:

1. Read and understand the NovaMart source.
2. Extract relevant textual knowledge.
3. Clean and normalize the text where appropriate.
4. Design a chunking strategy.
5. Preserve source traceability.
6. Store/index the resulting text representation.
7. Implement a basic/native retrieval path.
8. Convert retrieved results into the common `Evidence` format.
9. Implement the common `Pipeline` interface.
10. Test representative questions.
11. Document important design decisions and limitations.

Conceptually:

```text
NovaMart Source
      ↓
Text Extraction
      ↓
Cleaning / Normalization
      ↓
Chunking
      ↓
Searchable / Indexed Storage
      ↓
Basic / Native Retrieval
      ↓
Evidence[]
      ↓
PipelineResult
```

The pair should investigate reasonable chunking choices rather than assuming one chunk size is automatically correct.

They may compare a small number of chunking configurations to understand how chunk boundaries affect retrieval.

## Main research question

> **How does chunking affect the ability of a text representation to preserve and retrieve useful evidence?**

---

# 8. Pair 2 — Structured / Relational Data

## Ownership

Folder:

```text
pipelines/structured/
```

Pair 2 owns the structured representation of NovaMart knowledge.

PostgreSQL is the preferred database unless there is a documented technical reason to use another solution.

## Candidate entities

The pair should investigate entities naturally supported by the actual NovaMart source, such as:

```text
Customer
Customer Tier
Product
Manufacturer
Seller
Policy
Temporal Version
```

Additional entities may only be created if the source actually provides enough structured information to support them.

## Important restriction

Do not invent orders, support cases, promotions, regions, or other structured records merely because they appear conceptually in the handbook.

The final schema must be based on the actual NovaMart source data.

## Responsibilities

The pair should:

1. Identify naturally structured entities.
2. Identify attributes.
3. Identify relationships.
4. Design the relational schema.
5. Create database tables.
6. Load source-supported data.
7. Preserve stable source identifiers.
8. Create representative SQL retrieval queries.
9. Convert retrieved information into `Evidence[]`.
10. Implement the common `Pipeline` interface.
11. Test the representation.
12. Document schema and design decisions.
13. Document limitations caused by information that is not naturally structured in the source.

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
      ↓
PipelineResult
```

## Main research question

> **Which types of NovaMart knowledge become easier to query when represented as structured entities, attributes, and relationships?**

## Important restriction

Do not turn every sentence in the handbook into an arbitrary database row.

The database should contain the knowledge.

Queries should retrieve the knowledge.

Do not hardcode answers directly into SQL queries.

---

# 9. Pair 3 — Knowledge Graph

## Ownership

Folder:

```text
pipelines/graph/
```

Pair 3 owns the graph representation of NovaMart knowledge.

## Candidate entities

Examples include:

```text
Customer
Customer Tier
Product
Category
Manufacturer
Seller
Policy
Promotion
Region
Order
Support Case
```

However, the final graph must only contain entities supported by the actual NovaMart source.

## Candidate relationships

Examples:

```text
Customer ──HAS_TIER──────> Customer Tier

Product ──MANUFACTURED_BY─> Manufacturer

Product ──PART_OF─────────> Category

Product ──QUALIFIES_FOR───> Promotion

Promotion ──USES──────────> Policy
```

These are examples of relationship types to investigate.

They are **not permission to invent source facts**.

## Responsibilities

The pair should:

1. Identify entities.
2. Identify source-supported relationships.
3. Design the graph model.
4. Choose an appropriate graph storage solution.
5. Populate the graph.
6. Preserve source identifiers.
7. Implement basic/native graph traversal retrieval.
8. Return retrieved information through `Evidence[]`.
9. Implement the common `Pipeline` interface.
10. Test one-hop and two-hop questions.
11. Test multi-hop questions where the source supports them.
12. Document the graph design and limitations.

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
      ↓
PipelineResult
```

## Main research question

> **Can explicit graph structure preserve relationship-heavy knowledge that may be difficult to retrieve from flat text?**

## Important restriction

Do not invent relationships.

Do not hardcode the answer to a question into the graph or traversal query.

The graph must represent actual knowledge from NovaMart.

---

# 10. Pair 4 — Visual / Multimodal Document Representation

## Ownership

Folder:

```text
pipelines/visual/
```

Pair 4 owns the visual/multimodal representation of the NovaMart source document.

The purpose is to investigate cases where the **visual structure of the source document** contains useful information that may be weakened or lost when the document is reduced to plain text.

Examples include:

* tables,
* page structure,
* layout,
* spatial relationships,
* headings,
* visually organized policy information,
* document-level context.

## Responsibilities

The pair should:

1. Understand the original NovaMart document.
2. Identify information where visual/layout context matters.
3. Preserve document/page-level visual representation where appropriate.
4. Choose an appropriate visual/multimodal representation.
5. Choose appropriate storage/indexing.
6. Implement a basic/native multimodal retrieval path.
7. Preserve page/source traceability.
8. Convert retrieved results into `Evidence[]`.
9. Implement the common `Pipeline` interface.
10. Test representative visual/table/layout-sensitive questions.
11. Document design decisions.
12. Document limitations.

A technology such as **ColPali** may be investigated as part of this pipeline, but ColPali itself is not the definition of the representation.

Conceptually:

```text
NovaMart Source Document
          ↓
Page / Visual Representation
          ↓
Multimodal / Multi-vector Index
          ↓
Basic Multimodal Retrieval
          ↓
Evidence[]
          ↓
PipelineResult
```

## Main research question

> **Can visual/multimodal representation preserve document information that may be weakened or lost when the source is represented only as text or structured data?**

---

# 11. Metadata Is an Augmentation, Not a Separate Core Representation

Metadata may be used by any appropriate pipeline.

For example:

```text
Text Chunk
├── content
├── policy_id
├── customer_tier
├── region
├── effective_date
└── source_id
```

This does **not** create a fifth representation.

Metadata is an augmentation that can help preserve constraints and traceability.

For example:

```text
Text + Metadata
```

is still part of the Text pipeline.

Similarly, metadata can exist alongside:

```text
Structured Data
Knowledge Graph
Visual Documents
```

where supported by the source.

Metadata must always be based on actual NovaMart information.

---

# 12. Retrieval Strategy Ownership

Retrieval is representation-dependent.

The project does **not** require every pair to implement every retrieval technique.

Examples:

| Representation  | Appropriate retrieval examples               |
| --------------- | -------------------------------------------- |
| Text            | Keyword, semantic/vector, hybrid, reranking  |
| Structured      | SQL, filtering, joins, temporal queries      |
| Knowledge Graph | Entity lookup, graph traversal, Cypher       |
| Visual          | Multimodal retrieval, multi-vector retrieval |

The important requirement is that each pair can justify its chosen retrieval approach.

The pair should be able to explain:

1. Why this retrieval method fits the representation.
2. What query types it should handle well.
3. What query types it may struggle with.
4. What baseline it is being compared against.
5. What failure cases were observed.
6. What evidence supports the design decision.

Advanced retrieval experiments can be added during the shared Phase 2 work.

---

# 13. Common Evidence Contract

All four pairs must return evidence through the same conceptual structure.

```python
@dataclass
class Evidence:
    content: str
    source_id: str
    score: float
    metadata: dict[str, Any]
```

The purpose is to make the four pipelines interchangeable from the perspective of the rest of the system.

The integration layer should be able to receive:

```text
PipelineResult
      ↓
Evidence[]
```

without needing to know how that evidence was originally stored.

Each result should preserve source traceability wherever possible.

---

# 14. Common Pipeline Contract

The common pipeline interface is:

```python
class Pipeline(ABC):

    @abstractmethod
    def run(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> PipelineResult:
        pass
```

The pair's internal implementation may be completely different.

The external boundary remains consistent.

---

# 15. Evaluation Ownership

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
Retrieved Evidence[]
   ↓
Retrieval Evaluation
   ↓
Evidence Sufficiency
   ↓
Common LLM
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
* evidence sufficiency,
* incorrect near-matches,
* temporal/version mistakes,
* ignored exceptions,
* missing multi-hop evidence,
* irrelevant evidence,
* representation-specific failure modes.

Pairs may create **local tests** for their own implementation.

They should not create competing evaluation frameworks.

---

# 16. Same Benchmark

All four pipelines use the same NovaMart evaluation questions.

The benchmark is provided under:

```text
data/queries/
```

The benchmark should not be changed by individual pairs.

Teams must not create their own independent benchmark as a replacement.

This is important because the final comparison must remain controlled.

The same question should be passed through different pipelines.

For example:

```text
Question Q001
      ↓
Text Pipeline
      ↓
Evidence A
```

```text
Question Q001
      ↓
Structured Pipeline
      ↓
Evidence B
```

```text
Question Q001
      ↓
Graph Pipeline
      ↓
Evidence C
```

```text
Question Q001
      ↓
Visual Pipeline
      ↓
Evidence D
```

The common evaluation layer can then compare the evidence.

**The benchmark is currently frozen.**

Any future benchmark change must be discussed at the project level and, if approved, applied consistently to every pipeline.

---

# 17. Phase 1 vs Phase 2

This distinction is mandatory.

## Phase 1 — Pair-Owned

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
   ↓
PipelineResult
```

Each pair owns this part.

The purpose is to prove:

> **Our representation is correctly built, stored, queryable, and capable of returning traceable evidence.**

---

## Phase 2 — Shared

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
Common LLM
      ↓
Answer
      ↓
Answer Evaluation
```

The lead/shared layer owns:

* cross-representation experiments,
* advanced retrieval experimentation,
* common evaluation,
* comparison,
* common LLM integration,
* final application integration.

---

# 18. Shared Repository Structure

The current repository is organized as:

```text
rag-knowledge-representation-playground/
│
├── data/
│   ├── source/
│   ├── normalized/
│   └── queries/
│
├── shared/
│   ├── schemas.py
│   ├── interfaces.py
│   ├── config.py
│   └── registry.py
│
├── pipelines/
│   ├── text/
│   ├── structured/
│   ├── graph/
│   └── visual/
│
├── evaluation/
│   ├── retrieval/
│   ├── answer/
│   ├── analysis/
│   └── results/
│
├── integration/
│   ├── runner.py
│   ├── comparison.py
│   └── types.py
│
├── llm/
│   ├── adapter.py
│   └── prompts.py
│
├── app/
│   ├── backend/
│   └── frontend/
│
└── docs/
```

---

# 19. Shared Areas vs Pair Ownership

## Shared Areas

These affect the integrated project and require coordination:

```text
shared/
data/
evaluation/
integration/
llm/
app/
docs/architecture.md
```

In particular:

```text
shared/schemas.py
shared/interfaces.py
```

must not be changed independently by a pair.

---

## Pair Ownership

```text
Pair 1 → pipelines/text/

Pair 2 → pipelines/structured/

Pair 3 → pipelines/graph/

Pair 4 → pipelines/visual/
```

Pairs may add supporting tests and documentation within their own pipeline.

---

# 20. What Teams Must NOT Do

Without discussion with the lead, teams should not:

* modify `shared/schemas.py`,
* modify `shared/interfaces.py`,
* redesign the common `Evidence` contract,
* modify the benchmark,
* replace the NovaMart dataset,
* create a separate dataset,
* create a separate application,
* create a separate evaluation framework,
* modify another pair's pipeline,
* hardcode answers,
* invent source knowledge,
* add unnecessary dependencies,
* redesign the overall architecture,
* force a retrieval method that does not naturally fit the representation.

If a team discovers that a shared interface genuinely needs to change, raise the issue before modifying it.

---

# 21. Definition of Done — Phase 1

A pair is considered complete when:

```text
[ ] Source understanding is documented
[ ] Representation design is documented
[ ] Representation is implemented
[ ] Appropriate storage/index is created
[ ] Source data is loaded correctly
[ ] Source identifiers are preserved
[ ] Basic/native retrieval works
[ ] Common Pipeline interface is respected
[ ] Retrieval returns common Evidence structure
[ ] PipelineResult is returned correctly
[ ] Representative queries have been tested
[ ] Retrieved evidence has been inspected
[ ] Failure/limitation cases are documented
[ ] No unsupported knowledge has been invented
[ ] Code stays within the team's ownership boundary
[ ] Technical decisions are documented
[ ] Tests pass
[ ] Changes are committed to the team's branch
[ ] Pull Request is ready for integration review
```

---

# 22. Final Project Goal

The final project should demonstrate something more meaningful than:

> "Here are four different RAG implementations."

Instead, we want to demonstrate:

```text
Knowledge Representation
        ↓
Retrieval Strategy
        ↓
Retrieved Evidence
        ↓
Evidence Evaluation
        ↓
LLM Answer
        ↓
Answer Evaluation
        ↓
Comparison
```

The same question may produce different evidence depending on how the underlying knowledge is represented and how that representation is searched.

That difference is the core subject of this project.

---

# 23. Golden Rule

> **Each pair owns its representation from Source → Representation → Storage → Basic/Native Retrieval → Evidence[] → PipelineResult.**

> **Advanced retrieval experimentation, cross-representation comparison, common evaluation, LLM integration, and the final application belong to the shared Phase 2.**

This boundary keeps the project integrated while giving every pair genuine ownership of a technically meaningful component.
