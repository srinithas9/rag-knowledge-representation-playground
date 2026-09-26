# Team Assignments

## 1. Project Objective

The goal of this project is to understand how different ways of representing and storing the same knowledge affect retrieval quality and, ultimately, the evidence available to an LLM.

All teams work with the same NovaMart source dataset and evaluation benchmark.

The project compares four knowledge representation approaches:

1. Text / Chunked Text
2. Text + Metadata
3. Structured Data
4. Knowledge Graph

Each pair is responsible for the complete pipeline for its representation:

```text
NovaMart Source Data
        ↓
Knowledge Representation
        ↓
Representation-Specific Storage / Index
        ↓
Retrieval
        ↓
Evidence[]
        ↓
Evaluation
```

The purpose is not simply to create different data formats.

Each pair must understand and demonstrate:

* how the knowledge is represented
* where/how the representation is stored
* how it is indexed
* how relevant information is retrieved
* what evidence is returned
* what types of questions the approach handles well
* where the approach fails or becomes difficult

---

# 2. Common Dataset

All pairs MUST use the same NovaMart 2026 dataset.

Source:

```text
data/source/
```

Normalized data:

```text
data/normalized/
```

Evaluation questions:

```text
data/queries/
```

Ground truth:

```text
data/queries/ground_truth_v3.json
```

Evaluation rubric:

```text
data/queries/evaluation_rubric_v3.json
```

Do not create a separate dataset.

Do not modify the shared benchmark without lead approval.

---

# 3. Common Pipeline

Every implementation should conceptually follow:

```text
Source Data
    ↓
Parse / Transform
    ↓
Representation
    ↓
Storage / Index
    ↓
Query
    ↓
Retrieval
    ↓
Evidence[]
```

The storage technology may differ between pairs because the representation itself differs.

For example:

```text
Text
 ↓
Chunks
 ↓
Text/Vector/Keyword Index
 ↓
Retrieval
```

```text
Text + Metadata
 ↓
Chunks + Metadata
 ↓
Vector Index + Metadata Filtering
 ↓
Retrieval
```

```text
Structured Data
 ↓
Tables + Relationships
 ↓
SQL Database
 ↓
SQL Retrieval
```

```text
Knowledge Graph
 ↓
Nodes + Relationships
 ↓
Graph Database
 ↓
Graph Traversal
```

The exact technology is a design decision for each pair and must be justified.

---

# 4. Common Evidence Contract

All pairs must return evidence using the shared `Evidence` schema.

Conceptually:

```python
Evidence(
    content=...,
    source_id=...,
    score=...,
    metadata=...
)
```

The rest of the system should not need to know whether the evidence came from:

* a vector database
* a keyword index
* SQL
* a graph database
* metadata filtering
* another approved retrieval mechanism

The representation-specific implementation stays behind the common interface.

---

# 5. Pair 1 — Text / Chunked Text

## Ownership

```text
representations/text/
```

## Objective

Represent the NovaMart handbook as searchable text chunks and investigate how chunking affects retrieval.

The team should explore how decisions such as:

* chunk size
* chunk overlap
* chunk boundaries
* preserved metadata
* source references

affect retrieval quality.

## Required Pipeline

```text
NovaMart Handbook
        ↓
Text Extraction
        ↓
Cleaning
        ↓
Chunking
        ↓
Storage / Index
        ↓
Retrieval
        ↓
Evidence[]
```

## Storage / Index Responsibility

The pair MUST create and use an actual searchable storage/index for its chunks.

The pair should research suitable options and select an approach appropriate for the project.

Possible approaches may include:

* keyword-based indexing
* vector storage
* a local vector database
* another suitable searchable index

The pair must **justify the technology chosen**.

Do not select a technology simply because it is popular.

The choice should consider:

* ease of local setup
* suitability for chunk retrieval
* metadata/source traceability
* retrieval performance
* integration with the common interface

## Required Retrieval

The implementation must retrieve relevant chunks from the team's storage/index.

It must not simply search a Python list or return hardcoded answers.

The retrieval implementation must return:

```text
Evidence[]
```

## Experiments

At minimum, compare 2–3 chunking configurations.

For example:

```text
Configuration A
Configuration B
Configuration C
```

Measure how the configurations affect:

* retrieval relevance
* source coverage
* retrieval latency
* failure cases

## Main Question

> How does chunking affect what evidence a RAG system retrieves?

## Deliverables

The pair should provide:

* representation implementation
* storage/index creation
* retrieval implementation
* tests
* experiment results
* README
* example queries
* retrieval statistics
* latency measurements where practical
* failure analysis
* limitations

