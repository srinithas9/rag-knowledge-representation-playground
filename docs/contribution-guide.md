# Contribution Guide

## 1. Purpose

This guide explains how team members should contribute to the **RAG Knowledge Representation & Retrieval Playground**.

The project is intentionally divided into independent modules so that multiple people can work in parallel without breaking the shared architecture.

The basic workflow is:

```text
Research
   ↓
Design
   ↓
Implement
   ↓
Test
   ↓
Experiment
   ↓
Document
   ↓
Pull Request
   ↓
Review
   ↓
Merge
```

The project is divided into two main implementation phases:

```text
Phase 1
Representation → Storage → Basic/Native Retrieval → Evidence[]

Phase 2
Advanced Retrieval → Cross-Representation Experiments
→ Common Evaluation → LLM → Answer
```

---

# 2. Before You Start

Every team member should understand these project principles before writing code.

### Same Source

All teams use the same NovaMart source dataset.

### Same Benchmark

All teams use the same 40 evaluation questions and ground truth.

### Same Evidence Contract

All retrieval implementations return the common `Evidence` format.

### No Hardcoded Answers

The implementation must retrieve information from the representation rather than returning benchmark answers directly.

### Representation ≠ Retrieval

Knowledge representation and retrieval are separate concepts.

For example:

```text
Text Representation
        ↓
Storage / Index
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

### Compare, Don't Assume

The purpose is to understand the strengths and weaknesses of different approaches, not to prove that one technique is always better.

---

# 3. Repository Structure

```text
rag-knowledge-representation-playground/
│
├── data/
├── shared/
├── representations/
├── retrieval/
├── evaluation/
├── app/
└── docs/
```

### `data/`

Common source data, normalized data, evaluation questions, ground truth, and benchmark information.

### `shared/`

Common interfaces, schemas, configuration, and registries.

### `representations/`

Implementation of the four knowledge representation approaches.

### `retrieval/`

Shared retrieval strategy implementations and Phase 2 retrieval experiments.

### `evaluation/`

Metrics, evaluation logic, and experiment results.

### `app/`

Final integrated application.

### `docs/`

Project architecture, contribution rules, and team assignments.

---

# 4. Team Ownership

Each pair owns its assigned representation module.

```text
Pair 1 → representations/text/
Pair 2 → representations/text_metadata/
Pair 3 → representations/structured_table/
Pair 4 → representations/knowledge_graph/
```

Each pair owns its representation **end-to-end for Phase 1**.

This means the pair is responsible for:

```text
Understand Source
      ↓
Design Representation
      ↓
Transform Data
      ↓
Store / Index
      ↓
Basic / Native Retrieval
      ↓
Evidence[]
```

Teams are responsible for:

* Research
* Technical design
* Representation implementation
* Storage/index implementation
* Basic/native retrieval
* Unit tests
* Representation-level experiments
* Failure analysis
* Documentation

The project lead owns the integration and shared areas.

---

# 5. Shared Areas

The following areas are shared project infrastructure:

```text
shared/
data/
evaluation/
app/
docs/architecture.md
```

The following is also a shared Phase 2 area:

```text
retrieval/
```

Do not modify shared infrastructure casually.

In particular, do not change:

```text
shared/interfaces.py
shared/schemas.py
shared/config.py
shared/registry.py
```

without coordinating with the project lead.

These files define contracts used by multiple parts of the project.

---

# 6. Dataset Rules

The common dataset is part of the project's experimental control.

Teams must not:

* Modify the source handbook
* Change the normalized dataset
* Add private benchmark questions
* Remove evaluation questions
* Modify ground truth to improve results
* Create a separate competing dataset

If a genuine data issue is discovered, report it to the project lead.

The benchmark currently contains:

```text
40 evaluation questions
40 ground-truth entries
```

All teams should evaluate against the same benchmark.

---

# 7. Git Workflow

Do not work directly on `main`.

Each pair should create a feature branch.

Examples:

```text
feature/text-representation
feature/text-metadata
feature/structured
feature/knowledge-graph
```

Create a branch:

```bash
git checkout -b feature/<your-feature>
```

Check the current branch:

```bash
git branch
```

The active branch should be your feature branch.

---

# 8. Before Starting Work

Always synchronize with `main` before starting new work.

```bash
git checkout main
git pull origin main
```

Then create or update your feature branch.

If your feature branch already exists:

```bash
git checkout feature/<your-feature>
git merge main
```

Resolve conflicts carefully if they occur.

---

# 9. Development Workflow

## Step 1 — Research

Understand the technique before implementing it.

Research questions should include:

* What problem does this technique solve?
* How does it represent knowledge?
* Where is the knowledge stored?
* How does basic/native retrieval work?
* What assumptions does it make?
* What are its strengths?
* What are its weaknesses?
* What types of queries should it handle well?
* What types of queries might cause failure?

---

## Step 2 — Design

Before coding, decide:

* Input format
* Internal representation
* Storage/index
* Basic/native retrieval method
* Metadata requirements
* Output format
* Testing approach
* Experiment design

The design should remain compatible with the project's shared interfaces.

---

## Step 3 — Implement

Implement only within your assigned representation module unless a shared change has been discussed.

Your Phase 1 implementation should cover:

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

Do not implement every possible retrieval strategy independently.

For example, the Text pair does not need to independently build keyword, semantic, hybrid, and reranking systems.

Advanced retrieval comparisons belong primarily to Phase 2.

Keep implementation modular.

Avoid hardcoding answers for evaluation questions.

---

# 10. How to Test Your Representation

The main Phase 1 output is **retrieved evidence**, not an LLM answer.

Use this flow:

```text
Source
   ↓
