# Contribution Guide

## 1. Purpose

This guide explains how team members should contribute to the **RAG Knowledge Representation & Retrieval Playground**.

The project is a controlled experimentation environment for studying how different knowledge representations and retrieval approaches affect the evidence available to an LLM.

The central principle is:

```text
SAME KNOWLEDGE
      ↓
Different Representations / Retrieval Approaches
      ↓
SAME QUESTIONS
      ↓
Retrieved Evidence
      ↓
Common LLM
      ↓
Answers
      ↓
Evaluation & Comparison
```

The goal is not to prove that one technique is always best.

The goal is to understand:

* How the technique represents knowledge.
* How it stores or indexes that knowledge.
* How it retrieves evidence.
* Which questions it handles well.
* Where it fails.
* Why it succeeds or fails.
* How retrieved evidence affects the final answer.

---

# 2. Project Principles

Every team member must follow these principles.

## Same Source

All teams use the same NovaMart source knowledge.

Do not create a different version of the dataset for your pipeline.

---

## Same Benchmark

All teams use the same official benchmark:

```text
40 evaluation questions
40 ground-truth entries
```

The benchmark must remain unchanged.

Teams may create additional development or exploratory questions for testing, but these must not replace or modify the official benchmark.

---

## No Hardcoded Answers

Do not hardcode benchmark answers into the implementation.

The system must retrieve information from the implemented knowledge representation.

Bad:

```python
if query == "What is the refund period?":
    return "60 days"
```

Correct:

```text
Question
   ↓
Pipeline
   ↓
Representation
   ↓
Retrieval
   ↓
Evidence
```

---

## Common Evidence Contract

Every pipeline must ultimately return the common `Evidence` structure.

Conceptually:

```text
Evidence
├── content
├── source_id
├── score
└── metadata
```

This allows the integration and evaluation layers to compare different pipelines consistently.

---

## Representation and Retrieval

Representation and retrieval are distinct concepts, but they are intentionally owned together inside each pipeline.

The reason is that the appropriate retrieval method depends on how the knowledge is represented.

For example:

```text
Text
   ↓
Chunk / text index
   ↓
Keyword / dense / hybrid retrieval
```

while:

```text
Structured Data
   ↓
PostgreSQL
   ↓
SQL retrieval
```

and:

```text
Knowledge Graph
   ↓
Graph Store
   ↓
Graph traversal / graph query
```

Do not force the same retrieval technique onto every representation.

---

# 3. Repository Structure

The repository is organized into vertical pipelines.

```text
rag-knowledge-representation-playground/
│
├── data/
│
├── shared/
│
├── pipelines/
│   ├── text/
│   ├── metadata/
│   ├── structured/
│   └── graph/
│
├── llm/
│
├── evaluation/
│
├── integration/
│
├── app/
│
└── docs/
```

---

# 4. Pipeline Structure

Each pair owns one complete pipeline.

The expected structure is:

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

The exact internal implementation can differ between pipelines.

The important requirement is that each pipeline provides the required functionality and follows the common project contracts.

---

# 5. Pipeline Ownership

The four pairs are assigned as follows:

```text
Pair 1 → pipelines/text/

Pair 2 → pipelines/metadata/

Pair 3 → pipelines/structured/

Pair 4 → pipelines/graph/
```

Each pair owns its assigned pipeline end-to-end.

The expected flow is:

```text
NovaMart Source
      ↓
Representation
      ↓
Storage / Index
      ↓
Retrieval
      ↓
Evidence
      ↓
Pipeline Evaluation
```

The pair is responsible for:

* Understanding the source data relevant to its approach.
* Designing the representation.
* Building the representation.
* Choosing appropriate storage or indexing.
* Implementing appropriate retrieval.
* Returning common `Evidence`.
* Testing the pipeline.
* Running experiments.
* Recording failure cases.
* Documenting design decisions.
* Maintaining its pipeline README.

---

# 6. Pair Boundaries

Pairs should work primarily inside their assigned folder.

### Pair 1

```text
pipelines/text/
```

### Pair 2

```text
pipelines/metadata/
```

