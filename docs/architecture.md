# RAG Knowledge Representation & Retrieval Playground — Architecture

## 1. Purpose

The **RAG Knowledge Representation & Retrieval Playground** is a comparative RAG system designed to study how different ways of representing knowledge and retrieving evidence affect the final answer produced by an LLM.

The project uses:

* One common source of knowledge
* One normalized dataset
* One evaluation benchmark
* Multiple knowledge representations
* Multiple retrieval strategies
* A common evidence interface
* A shared evaluation layer

The goal is to make retrieval behavior **observable, comparable, and measurable**.

---

# 2. High-Level Architecture

```text
                    ┌─────────────────────────────┐
                    │     NovaMart Source Data    │
                    │  Customer & Operations      │
                    │      Policy Handbook        │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │      Parse / Normalize      │
                    │                             │
                    │   Common Source Dataset     │
                    └──────────────┬──────────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
     ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
     │     Text     │      │Text + Metadata│     │  Structured   │
     │Representation│      │Representation │     │     Data      │
     └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
            │                     │                     │
            │                     │                     │
            │              ┌──────┴───────┐             │
            │              │              │             │
            │              ▼              │             │
            │      Metadata Constraints   │             │
            │                             │             │
            │                             │             │
            └──────────────┬──────────────┴─────────────┘
                           │
                           │
                    ┌──────▼──────────┐
                    │ Knowledge Graph │
                    │ Representation  │
                    └──────┬──────────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │ Retrieval Strategies│
                 │                     │
                 │ Keyword             │
                 │ Vector              │
                 │ Hybrid              │
                 │ Metadata            │
                 │ Reranking           │
                 │ Structured          │
                 │ Graph               │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Evidence Contract  │
                 │                     │
                 │ content             │
                 │ source_id           │
                 │ score               │
                 │ metadata            │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Evaluation Layer  │
                 │                     │
                 │ Retrieval Quality   │
                 │ Evidence Quality    │
                 │ Answer Quality      │
                 │ Latency             │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │         LLM         │
                 │                     │
                 │ Answer Generation   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Final Answer    │
                 │ + Retrieved Evidence│
                 └─────────────────────┘
```

---

# 3. Core Pipeline

The complete system follows this pipeline:

```text
Source
  ↓
Parse / Extract
  ↓
Knowledge Representation
  ↓
Storage / Index
  ↓
User Query
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

Each stage has a separate responsibility.

### Source

The original NovaMart policy handbook is the common knowledge source.

### Parse / Extract

The source is converted into a normalized representation that can be consumed by the different representation modules.

### Knowledge Representation

The normalized knowledge is organized using one of the project's representation approaches.

### Storage / Index

Each representation may use a storage or indexing mechanism appropriate to its design.

### Query

A user submits a natural-language question.

### Retrieval

The selected retrieval strategy searches the representation and identifies relevant evidence.

### Evidence

Retrieved information is converted into the project's common `Evidence` format.

### LLM

The LLM receives the question and retrieved evidence and generates the answer.

### Evaluation

The system evaluates retrieval, evidence, and answer quality.

---

# 4. Knowledge Representation Layer

The project compares four representation approaches.

## 4.1 Text / Chunked Text

Knowledge is represented as searchable text chunks.

Example:

```text
Policy → Chunk 001
Policy → Chunk 002
Policy → Chunk 003
```

The main experimental variable is how the source is extracted and chunked.

The team investigates:

* Chunk size
* Chunk boundaries
* Context preservation
* Retrieval relevance
* Failure caused by inappropriate chunking

Location:

```text
representations/text/
```

---

## 4.2 Text + Metadata

Knowledge is represented as text units enriched with source-supported metadata.

Example:

```text
Content:
Premium customers can request...

Metadata:
policy_area = refunds
customer_tier = Premium
region = India
effective_from = 2026-07-01
```

Metadata can be used to constrain or improve retrieval.

The team investigates:

* Semantic retrieval
* Metadata filtering
* Combined semantic + metadata retrieval
* Cases where semantic similarity alone is insufficient

Location:

```text
representations/text_metadata/
```

---

## 4.3 Structured Data

Knowledge is represented using structured entities and relationships.

Possible entities include:

```text
Customer
Tier
Product
Manufacturer
Seller
Policy
Promotion
Region
Order
Support Case
```

Relationships are represented explicitly.

For example:

```text
Customer → HAS_TIER → Tier