---

# 6. Pair 2 — Text + Metadata

## Ownership

```text
representations/text_metadata/
```

## Objective

Represent NovaMart knowledge as searchable text units enriched with meaningful metadata.

Example metadata may include:

* policy area
* customer tier
* region
* product category
* effective date
* expiration date
* promotion
* seller type

Only metadata supported by the source dataset should be used.

## Required Pipeline

```text
NovaMart Handbook
        ↓
Text Extraction
        ↓
Chunk / Text Unit Creation
        ↓
Metadata Attachment
        ↓
Storage / Index
        ↓
Metadata Filtering + Retrieval
        ↓
Evidence[]
```

## Storage / Index Responsibility

The pair MUST create a searchable storage/index that supports the text and its metadata.

The chosen technology should support the team's experiment with:

```text
Semantic Retrieval
        vs
Semantic Retrieval + Metadata Constraints
```

The pair must research and select an appropriate storage/index technology.

The technology choice must be documented and justified.

## Required Retrieval

The pair should support retrieval with metadata constraints where appropriate.

Conceptually:

```text
Query
 ↓
Semantic Search
 ↓
Candidate Evidence
```

and:

```text
Query + Metadata Constraint
 ↓
Filtered Search
 ↓
Candidate Evidence
```

The comparison should show whether metadata constraints help retrieve the correct evidence.

## Important Rule

Do not invent metadata.

If the source does not support a metadata value, do not manufacture one simply to improve retrieval.

## Main Question

> Can metadata constraints improve retrieval when semantic similarity alone is insufficient?

## Deliverables

The pair should provide:

* text + metadata representation
* storage/index creation
* metadata filtering capability
* retrieval implementation
* tests
* experiment results
* README
* example queries
* failure cases
* limitations

---

# 7. Pair 3 — Structured Data

## Ownership

```text
representations/structured_table/
```

## Objective

Represent NovaMart knowledge as structured entities, attributes, and relationships.

The team should identify natural entities such as:

* Customer
* Tier
* Product
* Category
* Manufacturer
* Seller
* Policy
* Promotion
* Region
* Support Case
* Order

The exact schema should be justified from the source data.

## Required Pipeline

```text
NovaMart Source Data
        ↓
Entity Identification
        ↓
Relational Schema
        ↓
SQL Database
        ↓
SQL / Structured Retrieval
        ↓
Evidence[]
```

## Storage Responsibility

The pair MUST create an actual SQL database.

**PostgreSQL is the preferred database for this project.**

The database should contain:

* appropriate tables
* primary keys
* foreign keys
* relevant constraints
* relationships between entities

The pair must provide a schema file such as:

```text
schema.sql
```

The database must be populated from the NovaMart source data.

Do not simply create an SQL file containing hardcoded answers.

## Retrieval Responsibility

The pair should retrieve information using structured queries.

Depending on the question, this may involve:

* SELECT
* WHERE
* JOIN
* aggregation
* filtering
* relationship traversal
* other appropriate SQL operations

The retrieved information must ultimately be converted into:

```text
Evidence[]
```

## Main Question

> Which questions become easier, clearer, or more reliable when knowledge is represented as structured entities and relationships?

## Example Question Types

The team should investigate questions involving:

* exact values
* entity relationships
* filtering
* aggregation
* multiple related entities

## Deliverables

The pair should provide:

* relational schema
* `schema.sql`
* database setup instructions
* data-loading process
* structured retrieval implementation
* Evidence conversion
* tests
* example queries
* experiment results
* README
* limitations
* failure analysis

---

# 8. Pair 4 — Knowledge Graph

## Ownership

```text
representations/knowledge_graph/
```

## Objective

Represent NovaMart knowledge as entities connected through explicit relationships.

The graph should focus particularly on questions where relationships and multi-hop reasoning matter.

## Required Entities

The team should consider entities such as:

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

## Required Relationships

The team should consider source-supported relationships such as:

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

Only relationships supported by the NovaMart source should be created.

## Required Pipeline

```text
NovaMart Source Data
        ↓
Entity Extraction
        ↓
Node + Relationship Creation
        ↓
Graph Database / Graph Store
        ↓
Graph Retrieval / Traversal
        ↓
Evidence[]
```

## Storage Responsibility

The pair MUST create an actual graph-based storage/index.

The team should research appropriate graph technologies and choose one suitable for the project.

The technology choice must be justified.

The graph should contain real nodes and relationships derived from the NovaMart dataset.

Do not create a graph containing only a few manually entered examples.

## Retrieval Responsibility

