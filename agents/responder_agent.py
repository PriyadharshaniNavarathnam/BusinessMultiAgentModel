# agents/responder_agent.py
from typing import Dict, Any, List
import time
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_STYLE = {
    "support": "You are a professional customer-support agent. Be concise, empathetic and action-oriented.",
    "faq":     "You are a helpful FAQ assistant. Answer strictly from provided context. If unknown, say so.",
    "product": "You are a product advisor. Give clear, neutral, comparable recommendations from context."
}

class ResponderAgent:
    """
    Calls an LLM (Groq) to craft a final answer using retrieved context.
    Returns only the answer text.
    Retries automatically on rate-limit errors (429).
    """
    def __init__(self, groq_api_key: str, model: str = "llama3-8b-8192", temperature: float = 0.3):
        self.groq_api_key = groq_api_key
        self.model = model
        self.temperature = temperature

    def _build_messages(self, intent: str, user_query: str, context_chunks: List[str]) -> List[Dict[str, str]]:
        system_msg = SYSTEM_STYLE.get(intent, SYSTEM_STYLE["faq"])
        context = "\n\n---\n\n".join(context_chunks) if context_chunks else "NO CONTEXT FOUND"
        user_block = f"""Use ONLY this context to answer. If it doesn't contain the answer, say you don't know.

Context:
{context}

User question: {user_query}
"""
        return [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_block}
        ]

    def _call_groq_api(self, payload: Dict[str, Any], headers: Dict[str, str], max_retries: int = 3) -> Dict[str, Any]:
        """
        Helper to call Groq API with retry on 429 errors.
        """
        for attempt in range(max_retries):
            try:
                resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.HTTPError as e:
                if resp.status_code == 429:  # Rate limit
                    wait = 2 ** attempt  # exponential backoff
                    print(f"Rate limit hit. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
        raise Exception("Max retries exceeded for Groq API")

    def respond(self, intent: str, user_query: str, matches: List[Dict[str, Any]]) -> str:
        """
        Returns only the final answer string.
        """
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }

        context_chunks = [m.get("text", "") for m in matches]
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": self._build_messages(intent, user_query, context_chunks)
        }

        data = self._call_groq_api(payload, headers)
        answer = data["choices"][0]["message"]["content"]

        return answer