### Pair 3

```text
pipelines/structured/
```

### Pair 4

```text
pipelines/graph/
```

Do not modify another pair's pipeline without coordination.

Do not move another pair's files.

Do not redesign another pair's implementation.

If two pipelines need shared functionality, discuss it with the project lead before changing shared code.

---

# 7. Shared Areas

The following are shared project infrastructure:

```text
data/
shared/
evaluation/
integration/
llm/
app/
docs/architecture.md
docs/contribution-guide.md
docs/team-assignments.md
```

These areas should not be modified casually.

In particular, coordinate before changing:

```text
shared/schemas.py
shared/interfaces.py
shared/config.py
```

or any integration contract.

A shared change can affect multiple pipelines.

---

# 8. Dataset Rules

The NovaMart dataset is part of the controlled experiment.

Teams must not:

* Modify the source handbook.
* Modify the normalized source data.
* Change the official evaluation questions.
* Modify ground truth.
* Remove benchmark questions.
* Create a private competing dataset.
* Hardcode benchmark answers.

If a genuine data problem is discovered:

```text
Identify issue
     ↓
Document issue
     ↓
Inform project lead
     ↓
Discuss before changing anything
```

Do not silently modify the dataset.

---

# 9. Before Starting Implementation

Every pair must first understand:

```text
1. What problem does our representation solve?

2. Why is this representation useful?

3. What NovaMart information maps naturally to it?

4. What information does it represent poorly?

5. What storage/index is appropriate?

6. What retrieval method is appropriate?

7. Which benchmark questions should benefit?

8. Which questions might fail?

9. How will evidence be traced to the source?

10. What experiments will demonstrate the trade-offs?
```

Do not start by blindly implementing a library tutorial.

Understand the problem first.

---

# 10. Research Phase

Before implementation, research the assigned technology.

Answer:

* What is the technique?
* What problem does it solve?
* How does it represent knowledge?
* How is the knowledge stored?
* How is retrieval performed?
* What assumptions does it make?
* What are its strengths?
* What are its weaknesses?
* What types of questions should it handle well?
* What types of questions might cause failure?
* What alternatives were considered?
* Why was the chosen approach selected?

The goal is not to collect theory.

The goal is to make a defensible engineering decision.

---

# 11. Design Phase

Before coding, each pair should define:

```text
Source Input
      ↓
Representation
      ↓
Storage / Index
      ↓
Retrieval
      ↓
Evidence
      ↓
Evaluation
```

The design should specify:

* Input data.
* Representation structure.
* Storage/index.
* Retrieval method.
* Query handling.
* Top-K behavior where applicable.
* Metadata requirements.
* Source traceability.
* Error handling.
* Testing approach.
* Experiment approach.

---

# 12. Implementation Phase

Implement only within the assigned pipeline unless a shared change has been approved.

The pipeline should provide a complete path:

```text
NovaMart Knowledge
      ↓
Representation
      ↓
Storage / Index
      ↓
Retrieval
      ↓
Evidence
```

The exact implementation is up to the pair.

For example, the Text pipeline may use:

```text
Policy text
   ↓
Semantic chunks
   ↓
Text/vector index
   ↓
Dense / keyword / hybrid retrieval
   ↓
Evidence
```

The Structured pipeline may use:

```text
Entities / relationships
   ↓
PostgreSQL
   ↓
SQL retrieval
   ↓
Evidence
```

The Graph pipeline may use:

```text
Entities + relationships
   ↓
Graph store
   ↓
Graph traversal/query
   ↓
Evidence
```

These implementations do not need to be identical.

---

# 13. Retrieval Strategy

Each pair should choose retrieval that is appropriate for its representation.

Do not implement every retrieval technique just because it exists.

Potential retrieval approaches across the project include:

```text
Keyword / BM25
Dense / Semantic
Hybrid
Metadata Filtering
Reranking
SQL / Structured Retrieval
Graph Traversal
```

Not every approach applies to every pipeline.

For example:

| Pipeline   | Possible retrieval approaches                 |
| ---------- | --------------------------------------------- |
| Text       | Keyword, dense, hybrid, reranking             |
| Metadata   | Dense + metadata filtering, hybrid, reranking |
| Structured | SQL / relational retrieval                    |
| Graph      | Graph traversal / graph queries               |

The goal is to create **meaningful representation + retrieval combinations**.

---

# 14. Common Evidence Contract

Retrieval results must ultimately be represented using:

```python
@dataclass
class Evidence:
    content: str
    source_id: str
    score: float
    metadata: dict[str, Any]
```

### `content`

The actual information retrieved from the pipeline.

### `source_id`

An identifier that allows the evidence to be traced back to the NovaMart source.

### `score`

The retrieval relevance score when the underlying method provides one.

If the retrieval method does not naturally produce a comparable score, the implementation should document how the returned score is interpreted.

Do not invent a misleading confidence score simply to fill the field.

### `metadata`

Additional information useful for tracing, debugging, filtering, or analysis.

Examples may include:

```text
policy_id
region
customer_tier
chunk_id
table
entity
relationship
retrieval_method
```

Only include metadata that is actually supported by the implementation.

---

# 15. Source Traceability

Every retrieved evidence item should be traceable to the common NovaMart knowledge.

The project should be able to answer:

> Where did this evidence come from?

For example:

```text
Query
  ↓
Evidence
  ↓
source_id
  ↓
NovaMart source
```

Internal IDs such as:

```text
chunk_17
row_42
node_103
```

may be used, but they should be traceable back to the source.

---

# 16. Evaluation

The project evaluates retrieval separately from final answer generation.

The primary pipeline question is:

> **Did we retrieve the evidence required to answer the question?**

Relevant retrieval metrics may include:

* Recall@K
* Precision@K
* MRR
* nDCG@K where appropriate
* Retrieval latency
* Evidence coverage

Do not blindly calculate every metric.

Use metrics appropriate to the retrieval approach.

The official benchmark provides the common basis for comparison.

---

# 17. Development Questions vs Official Benchmark

The official 40 questions are the controlled benchmark.

They are not the only questions a pair should use during development.

Pairs should also test:

* Additional questions.
* Edge cases.
* Unseen questions.
* Boundary cases.
* Failure cases.
* Representation-specific questions.

The distinction is:

```text
Development
    ↓
Open-ended experimentation
    ↓
Improve and understand pipeline

Formal Evaluation
    ↓
Same 40 benchmark questions
    ↓
Fair comparison
```

Do not optimize the implementation by hardcoding behavior for the benchmark.

---

# 18. Failure Analysis

Failures are valuable experimental results.

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

For important failures, document:

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

Do not hide failures simply because they reduce the score.

---

# 19. LLM Responsibility

The common LLM is part of the integrated system.

Individual pairs should focus primarily on producing good retrieved evidence.

Do not use the LLM to hide retrieval problems.

For example:

```text
Retrieval fails
     ↓
LLM somehow produces correct answer
```

This does not mean the retrieval system worked correctly.

The project specifically wants to understand whether the required evidence was actually retrieved.

The integrated system will later evaluate:

```text
Retrieval
   ↓
Evidence
   ↓
LLM
   ↓
Answer
```

---

# 20. Testing Requirements

Each pipeline must contain meaningful tests.

Tests should cover appropriate parts of:

```text
Data loading
Representation creation
Storage/index creation
Retrieval
Evidence generation
Source traceability
Edge cases
Failure cases
```

Run:

```bash
python -m pytest
```

before creating a Pull Request.

Do not submit a pipeline with only placeholder tests.

---

# 21. README Requirements

Each pipeline must maintain its own:

```text
pipelines/<pipeline-name>/README.md
```

The README should explain:

### 1. Problem

What problem does this pipeline investigate?

### 2. Representation

How is NovaMart knowledge represented?

### 3. Storage / Index

Where and how is the representation stored?

### 4. Retrieval

How is evidence retrieved?

### 5. Design Decisions

Why were these choices made?

### 6. Experiments

What experiments were performed?

### 7. Results

What was observed?

### 8. Failure Cases

Where did the pipeline struggle?

