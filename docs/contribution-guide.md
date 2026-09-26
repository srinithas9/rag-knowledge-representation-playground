# Contribution Guide

## 1. Project Overview

This repository is the shared workspace for the **RAG Knowledge Representation & Retrieval Playground**.

The goal is to study how different ways of representing knowledge and different retrieval techniques affect the evidence retrieved by a RAG system.

All team members work from the same source dataset and follow the same integration contracts so that the final implementations can be compared fairly.

---

## 2. Repository Structure

```text
rag-knowledge-representation-playground/
│
├── data/
│   ├── source/          # Original NovaMart source document
│   ├── normalized/     # Normalized source data
│   └── queries/        # Evaluation questions, ground truth and rubric
│
├── shared/              # Common interfaces and schemas
│
├── representations/     # Knowledge representation implementations
│   ├── text/
│   ├── text_metadata/
│   ├── structured/
│   └── graph/
│
├── retrieval/           # Retrieval implementations
│
├── evaluation/          # Common evaluation framework and results
│
├── app/                 # Integrated demo application
│
└── docs/                # Project and team documentation
```

### Important principle

The repository structure defines **boundaries**, not exact implementation details.

Team members are expected to research, design, implement and test their own solutions within their assigned area.

---

## 3. Clone the Repository

Do not download the repository as a ZIP for normal development.

Clone it using Git:

```bash
git clone <REPOSITORY_URL>
cd rag-knowledge-representation-playground
```

Each team member should have their own local clone on their computer.

The local repository is connected to the shared GitHub repository.

---

## 4. Create Your Own Branch

Do not directly develop on `main`.

Create a branch for your assigned work.

Example:

```bash
git checkout -b feature/text-representation
```

Recommended branch names:

```text
feature/text-representation
feature/text-metadata
feature/structured-representation
feature/knowledge-graph
feature/keyword-retrieval
feature/vector-retrieval
feature/hybrid-retrieval
feature/reranking
```

Use a branch that clearly describes the work you are doing.

---

## 5. What You Are Allowed to Modify

You may freely modify:

* Your assigned representation implementation
* Your assigned retrieval implementation
* Tests related to your implementation
* Documentation related to your implementation
* Experimental configuration and results related to your work

You may create additional files inside your assigned area when they are useful.

You are responsible for keeping your implementation understandable, tested and documented.

---

## 6. Files and Areas That Require Coordination

Do not independently change the following:

```text
data/
shared/
evaluation/
app/
docs/architecture.md
```

In particular, do not change:

```text
shared/interfaces.py
shared/schemas.py
```

without discussing the change with the project lead.

These files define the common contract used to integrate all team implementations.

If you believe the shared contract needs improvement, raise the issue with the project lead before modifying it.

---

## 7. Common Evidence Contract

All retrieval implementations must eventually return evidence using the shared `Evidence` schema.

Conceptually:

```text
Evidence
├── content
├── source_id
├── score
└── metadata
```

The internal implementation is your choice.

For example, you may use:

* BM25
* vector search
* SQL
* graph traversal
* hybrid retrieval
* reranking
* other appropriate techniques

However, the output must remain compatible with the project's common interface.

---

## 8. Use the Common Dataset

All teams must use the provided NovaMart dataset.

Do not:

* Replace the dataset
* Create a different benchmark
* Modify the source document
* Invent policy information
* Hardcode answers to evaluation questions

The purpose of the project is to compare different approaches using the **same knowledge source and benchmark**.

---

## 9. Research Before Implementation

Do not simply implement the first approach that comes to mind.

For your assigned area:

1. Understand the representation/retrieval technique.
2. Research relevant implementation approaches.
3. Identify important design decisions.
4. Implement the approach.
5. Test it.
6. Evaluate it.
7. Document what worked and what failed.

Your README should explain important design decisions and their reasoning.

---

## 10. Testing

Every implementation should include appropriate tests.

At minimum, test:

* Basic functionality
* Expected retrieval behaviour
* Empty/invalid inputs where relevant
* Metadata or filters where applicable
* Source traceability
* Integration with the common interface

Run the project tests before submitting your work.

```bash
pytest
```

---

## 11. Commit Your Work

Make focused commits instead of one huge commit.

Example:

```bash
git add representations/text/
git commit -m "Implement text chunking"
```

Another example:

```bash
git add representations/text/tests/
git commit -m "Add text representation tests"
```

Commit messages should describe what changed.

---

## 12. Push Your Branch

Push your branch to GitHub:

```bash
git push -u origin feature/text-representation
```

Your branch will then appear in the shared GitHub repository.

---

## 13. Create a Pull Request

After completing your work:

1. Push your branch.
2. Open GitHub.
3. Create a Pull Request from your branch into `main`.
4. Explain what you implemented.
5. Mention tests performed.
6. Mention important design decisions.
7. Mention known limitations.

Do not merge your own Pull Request unless the project lead has explicitly agreed.

The project lead will review the implementation before it becomes part of `main`.

---

## 14. Keeping Your Branch Updated

Before starting new work, update your local `main`:

```bash
git checkout main
git pull origin main
```

Then update your feature branch from the latest `main` as appropriate.

If you are unsure how to resolve a merge conflict, do not randomly overwrite files. Ask the project lead.

---

## 15. Pull Request Checklist

Before requesting review, confirm:

* [ ] Implementation works
* [ ] Tests pass
* [ ] No hardcoded answers
* [ ] No changes to the source dataset
* [ ] Common interfaces are respected
* [ ] Evidence contains source traceability
* [ ] README/documentation is updated
* [ ] Experimental results are included where applicable
* [ ] No unnecessary dependencies were added
* [ ] No unrelated files were modified
* [ ] Code is reasonably clean and understandable

---

## 16. Core Team Rule

The project has one shared goal:

> **Different implementations, common contract, common benchmark, fair comparison.**

You are encouraged to experiment inside your assigned area.

At the same time, changes that affect the shared architecture must be coordinated so that individual experiments do not break the integrated project.

---

## 17. Ownership

The project lead is responsible for:

* Overall architecture
* Shared interfaces
* Integration
* Evaluation framework
* Demo application
* Final repository structure
* Reviewing Pull Requests

Each pair is responsible for:

* Research
* Implementation
* Testing
* Experiments
* Documentation
* Findings for their assigned area

The final application will integrate the independently developed components into one common playground.