Product → MANUFACTURED_BY → Manufacturer

Order → CONTAINS → Product

Policy → APPLIES_TO → Region
```

Structured queries can then be used to retrieve relevant information.

Location:

```text
representations/structured_table/
```

---

## 4.4 Knowledge Graph

Knowledge is represented as a graph of entities and relationships.

Example:

```text
Customer
   │
   └── HAS_TIER ──→ Premium
                         │
                         └── QUALIFIES_FOR ──→ Promotion
                                                   │
                                                   └── USES ──→ Policy
```

The graph representation is particularly useful for investigating relationship-heavy and multi-hop questions.

The team investigates:

* Entity relationships
* One-hop retrieval
* Multi-hop retrieval
* Relationship traversal
* Graph-specific failure cases

Location:

```text
representations/knowledge_graph/
```

---

# 5. Retrieval Layer

Knowledge representation and retrieval are treated as **separate dimensions**.

A representation should not be assumed to have only one possible retrieval method.

For example:

```text
Text
 ├── Keyword
 ├── Vector
 ├── Hybrid
 └── Reranking
```

Similarly:

```text
Text + Metadata
 ├── Vector
 ├── Metadata filtering
 └── Hybrid
```

Structured data may use:

```text
Structured Data
 └── SQL / Structured Query
```

Knowledge graphs may use:

```text
Knowledge Graph
 └── Graph Traversal
```

The exact implementation is owned by the relevant team within the project's common interfaces and constraints.

Retrieval modules are located under:

```text
retrieval/
```

---

# 6. Common Evidence Contract

Different retrieval implementations must produce a common evidence format.

```python
@dataclass
class Evidence:
    content: str
    source_id: str
    score: float
    metadata: dict[str, Any]
```

### Fields

**`content`**

The actual retrieved information.

**`source_id`**

Identifier that allows the retrieved evidence to be traced back to the source.

**`score`**

The retrieval relevance score when available.

**`metadata`**

Additional source or retrieval information.

This contract allows the rest of the system to remain independent of the underlying representation.

---

# 7. Common Retriever Interface

Retrievers follow a shared interface:

```python
class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[Evidence]:
        pass
```

The interface provides a common entry point while allowing each retrieval implementation to use its own internal technology.

The application and evaluation layers should not need to know how a specific retriever works internally.

---

# 8. Representation Interface

Knowledge representations follow a common abstraction:

```python
class KnowledgeRepresentation(ABC):

    @abstractmethod
    def build(self, documents):
        pass
```

The purpose is to separate:

```text
What the knowledge representation does
```

from:

```text
How the representation is implemented
```

---

# 9. Registry

The project contains a registry that allows representations and retrievers to be discovered and selected without hardcoding them throughout the application.

Conceptually:

```text
Representation Registry
        │
        ├── text
        ├── text_metadata
        ├── structured
        └── knowledge_graph

Retriever Registry
        │
        ├── keyword
        ├── vector
        ├── hybrid
        ├── metadata
        ├── reranking
        ├── structured
        └── graph
```

This supports integration and experimentation.

---

# 10. Evaluation Architecture

Evaluation is performed at multiple levels.

## 10.1 Retrieval Quality

The first question is:

> Did the retriever find the evidence that was expected?

Possible metrics include:

* Precision@K
* Recall@K
* MRR
* nDCG@K
* Retrieval latency

---

## 10.2 Evidence Quality

The second question is:

> Is the retrieved evidence sufficient and traceable?

The evaluation can examine:

* Required source IDs retrieved
* Evidence sufficiency
* Source traceability
* Irrelevant evidence
* Missing evidence

---

## 10.3 Answer Quality

The final question is:

> Did the answer correctly use the retrieved evidence?

The evaluation can examine:

* Correctness
* Groundedness / faithfulness
* Evidence-supported answers

---

# 11. Evidence-First Evaluation Model

The project follows this mental model:

```text
User Query
    ↓
Expected Evidence
    ↓
Was the correct evidence retrieved?
    ↓
