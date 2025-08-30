# 💼 Business Multi-Agent Model

## Overview
This project implements a **Business Multi-Agent system** using **FastAPI** and **Streamlit**.  
It leverages multiple agents to understand user queries, retrieve relevant information from a vector database, and generate intelligent responses.  

### Agents
- **IntentAgent**: Determines the intent of a user query.  
- **RetrieverAgent**: Searches relevant documents from Pinecone vector database.  
- **ResponderAgent**: Generates responses using Groq LLM API.  

The system is designed to run on **AWS EC2** but can also be run locally.  
Streamlit provides an interactive interface for querying the model.

---

## Features
- FastAPI backend with `/ask` and `/demo` endpoints.  
- Streamlit frontend for a simple user interface.  
- Continuous running with `nohup` on AWS EC2.  
- Vector search using Pinecone.  
- LLM-based response generation.  

---

## Prerequisites
- Python 3.12+  
- AWS EC2 instance (Ubuntu 22.04/24.04 recommended)  
- Pinecone account & API key  
- Groq API key  

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/PriyadharshaniNavarathnam/BusinessMultiAgentModel.git
cd BusinessMultiAgentModel
```

---

## Configuration
Create a `.env` file in the root directory:

```ini
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=llm-agent-index
GROQ_API_KEY=your_groq_api_key
```

---

## Usage

### Run FastAPI backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Run Streamlit frontend
```bash
streamlit run app.py
```

---

## Example Queries
- `"How can I track my order?"` → Order tracking intent  
- `"Recommend a budget smartphone with good battery."` → Product recommendation intent  
- `"What is your refund and return policy?"` → Policy retrieval intent  

---

## Deployment on AWS EC2

Run backend continuously with `nohup`:

```bash
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

Then access the API at:

```
http://<EC2-PUBLIC-IP>:8000
```

---

## Troubleshooting
- **401 Unauthorized** → Check your Pinecone or Groq API keys.  
- **No matches returned** → Ensure documents are indexed in Pinecone.  
- **Module not found** → Run inside virtual environment & reinstall dependencies.  

---

## Contributors
- [Priyadharshani Navarathnam](https://github.com/PriyadharshaniNavarathnam)  

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
