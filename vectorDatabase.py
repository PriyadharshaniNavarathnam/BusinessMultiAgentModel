from dotenv import load_dotenv
import os
import pandas as pd
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# --- Load API Key ---
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# --- Initialize Pinecone Client ---
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "llm-agent-index"

# --- Create index if not exists ---
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,   # MiniLM embeddings = 384
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",      # or "gcp"
            region="us-east-1"
        )
    )

# --- Connect to Index ---
index = pc.Index(index_name)

# --- Embedding Model ---
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --- Load & Prepare Data ---
docs = []

# Products
products = pd.read_csv("data/products/products_clean.csv")
for _, row in products.iterrows():
    docs.append({
        "id": f"product-{row.name}",
        "text": str(row.to_dict()),
        "source": "products"
    })

# Customer Support
support = pd.read_csv("data/customer_support/support_clean.csv")
for _, row in support.iterrows():
    docs.append({
        "id": f"support-{row.name}",
        "text": str(row.to_dict()),
        "source": "support"
    })

# FAQ
faq = pd.read_csv("data/faq/faq_clean.csv")
for _, row in faq.iterrows():
    docs.append({
        "id": f"faq-{row.name}",
        "text": row["question"] + " " + row["answer"],
        "source": "faq"
    })

print("📊 Total documents to index:", len(docs))

# --- Generate & Upload in Batches ---
batch_size = 100
for i in tqdm(range(0, len(docs), batch_size)):
    batch = docs[i:i+batch_size]
    embeddings = embedder.encode([d["text"] for d in batch]).tolist()
    vectors = [
        (batch[j]["id"], embeddings[j], {"source": batch[j]["source"], "text": batch[j]["text"]})
        for j in range(len(batch))
    ]
    index.upsert(vectors)

print("✅ Data uploaded to Pinecone")

# --- Verify ---
stats = index.describe_index_stats()
print("📦 Index Stats:", stats)
