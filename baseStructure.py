import os

base_path = r"C:\Users\CCS\Desktop\LLM_Agent_Project"

folders = [
    "data/products",
    "data/customer_support",
    "data/faq",
    "notebooks",
    "agents",
    "pipeline",
    "tests"
]

for f in folders:
    os.makedirs(os.path.join(base_path, f), exist_ok=True)

print(" Project folder structure created at:", base_path)
