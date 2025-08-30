from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

class RetrieverAgent:
    def __init__(self, pc: Pinecone, index_name: str, embedder: SentenceTransformer):
        self.index = pc.Index(index_name)
        self.embedder = embedder

    def retrieve(self, query: str, intent: str, top_k: int = 5):
        embedding = self.embedder.encode(query).tolist()
        result = self.index.query(vector=embedding, top_k=top_k, include_metadata=True)
        matches = [{"id": m["id"], "text": m["metadata"]["text"], "source": m["metadata"]["source"]} for m in result["matches"]]
        return {"source": intent, "top_k": top_k, "matches": matches}
