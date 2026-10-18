from fastapi import FastAPI
import requests

app = FastAPI(title="Inbox Agent")

# Task 1 API ni pilustundi
KB_API = "http://127.0.0.1:8000"

# 50 emails ki sample - 5 sample isthunna, nuvvu 50 varaku penchukovachu
SAMPLE_EMAILS = [
    "How to configure refunds in my site?",
    "I want a quote for building a website",
    "My search is not working, make it better",
    "Need help with payment settings",
    "Please cancel my subscription and refund"
]

def get_knowledge(query: str):
    try:
        r = requests.get(f"{KB_API}/search", params={"q": query}, timeout=5)
        return r.json()
    except:
        # KB off unte local search
        return {"results": [{"text": "Knowledge Brain is offline, but I can help based on general knowledge"}]}

@app.get("/")
def home():
    return {"status": "Inbox Agent running", "sample_emails": len(SAMPLE_EMAILS)}

@app.post("/draft")
def draft_reply(email: str):
    # Step 1: Understand email intent
    # Step 2: Call Knowledge Brain
    kb = get_knowledge(email)
    sources = [x.get('url','') for x in kb.get('results',[])][:2]
    
    # Step 3: Draft (Simple template - Task 2 lo Claude tho replace cheyavachu)
    draft = f"""Hi,

Thanks for reaching out about: "{email}"

Based on our knowledge base, here's help:
{kb.get('results',[{}])[0].get('text','')[:400] if kb.get('results') else 'We will check and get back.'}

Let me know if you need more help.

Best,
Support Team
Sources: {', '.join(sources)}
"""
    return {
        "original_email": email,
        "draft": draft,
        "sources": sources,
        "needs_human_approval": True,
        "email_type": "support" if "how to" in email.lower() else "sales"
    }

@app.get("/emails")
def list_emails():
    return SAMPLE_EMAILS