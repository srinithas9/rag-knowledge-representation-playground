# Team Assignments

## RAG Knowledge Representation & Retrieval Playground

## 1. Project Goal

The project studies two separate but connected questions:

### Question 1 — How should knowledge be represented?

We will compare:

1. Text / Chunked Text
2. Text + Metadata
3. Structured Data
4. Knowledge Graph

### Question 2 — How should relevant knowledge be retrieved?

We will later compare techniques such as:

* Keyword retrieval
* Vector / semantic retrieval
* Hybrid retrieval
* Metadata filtering
* Reranking
* Structured retrieval
* Graph retrieval

The important principle is:

> **Representation and retrieval are separate dimensions.**

The same representation may support multiple retrieval strategies.

---

# 2. Common Dataset

All teams will use the same fictional company and source:

**NovaMart — Customer & Operations Policy Handbook 2026**

The source dataset is already available under:

```text
data/
├── source/
├── normalized/
└── queries/
```

Do not create a separate dataset.

Do not modify the benchmark questions or ground truth.

The purpose is to make comparisons fair.

---

# 3. Common Pipeline

Every implementation fits into this overall pipeline:

```text
NovaMart Source Document
        ↓
Knowledge Representation
        ↓
Storage / Index
        ↓
User Query
        ↓
Retrieval
        ↓
Evidence
        ↓
LLM
        ↓
Answer
        ↓
Evaluation
```

Your work focuses primarily on the **representation and/or retrieval** stages.

---

# 4. Pair 1 — Text / Chunked Text

### Assigned area

```text
representations/text/
```

### Objective

Represent the NovaMart handbook as searchable text chunks.

The main question is:

> How does the way we split and organize raw text affect retrieval?

### You should investigate

* Document extraction
* Text cleaning
* Chunking
* Chunk size
* Chunk overlap
* Section boundaries
* Metadata required for traceability
* Retrieval from chunks

### Experiment

Compare approximately 2–3 reasonable chunking strategies.

For example, investigate differences between:

* Smaller chunks
* Medium chunks
* Larger chunks

The exact strategy is your design decision.

### Important requirement

Do not assume that smaller chunks are automatically better.

You should evaluate the effect of chunking on the benchmark.

### Deliverables

```text
representations/text/
├── README.md
├── your implementation files
└── tests/
```

Your implementation should eventually provide evidence compatible with the shared interface.

### README should explain

* What representation you created
* How the document is chunked
* Why you selected your approach
* Chunk statistics
* Retrieval approach used for testing
* Example queries
* Results
* Latency where useful
* Limitations

### Do not

* Create a new dataset
* Hardcode answers
* Create a separate application
* Change shared interfaces without approval

---

# 5. Pair 2 — Text + Metadata

### Assigned area

```text
representations/text_metadata/
```

### Objective

Represent text together with useful structured metadata.

The main question is:

> Can metadata constraints improve retrieval when semantic similarity alone is insufficient?

### Possible metadata

Use metadata that actually exists in the source.

Examples include:

* Policy area
* Customer tier
* Region
* Product category
* Effective date
* Expiry date
* Promotion
* Seller type
* Policy ID

Do not invent metadata that cannot be supported by the source.

### Experiment

Compare retrieval behaviour such as:

```text
Query
 ↓
Semantic retrieval
```

versus:

```text
Query
 ↓
Semantic retrieval + metadata constraints
 ↓
Evidence
```

Investigate cases where semantic similarity can retrieve a plausible but incorrect policy.

Examples of useful failure cases:

* Wrong region
* Wrong customer tier
* Wrong policy version
* Expired promotion
* Similar but different product/category

### Deliverables

```text
representations/text_metadata/
├── README.md
├── your implementation files
└── tests/
```

### README should explain

* Metadata schema
* Why each metadata field exists
* How metadata is generated
* How metadata is used during retrieval
* Examples where metadata helps
* Examples where metadata does not help
* Retrieval results
* Limitations

### Do not

* Invent metadata
* Hardcode answers
* Create a separate dataset
* Create a separate application
* Change the common contract without approval

---

# 6. Pair 3 — Structured Data

### Assigned area

```text
representations/structured/
```

### Objective

Represent naturally structured parts of the handbook as structured entities and relationships.

The main question is:

> Which questions are easier to answer when knowledge is represented explicitly as structured data?

### Possible entities

Investigate entities such as:

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

Do not automatically turn every sentence into a database row.

