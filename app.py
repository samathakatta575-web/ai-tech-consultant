from fastapi import FastAPI
import json

app = FastAPI(title="Knowledge Brain API")

# Load docs
DOCS = []
try:
    with open("task1/anthropic_docs.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            DOCS.append(json.loads(line))
    print(f"Loaded {len(DOCS)} docs")
except:
    print("No docs file yet")

@app.get("/")
def home():
    return {"status": "Knowledge Brain running", "docs": len(DOCS)}

@app.get("/search")
def search(q: str, limit: int = 3):
    q = q.lower()
    results = []
    for doc in DOCS:
        if q in doc['text'].lower() or q in doc['url'].lower():
            results.append(doc)
            if len(results) >= limit:
                break
    return {"query": q, "results": results}

@app.get("/chat")
def chat(question: str):
    # Simple RAG: search + return context
    q = question.lower()
    hits = [d for d in DOCS if any(w in d['text'].lower() for w in q.split()[:4])][:2]
    if not hits:
        return {"answer": "I don't know based on current knowledge.", "sources": []}
    
    context = "\n".join([h['text'][:1000] for h in hits])
    answer = f"Based on docs: {context[:500]}... (Full answer needs Claude API)"
    return {
        "question": question,
        "answer": answer,
        "sources": [h['url'] for h in hits]
    }