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

Retrieval strategy implementations.

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

Teams are responsible for:

* Research
* Technical design
* Implementation
* Unit tests
* Experiments
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

Do not modify these areas casually.

In particular, do not change:

```text
shared/interfaces.py
shared/schemas.py
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
* How does retrieval work?
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
* Retrieval method
* Metadata requirements
* Output format
* Testing approach
* Experiment design

The design should remain compatible with the project's shared interfaces.

---

## Step 3 — Implement

Implement only within your assigned module unless a shared change has been discussed.

Keep implementation modular.

Avoid hardcoding answers for evaluation questions.

---

## Step 4 — Test

Every implementation should include meaningful tests.

Tests should verify things such as:

* Data loading
* Representation creation
* Retrieval behavior
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

# 10. Evidence Contract

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

# 11. Retrieval Interface

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

# 12. Experiments

Experiments should use the common benchmark.

Teams should record:

* Configuration
* Retrieval method
* Top-K
* Relevant source IDs
* Retrieved source IDs
* Retrieval latency
* Relevant metrics
* Failure cases
* Observations

The objective is to understand **why** a method succeeds or fails.

Do not report only a single aggregate score.

---

# 13. Failure Analysis

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

---

# 14. Documentation Requirements

Each representation module should contain a README.

A team README should explain:

### 1. Approach

What representation or retrieval technique was implemented?

### 2. Design

How is the knowledge represented and stored?

### 3. Retrieval

How is relevant evidence retrieved?

### 4. Integration

How does the module use the common interfaces?

### 5. Experiments

What experiments were performed?

### 6. Results

What was observed?

### 7. Failure Cases

Where did the approach struggle?

### 8. Limitations

What are the known limitations?

---

# 15. Code Quality

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

# 16. Dependencies

Before adding a new dependency, check whether it is genuinely required.

Do not introduce libraries simply because they are popular.

If a new dependency is necessary:

1. Explain why it is needed.
2. Add it to `requirements.txt`.
3. Ensure the project still installs correctly.
4. Inform the project lead.

---

# 17. Commits

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

# 18. Push Your Branch

After committing:

```bash
git push -u origin feature/<your-feature>
```

For later pushes:

```bash
git push
```

---

# 19. Pull Request

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

---

# 20. Pull Request Checklist

Before requesting review:

```text
[ ] Correct feature branch used
[ ] No changes to shared data
[ ] No hardcoded benchmark answers
[ ] Common interfaces followed
[ ] Evidence objects contain source IDs
[ ] Tests added
[ ] Tests pass
[ ] Experiments documented
[ ] Failure cases documented
[ ] README updated
[ ] No unnecessary dependencies
[ ] Code is limited to the assigned area
```

---

# 21. Keeping Your Branch Updated

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

# 22. What Requires Project Lead Approval?

Coordinate before changing:

```text
shared/interfaces.py
shared/schemas.py
shared/config.py
shared/registry.py
data/
evaluation/
app/
docs/architecture.md
```

A shared change can affect multiple teams, so it should be discussed before implementation.

---

# 23. Definition of Done

A team contribution is considered complete when:

```text
Research
   ↓
Design
   ↓
Implementation
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

> What evidence does it retrieve?

> What queries does it handle well?

> Where does it fail?

> What did we learn?

---

# 24. Final Principle

This project is a learning and comparison environment.

The goal is not:

> "Our technique is the best."

The goal is:

> **"We understand how this technique represents knowledge, how it retrieves evidence, what kinds of questions it handles well, where it fails, and why."**

A successful contribution is therefore one that produces both:

**working implementation + meaningful understanding.**
