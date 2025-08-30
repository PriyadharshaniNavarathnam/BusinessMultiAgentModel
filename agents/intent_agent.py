# Simple keyword-based intent detection
class IntentAgent:
    KEYWORDS = {
        "support": ["refund", "return", "help", "issue", "complaint"],
        "product": ["recommend", "buy", "best", "compare", "price"],
        "faq": ["how", "what", "when", "where", "faq"]
    }

    def decide(self, question: str):
        votes = {k: 0 for k in self.KEYWORDS}
        q_lower = question.lower()
        for intent, keywords in self.KEYWORDS.items():
            for kw in keywords:
                if kw in q_lower:
                    votes[intent] += 1
        chosen_intent = max(votes, key=votes.get)
        return {"intent": chosen_intent, "rationale": f"Keyword votes → {votes}. Chosen intent: '{chosen_intent}'."}