Representation
   ↓
Storage
   ↓
Question
   ↓
Basic / Native Retrieval
   ↓
Top-K Evidence
   ↓
Compare with Ground Truth
```

For each representation, inspect:

* Was the relevant information retrieved?
* Was it ranked appropriately?
* Is the evidence complete?
* Can it be traced to the source?
* Was irrelevant information retrieved?
* Was an important constraint missed?
* Was an outdated policy retrieved?
* Did chunking/entity design affect retrieval?
* Did the representation make the query difficult?

### LLM is not required for Phase 1

Do not depend on the LLM to prove that your retrieval works.

The important Phase 1 question is:

> **Can our representation retrieve the right evidence?**

The LLM comes later:

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

This prevents a plausible LLM answer from hiding a retrieval failure.

---

# 11. Phase 1 vs Phase 2 Responsibilities

## Phase 1 — Representation Readiness

Each pair owns:

```text
Representation
      +
Storage / Index
      +
Basic / Native Retrieval
      ↓
Evidence[]
```

Examples:

### Text

```text
Text chunks
   ↓
Text storage/index
   ↓
Basic text retrieval
```

### Text + Metadata

```text
Text + metadata
   ↓
Metadata-aware storage/index
   ↓
Basic text + metadata filtering
```

### Structured

```text
Tables / entities
   ↓
PostgreSQL
   ↓
SQL retrieval
```

### Knowledge Graph

```text
Nodes + relationships
   ↓
Graph store
   ↓
Basic graph traversal
```

---

## Phase 2 — Retrieval Experiments

Phase 2 focuses on advanced retrieval and cross-representation comparison.

Potential retrieval strategies include:

```text
Keyword
Vector / Semantic
Hybrid
Metadata Filtering
Reranking
SQL / Structured Retrieval
Graph Traversal
```

Not every retrieval strategy applies to every representation.

Examples:

| Representation  | Applicable retrieval examples               |
| --------------- | ------------------------------------------- |
| Text            | Keyword, Vector, Hybrid                     |
| Text + Metadata | Keyword, Vector, Hybrid, Metadata Filtering |
| Structured      | SQL / Structured Retrieval                  |
| Knowledge Graph | Graph Traversal                             |

The goal is to compare **meaningful combinations**, not force every strategy onto every representation.

---

# 12. Testing

Every implementation should include meaningful tests.

Tests should verify things such as:

* Data loading
* Representation creation
* Storage/index creation
* Basic/native retrieval
* Evidence format
* Source traceability
* Edge cases
* Failure cases

Run:

```bash
python -m pytest
```

before creating a Pull Request.

---

# 13. Evidence Contract

Retrievers must return:

```python
@dataclass
class Evidence:
    content: str
    source_id: str
    score: float
    metadata: dict[str, Any]
