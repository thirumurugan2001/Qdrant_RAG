# Qdrant_RAG# HR Policy RAG Chatbot

An intelligent HR Policy assistant built with **FastAPI**, **Qdrant**, **Cohere embeddings**, and an **OpenAI-compatible LLM**. The chatbot answers employee questions strictly based on the content of an HR Policy PDF using Retrieval-Augmented Generation (RAG), with conversation memory for context-aware follow-ups.

## Features

- 📄 Ingests an HR Policy PDF, chunks it, and stores embeddings in a **Qdrant** vector database
- 🔍 Retrieves the most relevant policy sections for each employee question
- 🤖 Answers using an LLM constrained to the retrieved policy content only (no hallucination/outside knowledge)
- 🧠 Maintains conversation summary memory across turns via LangChain
- 🛡️ Includes a prompt-sanitization utility to help block prompt-injection style inputs
- ⚙️ Config-driven via `config.yaml` and `.env`

## Architecture

```
PDF (hr_policy_details.pdf)
   │
   ▼
fetch_data.py  (load_pdf)          → extract raw text
   │
   ▼
preprocessing.py (preprocess)      → clean/normalize text
   │
   ▼
chunking.py (chunk_text)           → split into overlapping chunks
   │
   ▼
embedding.py (get_embedding)       → Cohere embeddings
   │
   ▼
vectorstore.py (setup_collection,
                 ingest_chunks)     → store vectors in Qdrant

--- at query time ---

FastAPI endpoint (main.py)
   │
   ▼
ragController.py (rag)
   │
   ├── embedding.py        → embed the question
   ├── dbConnection.py     → connect to Qdrant
   ├── Qdrant query_points  → fetch top-matching chunks
   │
   ▼
ConnectChatBot.py           → build prompt with retrieved context
                              + conversation summary memory
                              → call LLM (OpenAI-compatible API)
   │
   ▼
Response returned to client
```

## Project Structure

```
├── main.py                    # FastAPI app & endpoint
├── Create_rag_pipeline.py     # One-time/offline script to build the RAG index
├── hr_policy_details.pdf      # Source HR policy document
├── requirements.txt
├── .env                       # API keys (not committed)
├── Config/
│   ├── config.yaml            # App configuration
│   └── loadConfig.py          # YAML config loader
├── rag_utils/
│   ├── fetch_data.py          # PDF text extraction
│   ├── preprocessing.py       # Text cleaning
│   ├── chunking.py            # Text splitting (LangChain)
│   ├── embedding.py           # Cohere embedding generation
│   ├── vectorstore.py         # Qdrant collection setup & ingestion
│   ├── dbConnection.py        # Qdrant client connection
│   ├── ConnectChatBot.py      # LLM call + conversation memory
│   ├── ragController.py       # RAG orchestration
│   ├── controller.py          # Request handling wrapper
│   ├── model.py                # Pydantic request schema
│   └── sanitize_prompt.py     # Prompt-injection guardrails
└── qdrant_storage/             # Local Qdrant persistent storage
```

## Prerequisites

- Python 3.9+
- A running [Qdrant](https://qdrant.tech/) instance (local or remote)
- An OpenAI-compatible LLM API key/endpoint
- A Cohere API key (for embeddings)

## Installation

```bash
git clone https://github.com/thirumurugan2001/Qdrant_RAG.git
cd Qdrant_RAG
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
OPEN_API_KEY=your_openai_compatible_api_key
COHERE_API_KEY=your_cohere_api_key
```

Update `Config/config.yaml` with your settings, e.g.:

```yaml
OPEN_AI:
  MODEL: "your-model-name"
  API_BASE_URL: "https://your-llm-endpoint/v1"

cohere:
  model: "embed-english-v3.0"
  input_type: "search_document"

qdrant:
  host: "localhost"
  port: 6333
  collection_name: "hr_policy_collection"
  vector_size: 1024

document:
  pdf_path: "hr_policy_details.pdf"
```

> Ensure `vector_size` matches the output dimension of the Cohere embedding model you configure.

## Usage

### 1. Build the RAG index (one-time, or whenever the policy PDF changes)

```bash
python Create_rag_pipeline.py
```

This loads the PDF, cleans and chunks the text, generates embeddings, and (re)creates the Qdrant collection with the ingested chunks.

### 2. Start the API server

```bash
uvicorn main:app --reload
```

The server runs at `http://127.0.0.1:8000` by default.

### 3. Query the chatbot

**Endpoint:** `POST /chatbot/about/`

**Request body:**
```json
{
  "Question": "Could you explain the company's remote work policy?"
}
```

**Response:**
```json
{
  "statusCode": 200,
  "status": true,
  "message": "Relevant information found.",
  "response": "### Remote Work Policy\n\n- ..."
}
```

## How It Works

1. The employee's question is embedded using Cohere and matched against the top 2 most relevant chunks stored in Qdrant.
2. The retrieved chunks are passed as context to the LLM along with a strict system prompt that:
   - Restricts answers to the HR policy content only
   - Declines to answer unrelated questions (weather, coding, sports, etc.)
   - Asks for clarification on ambiguous questions
   - Formats answers with headings/bullet points
3. A running conversation summary (via LangChain's `ConversationSummaryMemory`) is included so follow-up questions retain context.
4. The final answer is returned as JSON.

## Notes & Possible Improvements

- `sanitize_prompt.py` is implemented but not currently wired into the request flow in `main.py`/`ragController.py` — consider calling it on the incoming question before processing to actively block injection attempts.
- Conversation memory is currently in-process/global, so it is shared across all requests rather than scoped per user/session — consider keying memory by a session or user ID for multi-user deployments.
- No authentication is implemented on the FastAPI endpoint; add an auth layer before deploying publicly.
- Consider adding logging/monitoring and rate limiting for production use.

## License

See the [LICENSE](./LICENSE) file for details.