### 9. Limitations

What are the known limitations?

### 10. Integration

How does the pipeline return common `Evidence`?

---

# 22. Dependencies

Before adding a dependency, check whether it is genuinely required.

Do not add libraries simply because they are popular.

If a new dependency is necessary:

1. Explain why it is needed.
2. Add it to `requirements.txt`.
3. Verify installation.
4. Test the project.
5. Inform the project lead.

Do not modify dependencies casually because another library happens to be easier.

---

# 23. Git Workflow

Do not work directly on `main`.

Start by synchronizing:

```bash
git checkout main
git pull origin main
```

Create your feature branch:

```bash
git checkout -b feature/<your-feature>
```

Examples:

```text
feature/text-pipeline
feature/metadata-pipeline
feature/structured-pipeline
feature/graph-pipeline
```

Work inside your assigned pipeline.

Commit focused changes:

```bash
git add .
git commit -m "Implement text pipeline retrieval"
```

Push:

```bash
git push -u origin feature/<your-feature>
```

---

# 24. Pull Request

Create the Pull Request from:

```text
feature/<your-feature>
```

into:

```text
main
```

The Pull Request should explain:

* What was implemented.
* Why the design was chosen.
* What representation was used.
* What storage/index was used.
* What retrieval method was used.
* What was tested.
* What experiments were performed.
* What was learned.
* Known limitations.
* Representative failure cases.

---

# 25. Shared Change Approval

Discuss with the project lead before modifying:

```text
data/
shared/
integration/
llm/
evaluation/
app/
docs/architecture.md
docs/team-assignments.md
requirements.txt
```

In particular, coordinate before changing:

```text
shared/schemas.py
shared/interfaces.py
shared/config.py
```

Do not change common contracts independently.

If your pipeline genuinely requires a contract change:

```text
Identify requirement
      ↓
Explain why existing contract is insufficient
      ↓
Discuss with project lead
      ↓
Agree on change
      ↓
Implement change
      ↓
Verify other pipelines
```

---

# 26. Code Quality

Keep code:

* Modular.
* Readable.
* Testable.
* Understandable.
* Documented where necessary.
* Consistent with common project contracts.

Avoid:

* Hardcoded benchmark answers.
* Duplicated datasets.
* Unnecessary dependencies.
* Representation-specific logic inside shared code.
* Unexplained magic values.
* Large monolithic files.
* Changes outside your assigned area.
* Implementations copied without understanding them.

Every pair should be able to explain its own implementation during review.

---

# 27. Commit Quality

Keep commits focused and meaningful.

Good:

```text
Implement policy-boundary text representation
```

```text
Add metadata-filtered retrieval
```

```text
Add structured pipeline tests
```

```text
Document graph traversal experiments
```

Avoid:

```text
update
changes
final
stuff
test
```

---

# 28. Pull Request Checklist

Before requesting review:

```text
[ ] Correct feature branch used
[ ] Work is inside assigned pipeline
[ ] Common dataset is unchanged
[ ] Official benchmark is unchanged
[ ] No hardcoded answers
[ ] Common Evidence contract followed
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
[ ] No unrelated files changed
[ ] Code can be explained by both pair members
```

---

# 29. Definition of Done

A pipeline is ready for integration when:

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
Evidence
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

Both members of the pair should be able to explain:

> What did we build?

> Why did we choose this representation?

> Why did we choose this storage/index?

> Why did we choose this retrieval method?

> How is evidence produced?

> How is evidence traced to the source?

> Which questions does it handle well?

> Where does it fail?

> Why does it fail?

> What did we learn?

---

# 30. Final Principle

We are **not building four unrelated RAG systems**.

We are building one controlled experimentation playground.

The same NovaMart knowledge and the same benchmark questions must pass through different pipelines so that we can understand:

> **How does the way we represent and retrieve knowledge change the evidence available to the LLM, and how does that affect the final answer?**

A successful contribution is therefore:

```text
Working Pipeline
+
Traceable Evidence
+
Meaningful Evaluation
+
Failure Analysis
+
Clear Documentation
+
Understanding
```
