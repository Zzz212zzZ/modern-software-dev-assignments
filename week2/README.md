# Week 2 – Action Item Extractor

A FastAPI + SQLite application that converts free-form notes into enumerated action items using both heuristic-based and LLM-powered extraction.

## Setup

### Prerequisites

- Python 3.10+
- Conda (with the `cs146s` environment)
- [Ollama](https://ollama.com/) installed and running (`ollama serve`)

### Install Dependencies

```bash
conda activate cs146s
poetry install
```

### Pull an Ollama Model

```bash
ollama pull llama3.1:8b
```

You can override the model by setting the `OLLAMA_MODEL` environment variable.

## Running the Server

```bash
conda activate cs146s
uvicorn week2.app.main:app --reload
```

Open http://127.0.0.1:8000/ in your browser.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the frontend HTML |
| `POST` | `/notes` | Create a new note |
| `GET` | `/notes` | List all saved notes |
| `GET` | `/notes/{note_id}` | Retrieve a single note |
| `POST` | `/action-items/extract` | Extract action items using heuristic rules |
| `POST` | `/action-items/extract-llm` | Extract action items using an LLM (Ollama) |
| `GET` | `/action-items` | List all action items (optionally filter by `?note_id=`) |
| `POST` | `/action-items/{id}/done` | Mark an action item as done/undone |

### Example Requests

**Extract (heuristic):**
```bash
curl -X POST http://127.0.0.1:8000/action-items/extract \
  -H 'Content-Type: application/json' \
  -d '{"text": "- Set up database\n- Write tests", "save_note": true}'
```

**Extract (LLM):**
```bash
curl -X POST http://127.0.0.1:8000/action-items/extract-llm \
  -H 'Content-Type: application/json' \
  -d '{"text": "Buy groceries. Fix the login bug.", "save_note": false}'
```

**List notes:**
```bash
curl http://127.0.0.1:8000/notes
```

## Running Tests

```bash
conda activate cs146s
python -m pytest week2/tests/test_extract.py -v
```

## Project Structure

```
week2/
├── app/
│   ├── main.py              # FastAPI app entry point with lifespan
│   ├── db.py                # SQLite database layer
│   ├── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── notes.py         # Notes CRUD endpoints
│   │   └── action_items.py  # Action item extraction & management
│   └── services/
│       └── extract.py       # Heuristic + LLM extraction logic
├── frontend/
│   └── index.html           # Single-page HTML/JS frontend
├── tests/
│   └── test_extract.py      # Unit tests for extraction functions
└── data/
    └── app.db               # SQLite database (auto-created)
```
