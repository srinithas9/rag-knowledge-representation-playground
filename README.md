# RAG Knowledge Representation & Retrieval Playground

A hands-on project for understanding how **knowledge representation** and **retrieval strategies** affect the evidence retrieved by a Retrieval-Augmented Generation (RAG) system and, ultimately, the quality of the final answer.

## 🎯 Project Goal

A RAG system can have a strong LLM and still produce poor answers if the **right evidence is not retrieved**.

This project explores a key question:

> **How does the way knowledge is represented and retrieved affect the evidence available to an LLM?**

We use the **same source knowledge, same evaluation questions, and same ground truth** across multiple representations and retrieval approaches so that the results can be compared fairly.

The project focuses on the complete pipeline:

```text
Source Knowledge
      ↓
Parse / Extract
      ↓
Knowledge Representation
      ↓
Storage / Index
      ↓
User Query
      ↓
Retrieval Strategy
      ↓
Relevant Evidence
      ↓
LLM
      ↓
Answer
      ↓
Evaluation
```

---

## 🧠 Key Concepts

### Knowledge Representation

Knowledge representation describes **how the source knowledge is organized** so that it can later be searched or queried.

We compare:

1. **Text / Chunked Text**
2. **Text + Metadata**
3. **Structured Data / Tables**
4. **Knowledge Graph**

### Retrieval

Retrieval describes **how relevant evidence is found from a representation**.

The project explores retrieval approaches such as:

* Keyword retrieval
* Vector / semantic retrieval
* Hybrid retrieval
* Metadata filtering
* Reranking
* Structured querying
* Graph-based retrieval

Representation and retrieval are treated as **separate dimensions**.

For example:

```text
Text Representation
 ├── Keyword Retrieval
 ├── Vector Retrieval
 ├── Hybrid Retrieval
 └── Reranking
```

---

# 📚 Dataset

The project uses a single fictional company and knowledge source:

**Company:** NovaMart

**Source:** `NovaMart Customer & Operations Policy Handbook — 2026`

The dataset contains realistic RAG scenarios involving:

* Customer policies
* Customer tiers
* Refunds and returns
* Products
* Manufacturers
* Sellers
* Orders
* Promotions
* Regions
* Policy versions
* Effective dates
* Exceptions
* Multi-hop relationships
* Policy precedence
* Near-match and ambiguity cases

The normalized dataset is available under:

```text
data/
├── source/
├── normalized/
└── queries/
```

### Important Benchmark Rule

All approaches use the **same source dataset**.

The evaluation benchmark contains:

* **40 evaluation questions**
* **40 ground-truth entries**
* Evaluation rubric
* Benchmark audit

The benchmark is shared across all teams to make comparisons meaningful.

> Teams must not modify the shared source dataset, evaluation questions, or ground truth.

---

# 🏗️ Project Structure

```text
rag-knowledge-representation-playground/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── source/
│   ├── normalized/
│   └── queries/
│
├── shared/
│   ├── __init__.py
│   ├── interfaces.py
│   ├── schemas.py
│   ├── config.py
│   └── registry.py
│
├── representations/
│   ├── text/
│   ├── text_metadata/
│   ├── structured_table/
│   └── knowledge_graph/
│
├── retrieval/
│   ├── keyword/
│   ├── vector/
│   ├── hybrid/
│   ├── metadata/
│   ├── reranking/
│   ├── structured/
│   └── graph/
│
├── evaluation/
│   ├── evaluator.py
│   ├── metrics.py
│   ├── README.md
│   └── results/
│
├── app/
│   ├── README.md
│   ├── backend/
│   └── frontend/
│
└── docs/
    ├── architecture.md
    ├── contribution-guide.md
    └── team-assignments.md
```

---

# 👥 Team Structure

The project is divided into four representation teams.

| Pair   | Representation      | Main Question                                                                              |
| ------ | ------------------- | ------------------------------------------------------------------------------------------ |
| Pair 1 | Text / Chunked Text | How does chunking affect retrieval?                                                        |
| Pair 2 | Text + Metadata     | Can metadata constraints improve retrieval when semantic similarity is insufficient?       |
| Pair 3 | Structured Data     | Which questions become easier when knowledge is represented as entities and relationships? |
| Pair 4 | Knowledge Graph     | Can graph structure improve relationship-heavy and multi-hop retrieval?                    |

Each pair owns its assigned representation module, experiments, tests, and documentation.



---

# 🔌 Common Interface

All approaches must integrate with the same evidence contract.

