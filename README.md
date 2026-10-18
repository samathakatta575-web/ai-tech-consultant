# AI Tech Consultant - Full Stack Assignment

## Tasks Completed

### Task 1: Knowledge Brain (RAG) - Port 8005
- URL: http://127.0.0.1:8005/docs
- Features: /search (TF-IDF), /chat (RAG), scraper
- Docs loaded: 564 docs from anthropic_docs.jsonl

### Task 2: Inbox Agent - Port 8006
- URL: http://127.0.0.1:8006/docs
- Features: /draft (AI reply), /emails (list)

## How to Run

pip install -r requirements.txt

Terminal 1: python -m uvicorn task1.app:app --port 8005 --reload
Terminal 2: python -m uvicorn task2.main:app --port 8006 --reload

## Architecture
Swagger UI -> FastAPI -> TF-IDF + RAG -> JSONL Docs / Mock Emails

## Proof
Both APIs running successfully on 8005 and 8006.