```

### `content`

Retrieved information.

### `source_id`

Identifier that allows the evidence to be traced back to the source.

### `score`

Retrieval relevance score when available.

### `metadata`

Additional information useful for tracing or analysis.

The common format allows different implementations to be evaluated using the same evaluation layer.

---

# 14. Retrieval Interface

Retrievers should follow:

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

Teams should not create incompatible retrieval APIs for individual modules.

If the interface is insufficient for a legitimate use case, discuss the requirement before changing the shared interface.

---

# 15. Experiments

Phase 1 experiments should verify that the representation and its basic/native retrieval path work.

Teams should record:

* Configuration
* Representation design
* Storage/index
* Retrieval method
* Top-K
* Relevant source IDs
* Retrieved source IDs
* Retrieval latency
* Relevant metrics
* Failure cases
* Observations

Phase 2 experiments will compare applicable retrieval strategies across representations using the common evaluation framework.

The objective is to understand **why** a method succeeds or fails.

Do not report only a single aggregate score.

---

# 16. Failure Analysis

Teams should identify representative failure cases.

Examples:

```text
Wrong policy version
Wrong region
Wrong customer tier
Near-match entity
Missed exception
Incomplete multi-hop relationship
Irrelevant evidence
Insufficient evidence
Poor chunking
Missing metadata
Incorrect entity/relationship modeling
```

For each important failure, explain:

```text
Query
↓
Expected evidence
↓
Retrieved evidence
↓
What went wrong?
↓
Why did the approach behave this way?
```

The purpose is to understand the behavior of the representation and retrieval approach.

---

# 17. Documentation Requirements

Each representation module should contain a README.

A team README should explain:

### 1. Approach

What representation was implemented?

### 2. Design

How is the knowledge represented?

### 3. Storage

Where and how is the representation stored/indexed?

### 4. Basic Retrieval

How is evidence retrieved in Phase 1?

### 5. Integration

How does the module use the common interfaces?

### 6. Experiments

What experiments were performed?

### 7. Results

What was observed?

### 8. Failure Cases

Where did the approach struggle?

### 9. Limitations

What are the known limitations?

---

# 18. Code Quality

Keep code:

* Modular
* Readable
* Testable
* Documented where necessary
* Consistent with the project's interfaces

Avoid:

* Hardcoded benchmark answers
* Duplicated datasets
* Unnecessary dependencies
* Representation-specific logic in shared code
* Unexplained magic values
* Large monolithic files

---

# 19. Dependencies

Before adding a new dependency, check whether it is genuinely required.

Do not introduce libraries simply because they are popular.

If a new dependency is necessary:

1. Explain why it is needed.
2. Add it to `requirements.txt`.
3. Ensure the project still installs correctly.
4. Inform the project lead.

---

# 20. Commits

Keep commits focused.

Good:

```bash
git commit -m "Implement text chunking"
```

```bash
git commit -m "Add text retrieval tests"
```

```bash
git commit -m "Document chunking experiments"
```

Avoid vague commits such as:

```text
update
changes
final
test
stuff
```

---

# 21. Push Your Branch

After committing:

```bash
git push -u origin feature/<your-feature>
```

For later pushes:

```bash
git push
```

---

# 22. Pull Request

Create a Pull Request from:

```text
feature/<your-feature>
```

into:

```text
main
```

The Pull Request should explain:

* What was implemented
* Why the design was chosen
* What was tested
* What experiments were performed
* What was learned
* Known limitations

For Phase 1, also include:

* Representation approach
* Storage/index approach
* Basic/native retrieval approach
* Example retrieved evidence
* Source traceability
* Representative failure cases

---

# 23. Pull Request Checklist

Before requesting review:

```text
[ ] Correct feature branch used
[ ] No changes to shared data
[ ] No hardcoded benchmark answers
[ ] Common interfaces followed
[ ] Evidence objects contain source IDs
[ ] Representation is documented
[ ] Storage/index is documented
[ ] Basic/native retrieval works
[ ] Tests added
[ ] Tests pass
[ ] Experiments documented
[ ] Failure cases documented
[ ] README updated
[ ] No unnecessary dependencies
[ ] Code is limited to the assigned area
```

---

# 24. Keeping Your Branch Updated

The `main` branch may receive changes from other teams.

Before continuing significant work:

```bash
git checkout main
git pull origin main
```

Then update your feature branch:

```bash
git checkout feature/<your-feature>
git merge main
```

Resolve conflicts carefully.

Do not overwrite another team's work.

---

# 25. What Requires Project Lead Approval?

Coordinate before changing:

```text
shared/interfaces.py
shared/schemas.py
shared/config.py
shared/registry.py
data/
evaluation/
app/
retrieval/
docs/architecture.md
```

A shared change can affect multiple teams, so it should be discussed before implementation.

---

# 26. Definition of Done

A Phase 1 representation contribution is considered complete when:

```text
Research
   ↓
Design
   ↓
Representation
   ↓
Storage / Index
   ↓
Basic / Native Retrieval
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

The code working locally is **not the only definition of done**.

The team should also be able to explain:

> What did we build?

> Why did we design it this way?

> How is the knowledge represented?

> Where is it stored?

> How does basic retrieval work?

> What evidence does it retrieve?

> What queries does it handle well?

> Where does it fail?

> What did we learn?

---

# 27. Final Principle

This project is a learning and comparison environment.

The goal is not:

> "Our technique is the best."

The goal is:

> **"We understand how this technique represents knowledge, how it stores and retrieves evidence, what kinds of questions it handles well, where it fails, and why."**

A successful contribution is therefore:

> **working implementation + meaningful evidence + meaningful understanding.**
