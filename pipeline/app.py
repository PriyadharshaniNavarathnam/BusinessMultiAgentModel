from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from agents.intent_agent import IntentAgent
from agents.retriever_agent import RetrieverAgent
from agents.responder_agent import ResponderAgent

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "llm-agent-index")

pc = Pinecone(api_key=PINECONE_API_KEY)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

intent_agent = IntentAgent()
retriever_agent = RetrieverAgent(pc, INDEX_NAME, embedder)
responder_agent = ResponderAgent(GROQ_API_KEY)

app = FastAPI(title="LLM Agents: Decide → Retrieve → Respond")

class AskBody(BaseModel):
    question: str
    top_k: int = 5

@app.post("/ask")
def ask(body: AskBody):
    trace = []

    # Decide
    decision = intent_agent.decide(body.question)
    #trace.append({"step": "decide", **decision})

    # Retrieve
    retrieved = retriever_agent.retrieve(body.question, decision["intent"], top_k=body.top_k)
    #trace.append({"step": "retrieve", **retrieved})

    # Respond
    answer = responder_agent.respond(decision["intent"], body.question, retrieved["matches"])
    #trace.append({"step": "respond", "final_answer": answer})

    return {"intent": decision["intent"], "answer": answer}

@app.get("/demo")
def demo():
    samples = [
        "How can I track my order?",
        "Recommend a budget smartphone with good battery.",
        "What is your refund and return policy?"
    ]
    out = []
    for q in samples:
        decision = intent_agent.decide(q)
        retrieved = retriever_agent.retrieve(q, decision["intent"], top_k=5)
        answer = responder_agent.respond(decision["intent"], q, retrieved["matches"])
        out.append({"question": q, "intent": decision["intent"], "answer": answer})
    return {"runs": out}
