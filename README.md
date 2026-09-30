# 🏛️ CivicFlow

### AI-Powered Civic & Government Procedure Assistant

CivicFlow is an **AI-powered multi-agent platform** that helps users understand and complete real-world civic and government-related tasks.

Instead of simply generating an answer, CivicFlow analyzes a user's goal, identifies the relevant eligibility requirements, documents, rules, and procedures, retrieves supporting information from trusted sources, and produces an **evidence-backed step-by-step procedure**.

---

## Problem

Government and civic procedures are often difficult to navigate because information is:

* Scattered across multiple government documents and websites
* Written in complex administrative language
* Difficult to search and understand
* Different depending on eligibility, location, or type of service
* Often missing a clear step-by-step explanation

Users may have to search through multiple PDFs, websites, rules, and application instructions before understanding what they actually need to do.

###  Solution

CivicFlow acts as an **AI civic assistant** that converts a real-world civic goal into a structured procedure.

For example:

> **User:** "I want to apply for a government housing scheme. Am I eligible and what documents do I need?"

CivicFlow can analyze the request and provide:

1. Eligibility requirements
2. Required documents
3. Applicable rules/regulations
4. Application procedure
5. Relevant government sources
6. Evidence supporting the generated answer

---

#  Key Features

###  Multi-Agent Architecture

CivicFlow uses specialized AI agents for different tasks rather than relying on a single LLM response.

The workflow can include agents for:

* **Eligibility Analysis**
* **Document Identification**
* **Regulation/Rule Analysis**
* **Procedure Generation**
* **Evidence Verification**

The outputs from these agents are combined into a final structured response.

---

###  Document-Based Retrieval

CivicFlow first searches its collection of stored government documents.

Documents are:

1. Loaded
2. Split into meaningful chunks
3. Converted into embeddings
4. Stored in **Qdrant**
5. Retrieved based on semantic similarity to the user's query

This allows the system to use relevant portions of large government documents instead of passing entire documents to the LLM.

---

### Semantic Retrieval

CivicFlow uses embeddings to represent both:

* User queries
* Document chunks

The system compares their vector representations to identify relevant information.

Conceptually:

```text
User Query
     ↓
Embedding Model
     ↓
Query Vector
     ↓
Qdrant Vector Search
     ↓
Relevant Document Chunks
```

This enables retrieval even when the user's wording differs from the wording used in the original government document.

---

###  Web Search Fallback

If sufficient information cannot be found in the stored document collection, CivicFlow can use web search to obtain additional information.

The overall retrieval strategy is:

```text
User Query
    ↓
Search Stored Documents
    ↓
Relevant Evidence Found?
   / \
 Yes  No
 ↓     ↓
Use   Web Search
Docs      ↓
   \     /
    ↓   ↓
 Evidence
    ↓
 AI Agents
    ↓
Verification
    ↓
Final Procedure
```

This helps combine a controlled document knowledge base with additional online information when necessary.

---

###  LangGraph Workflow

CivicFlow uses **LangGraph** to coordinate the multi-agent workflow.

Instead of a simple linear chain, the system can make decisions about which agents should execute and how their results should be combined.

Example:

```text
                 User Goal
                    │
                    ▼
             Query Understanding
                    │
                    ▼
             Document Retrieval
                    │
             ┌──────┴──────┐
             │             │
        Documents       Web Search
             │             │
             └──────┬──────┘
                    ▼
          ┌─────────────────────┐
          │     AI Agents       │
          ├─────────────────────┤
          │ Eligibility Agent   │
          │ Document Agent      │
          │ Regulation Agent    │
          │ Procedure Agent     │
          └──────────┬──────────┘
                     ▼
              Result Aggregation
                     │
                     ▼
             Evidence Verification
                     │
                     ▼
               Final Response
```

---

#  System Architecture

```text
                         ┌─────────────────┐
                         │      User       │
                         └────────┬────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │   Query Analysis   │
                       └─────────┬──────────┘
                                 │
                                 ▼
                       ┌────────────────────┐
                       │ Retrieval Layer    │
                       └─────────┬──────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
             ┌─────────────┐           ┌─────────────┐
             │  Qdrant     │           │ Web Search  │
             │ Vector DB   │           │   Fallback  │
             └──────┬──────┘           └──────┬──────┘
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                       ┌────────────────────┐
                       │   LangGraph        │
                       │ Multi-Agent Layer  │
                       └─────────┬──────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             ▼                   ▼                   ▼
      ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
      │ Eligibility │     │  Document   │     │ Regulation  │
      │    Agent    │     │    Agent    │     │    Agent    │
      └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 ▼
                       ┌────────────────────┐
                       │ Procedure Agent    │
                       └─────────┬──────────┘
                                 ▼
                       ┌────────────────────┐
                       │ Evidence Checker   │
                       └─────────┬──────────┘
                                 ▼
                       ┌────────────────────┐
                       │ Structured Answer  │
                       └────────────────────┘
```