Identify information that naturally benefits from structured representation.

### Preferred technology

PostgreSQL is preferred, but the team may discuss alternatives if there is a strong reason.

### You should investigate

* Entity identification
* Primary keys
* Foreign keys
* Relationships
* Normalization
* Constraints
* SQL querying
* Multi-table queries
* Traceability back to the source

### Important question

Determine which benchmark questions can be answered efficiently using structured queries.

For example:

```text
Customer
    ↓
Tier
    ↓
Policy
    ↓
Region
```

This may require joining multiple entities.

### Deliverables

```text
representations/structured/
├── README.md
├── schema.sql
├── your implementation files
└── tests/
```

### README should explain

* Entities identified
* Relationships
* Schema design
* Why the schema was designed this way
* Example SQL queries
* Retrieval examples
* Results
* Limitations

### Do not

* Hardcode benchmark answers
* Create artificial relationships
* Put every sentence into a table
* Create a separate dataset
* Change the shared evidence contract without approval

---

# 7. Pair 4 — Knowledge Graph

### Assigned area

```text
representations/graph/
```

### Objective

Represent entities and relationships explicitly as a graph.

The main question is:

> Can graph structure improve retrieval for relationship-heavy and multi-hop questions?

### Possible entities

Investigate:

```text
Customer
Tier
Product
Category
Manufacturer
Seller
Policy
Promotion
Region
Order
Support Case
Escalation Level
```

### Possible relationships

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

These are examples of relationships to investigate, not instructions to invent relationships.

Only create relationships supported by the source.

### Focus especially on

* One-hop questions
* Two-hop questions
* Multi-hop questions
* Relationship traversal
* Entity disambiguation
* Source traceability

### Example reasoning pattern

A question may require:

```text
Product
   ↓
Category
   ↓
Promotion
   ↓
Policy
   ↓
Region
```

The graph should make these relationships explicit.

### Deliverables

```text
representations/graph/
├── README.md
├── your implementation files
└── tests/
```

### README should explain

* Graph schema
* Entity types
* Relationship types
* Why graph representation is useful
* Example traversals
* Multi-hop examples
* Retrieval results
* Limitations

### Do not

* Invent relationships
* Hardcode answers
* Create a separate dataset
* Create a separate application
* Modify shared interfaces without approval

---

# 8. Common Requirement — Evidence

Every retrieval implementation must eventually produce evidence that can be passed to the common RAG pipeline.

Conceptually:

```text
Evidence
├── content
├── source_id
├── score
└── metadata
```

The exact internal implementation is up to each team.

The final system should be able to answer:

> "Where did this evidence come from?"

Source traceability is therefore important.

---

# 9. What Every Pair Must Learn

By the end of the implementation, every pair should be able to explain:

### 1. What did you represent?

Example:

> "We represented the handbook as..."

### 2. Why did you represent it this way?

Explain the problem your representation solves.

### 3. What information became easier to retrieve?

Give concrete examples.

### 4. What became harder?

Discuss limitations honestly.

### 5. Which benchmark questions benefited?

Use actual evaluation questions.

### 6. Which questions failed?

Failure cases are important.

### 7. How did you measure performance?

Discuss appropriate retrieval metrics and latency.

### 8. How is the evidence traced back to the source?

This is required for trustworthy RAG.

---

# 10. Important Team Principle

Do not try to prove that your technique is "the best."

The objective is to understand:

```text
Where does this approach work?
Where does it fail?
Why does it behave that way?
```

A useful failure is as valuable as a successful example because it helps us understand the trade-offs between approaches.

---

# 11. Integration Requirement

Each pair works independently during development.

The final system will integrate the implementations through the shared project interfaces.

Conceptually:

```text
                 ┌── Text
                 │
NovaMart ────────┼── Text + Metadata
                 │
                 ├── Structured
                 │
                 └── Knowledge Graph
                          ↓
                    Common Evidence
                          ↓
                     Evaluation
                          ↓
                         LLM
                          ↓
                        Answer
```

The final application will allow us to compare these approaches using the same questions.

---

# 12. Final Deliverable From Each Pair

Before requesting a Pull Request, your assigned area should contain:

```text
Implementation
Tests
README
Examples
Experimental findings
Known limitations
```

The implementation does not need to be perfect.

It needs to be:

* Understandable
* Reproducible
* Testable
* Compatible with the common architecture
* Based on the common NovaMart dataset
* Supported by experimental evidence