The team should investigate retrieval based on graph structure.

Particular attention should be given to:

* one-hop relationships
* two-hop relationships
* multi-hop relationships
* relationship filtering
* connected entities

The retrieval implementation must return:

```text
Evidence[]
```

with source traceability.

## Main Question

> Can graph structure improve retrieval for relationship-heavy and multi-hop questions?

## Deliverables

The pair should provide:

* graph schema/model
* graph database/store setup
* data-loading process
* node/relationship creation
* graph retrieval implementation
* Evidence conversion
* tests
* example queries
* multi-hop experiments
* failure analysis
* README
* limitations

---

# 9. Storage Technology Is Part of the Experiment

The database or index is not an afterthought.

Each pair should be able to explain:

> Why is this storage/index appropriate for this representation?

For example:

```text
Representation
      ↓
Why this representation?
      ↓
Why this storage?
      ↓
Why this retrieval method?
      ↓
What evidence does it retrieve?
```

The project is therefore comparing not only data formats, but complete retrieval pipelines.

---

# 10. Technology Selection Rules

Teams are encouraged to research and choose appropriate technologies.

However:

* do not introduce unnecessary infrastructure
* prefer locally reproducible solutions
* document installation/setup requirements
* avoid paid services unless explicitly approved
* do not require cloud infrastructure for the basic demo
* do not create a separate application
* do not create a separate dataset
* do not modify shared interfaces without approval

If a technology introduces a significant new dependency, discuss it with the project lead before adopting it.

---

# 11. Representation vs Retrieval

Teams must keep these concepts separate.

### Representation

How is the knowledge organized?

Examples:

```text
Chunks
Chunks + Metadata
Tables
Nodes + Relationships
```

### Storage / Index

Where and how is that representation made searchable?

Examples:

```text
Text index
Vector index
Vector store
SQL database
Graph database
```

### Retrieval

How do we find relevant evidence?

Examples:

```text
Keyword search
Semantic search
Metadata filtering
SQL query
Graph traversal
Hybrid retrieval
```

A pair must be able to explain all three.

---

# 12. Prohibited Actions

Teams must NOT:

* create a separate dataset
* create a separate benchmark
* hardcode answers
* manually return answers instead of retrieving evidence
* invent relationships
* invent metadata
* modify the common Evidence contract without approval
* modify shared interfaces without approval
* build a completely separate application
* ignore source traceability
* optimize only for one example query
* claim retrieval quality without testing
* add unnecessary infrastructure

---

# 13. Experiment Mindset

The goal is not:

> "Our implementation works."

The goal is:

> "We can demonstrate what this representation and retrieval approach does well, where it fails, and why."

Every pair should therefore include examples of:

### Successful retrieval

```text
Query
↓
Retrieved evidence
↓
Why it is relevant
```

### Failed retrieval

```text
Query
↓
Retrieved evidence
↓
What went wrong
↓
Why it happened
```

### Comparison

Where applicable:

```text
Approach A
vs
Approach B
```

The comparison should be based on observed results rather than assumptions.

---

# 14. Definition of Done

A pair is complete only when all of the following are true:

* [ ] Source dataset understood
* [ ] Representation designed
* [ ] Representation implemented
* [ ] Appropriate storage/index selected
* [ ] Storage/index created and populated
* [ ] Retrieval implemented
* [ ] Common interface respected
* [ ] Evidence[] returned
* [ ] Source traceability preserved
* [ ] Tests written
* [ ] Example queries tested
* [ ] Retrieval behavior measured
* [ ] At least some failure cases documented
* [ ] Technology choices explained
* [ ] README completed
* [ ] No hardcoded answers
* [ ] No separate dataset
* [ ] No unauthorized shared-interface changes
* [ ] Code committed to the team's feature branch
* [ ] Pull request ready for review

---

# 15. Final Goal

At the end of the project, the integrated system should allow the same NovaMart question to be evaluated through different knowledge representations and retrieval approaches.

Conceptually:

```text
                    ┌── Text ────────────────┐
                    │                         │
NovaMart Data ──────┼── Text + Metadata ──────┤
                    │                         │
                    ├── Structured Data ──────┤
                    │                         │
                    └── Knowledge Graph ──────┘
                              ↓
                         Retrieval
                              ↓
                         Evidence[]
                              ↓
                         Evaluation
                              ↓
                    Compare Retrieval Behavior
```

The final demonstration should make one idea clear:

> **The way knowledge is represented and stored affects what evidence can be retrieved, and the quality of retrieved evidence affects the quality of a RAG system's answer.**