Was the retrieved evidence sufficient?
    ↓
Did the answer use that evidence?
    ↓
Is the final answer correct?
```

This is important because a wrong answer does not necessarily mean the LLM itself was the problem.

A failure may originate from:

```text
Representation
      ↓
Retrieval
      ↓
Evidence
      ↓
LLM Answer
```

The evaluation system therefore attempts to identify **where the failure occurred**.

---

# 12. Benchmark Architecture

All representation and retrieval approaches use the same benchmark.

```text
data/queries/
│
├── evaluation_questions_v3.json
├── ground_truth_v3.json
├── evaluation_rubric_v3.json
└── benchmark_audit_v3.json
```

The benchmark currently contains:

```text
40 evaluation questions
40 ground-truth entries
```

Questions cover scenarios such as:

* Temporal policies
* Regional overrides
* Customer tiers
* Product-specific rules
* Exceptions
* Policy precedence
* Multi-hop relationships
* Promotions
* Near-match entities
* Structured information

The benchmark must remain unchanged during representation experiments.

---

# 13. Failure Analysis

The project intentionally examines retrieval failure modes.

Examples include:

### Semantic Near-Match

The system retrieves a semantically similar but incorrect policy.

### Wrong Policy Version

The system retrieves an older or expired policy instead of the applicable version.

### Wrong Region

The system retrieves a global policy while a regional override applies.

### Wrong Customer Tier

The system retrieves a general policy when the customer's tier-specific policy should apply.

### Ignored Exception

The general rule is retrieved but a relevant exception is missed.

### Incomplete Multi-Hop Path

The system retrieves only part of a relationship chain.

### Irrelevant Evidence Overload

The correct evidence exists but is buried among irrelevant retrieved content.

### Unsupported Answer

The final answer may appear correct but cannot be supported by the retrieved evidence.

---

# 14. Application Layer

The application provides a common interface for interacting with the different approaches.

The application should allow users to:

1. Enter a question.
2. Select a representation.
3. Select a retrieval strategy.
4. Retrieve evidence.
5. Inspect the retrieved evidence.
6. Generate an answer.
7. Compare results.
8. Inspect evaluation results.

The application should not contain representation-specific business logic that belongs inside the representation or retrieval modules.

Location:

```text
app/
├── backend/
└── frontend/
```

---

# 15. Ownership Boundaries

## Representation Teams Own

```text
representations/<their-module>/
```

They are responsible for:

* Research
* Design
* Implementation
* Tests
* Experiments
* Documentation
* Representation-specific results

---

## Retrieval Teams / Modules Own

```text
retrieval/<their-module>/
```

They are responsible for:

* Retrieval implementation
* Retrieval experiments
* Tests
* Retrieval metrics
* Failure analysis
* Documentation

---

## Project Lead / Core Integration Owns

```text
shared/
evaluation/
app/
docs/
```

These areas define the project's common contracts and integration behavior.

---

# 16. Shared Data Ownership

The following directories are shared project inputs:

```text
data/source/
data/normalized/
data/queries/
```

Teams must **not modify the benchmark or common dataset** to improve their own results.

If a genuine dataset issue is discovered, it should be reported to the project lead rather than silently changed inside a team branch.

---

# 17. Git Integration

Each pair works on its own feature branch.

Example:

```text
main
 │
 ├── feature/text-representation
 ├── feature/text-metadata
 ├── feature/structured
 └── feature/knowledge-graph
```

Changes are integrated through Pull Requests.

The basic flow is:

```text
main
 ↓
Feature Branch
 ↓
Research
 ↓
Implementation
 ↓
Testing
 ↓
Experiment
 ↓
Pull Request
 ↓
Review
 ↓
Merge
```

The `main` branch should remain stable and runnable.

---

# 18. Design Principle

The project is **not** intended to prove that one representation or retrieval technique is universally superior.

Instead, the goal is to understand:

> **Which representation and retrieval approach works well for which type of question, what evidence it retrieves, and where it fails.**

The final system should make those differences visible through:

```text
Representation
      ↓
Retrieval
      ↓
Evidence
      ↓
Answer
      ↓
Evaluation
```

This architecture keeps the project modular, comparable, and extensible.