---

#  Technology Stack

| Component           | Technology                    |
| ------------------- | ----------------------------- |
| Frontend            | React                         |
| Backend             | Python                        |
| API                 | FastAPI                       |
| AI/LLM              | LLM-based reasoning           |
| Agent Orchestration | LangGraph                     |
| Validation          | Pydantic                      |
| Embeddings          | Embedding Model               |
| Vector Database     | Qdrant                        |
| Retrieval           | Vector/Semantic Retrieval     |
| Document Processing | Python                        |
| Web Retrieval       | Web Search                    |
| Data Storage        | Qdrant / Application Database |
| Environment         | Python Virtual Environment    |

---

#  RAG Pipeline

CivicFlow follows a Retrieval-Augmented Generation architecture.

### 1. Document Ingestion

Government documents are collected and processed.

```text
Documents
    ↓
Text Extraction
    ↓
Cleaning
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Qdrant
```

### 2. Query Processing

When a user asks a question:

```text
Question
   ↓
Query Embedding
   ↓
Vector Search
   ↓
Relevant Chunks
   ↓
Context
   ↓
LLM
```

### 3. Answer Generation

The retrieved evidence is provided to the relevant agents.

The final response is generated from the retrieved information rather than relying solely on the model's internal knowledge.

---

#  Chunking

Large government documents are divided into smaller pieces called **chunks**.

For example:

```text
Government Document
        ↓
 ┌───────────────┐
 │ Chunk 1       │
 ├───────────────┤
 │ Chunk 2       │
 ├───────────────┤
 │ Chunk 3       │
 ├───────────────┤
 │ Chunk 4       │
 └───────────────┘
```

Each chunk is converted into an embedding and stored in Qdrant.

This makes it possible to retrieve only the portions relevant to a particular question.

---

#  Embeddings

An embedding converts text into a numerical vector representation.

For example:

```text
"Documents required for housing application"
                    ↓
              Embedding Model
                    ↓
       [0.21, -0.13, 0.72, ...]
```

The same process is applied to document chunks.

The query vector is then compared with stored vectors to find semantically related information.

---

#  Qdrant

Qdrant is used as the project's **vector database**.

It stores:

* Document embeddings
* Text chunks
* Metadata
* Source information

Example metadata:

```json
{
  "source": "government_document.pdf",
  "page": 12,
  "section": "Eligibility",
  "document_type": "scheme_guidelines"
}
```

Metadata helps the system identify where retrieved information originated and supports evidence tracking.

> `qdrant_data/` contains local Qdrant database files and should not be committed to Git.

---

#  Why Multi-Agent AI?

A single LLM response may not be sufficient for complex civic procedures.

CivicFlow separates the problem into specialized tasks.

For example:

```text
User Goal
   │
   ├──► Eligibility Agent
   │
   ├──► Document Agent
   │
   ├──► Regulation Agent
   │
   └──► Procedure Agent
              │
              ▼
        Result Aggregator
              │
              ▼
       Evidence Checker
              │
              ▼
        Final Procedure
```

Each agent focuses on a specific aspect of the user's goal.

---

#  Evidence Verification

One of CivicFlow's important goals is to reduce unsupported AI-generated information.

The verification stage checks whether the final response is supported by retrieved evidence.

Conceptually:

```text
Generated Claim
      ↓
Find Supporting Evidence
      ↓
Evidence Available?
   /          \
 Yes           No
 ↓              ↓
Supported    Flag/Remove
```

This helps reduce hallucinations and improves the reliability of the generated procedure.

---

#  Example

### User Input

```text
I want to apply for a government housing scheme.
What are the eligibility requirements and documents?
```

### CivicFlow Processing

```text
User Goal
   ↓
Query Analysis
   ↓
Retrieve Government Documents
   ↓
Eligibility Agent
   ↓
Document Agent
   ↓
Regulation Agent
   ↓
Procedure Agent
   ↓
Evidence Verification
```

### Example Output Structure

```text
Eligibility
├── Requirement 1
├── Requirement 2
└── Requirement 3

Required Documents
├── Document 1
├── Document 2
└── Document 3

Procedure
1. Complete application
2. Submit required documents
3. Verification
4. Application processing

Sources
├── Government Document
└── Official Website
```

---

#  Project Structure

```text
CivicFlow/
│
├── backend/
│   ├── agents/
│   │   ├── eligibility_agent.py
│   │   ├── document_agent.py
│   │   ├── regulation_agent.py
│   │   └── procedure_agent.py
│   │
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── qdrant.py
│   │
│   ├── ingestion/
│   │   ├── loader.
```
