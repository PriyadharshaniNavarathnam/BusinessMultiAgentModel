import kagglehub
import os
import shutil

# Base project path
base_path = r"C:\Users\CCS\Desktop\LLM_Agent_Project\data"

# Dataset → target folder mapping
datasets = {
    "PromptCloudHQ/flipkart-products": "products",          # Product catalog
    "thoughtvector/customer-support-on-twitter": "customer_support", 
    "scodepy/customer-support-intent-dataset": "customer_support",
    "divyanshu2000/customer-support-training-dataset-27k": "customer_support",
    "steve1215rogg/tech-support-conversations-dataset": "customer_support",
    "saadmakhdoom/ecommerce-faq-chatbot-dataset": "faq"
}

for dataset, folder in datasets.items():
    print(f"🔽 Downloading: {dataset}")
    path = kagglehub.dataset_download(dataset)

    target_folder = os.path.join(base_path, folder)
    os.makedirs(target_folder, exist_ok=True)

    # Copy downloaded files into the right folder
    for file in os.listdir(path):
        src = os.path.join(path, file)
        dst = os.path.join(target_folder, file)
        if os.path.isfile(src):
            shutil.copy(src, dst)

    print(f"✅ {dataset} stored in {target_folder}\n")

print("🎉 All datasets downloaded and organized!")