```python
@dataclass
class Evidence:
    content: str
    source_id: str
    score: float
    metadata: dict[str, Any]
```

Retrievers follow a common interface:

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

This allows the application and evaluation layer to compare different approaches without knowing their internal implementation details.

---

# 🔬 Evaluation

The project follows an **evidence-first evaluation approach**.

Instead of only asking:

> "Did the LLM give the correct answer?"

we examine the complete chain:

```text
Query
 ↓
Expected Evidence
 ↓
Was the correct evidence retrieved?
 ↓
Was the evidence sufficient?
 ↓
Did the answer use the evidence?
 ↓
Was the final answer correct?
```

### Retrieval Metrics

Depending on the representation and experiment, evaluation may include:

* Precision@K
* Recall@K
* MRR
* nDCG@K
* Retrieval latency

### Evidence Quality

We also examine:

* Required source IDs retrieved
* Evidence sufficiency
* Source traceability
* Irrelevant evidence
* Missing evidence

### Answer Quality

The final RAG response can be evaluated for:

* Correctness
* Groundedness / faithfulness
* Evidence support

---

# 🧪 Important Failure Cases

The benchmark intentionally includes cases where retrieval quality matters.

Examples include:

* Semantic near-matches
* Incorrect policy versions
* Region-specific rules
* Customer-tier differences
* Product-specific exceptions
* Policy precedence
* Multi-hop relationships
* Expired promotions
* Similar but incorrect entities
* Incomplete evidence
* Irrelevant evidence overload

These cases help us understand **where and why a retrieval approach fails**.

---

# 🔄 Development Workflow

Each pair works independently on a feature branch.

Example:

```text
main
│
├── feature/text-representation
├── feature/text-metadata
├── feature/structured
└── feature/knowledge-graph
```

Basic workflow:

```bash
git checkout -b feature/<your-feature>
```

Implement and test the work locally:

```bash
git add .
git commit -m "Implement <feature>"
git push -u origin feature/<your-feature>
```

Then create a Pull Request into `main`.

### Shared Areas

The following areas should not be modified casually by individual pairs:

```text
shared/
data/
evaluation/
app/
docs/architecture.md
```

Changes to shared contracts should be coordinated with the project lead.

---

# ▶️ Setup

Clone the repository:

```bash
git clone <repository-url>
cd rag-knowledge-representation-playground
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify the shared components:

```bash
python -c "from shared import Evidence, Retriever, KnowledgeRepresentation; print('Shared foundation OK')"
```

Run tests:

```bash
python -m pytest
```

---

# 📌 Project Principles

### 1. Same Knowledge

Every approach works from the same NovaMart source knowledge.

### 2. Same Benchmark

Every approach is evaluated against the same 40 questions and ground truth.

### 3. Representation ≠ Retrieval

Changing how knowledge is represented is different from changing how it is retrieved.

### 4. Evidence Before Answers

The project evaluates retrieved evidence before attributing improvements or failures to the LLM.

### 5. No Hardcoded Answers

Implementations must retrieve evidence from the representation rather than hardcoding benchmark answers.

### 6. Compare, Don't Assume

The objective is not to prove that one technique is universally better.

The objective is to understand:

> **Which representation and retrieval approach works well for which type of question, and where does it fail?**

---

# 🚀 Final Demonstration

The final application will allow users to:

1. Enter a question.
2. Select or compare knowledge representations.
3. Select retrieval strategies.
4. Inspect retrieved evidence.
5. Compare retrieval results.
6. Generate an answer using the retrieved evidence.
7. View evaluation results and failure cases.

The final demo will make the relationship between:

```text
Representation
      ↓
Retrieval
      ↓
Evidence
      ↓
Answer
```

visible and measurable.

---

## 📖 Documentation

Additional project documentation:

* `docs/architecture.md` — System architecture
* `docs/contribution-guide.md` — Team contribution workflow
* `docs/team-assignments.md` — Pair responsibilities
* `evaluation/README.md` — Evaluation methodology

---

## 🎯 Expected Outcome

By the end of the project, the team should be able to demonstrate:

* How different knowledge representations affect retrieval
* How different retrieval strategies behave on the same knowledge
* Why semantic similarity alone can be insufficient
* How structured relationships help certain questions
* How metadata can constrain retrieval
* How graphs can support multi-hop reasoning
* How retrieval failures affect downstream answers
* Why **retrieval quality and evidence quality are critical components of RAG systems**

---

**Core idea:**

> **A better RAG system does not start with “Which LLM should we use?” It starts with “Did we retrieve the right evidence?”**
