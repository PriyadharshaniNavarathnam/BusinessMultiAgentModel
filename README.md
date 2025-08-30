# BusinessMultiAgentModel
# 💼 Business Multi-Agent Model

## Overview
This project implements a **Business Multi-Agent system** using **FastAPI** and **Streamlit**. It leverages multiple agents to understand user queries, retrieve relevant information from a vector database, and generate intelligent responses.  

### Agents
- **IntentAgent**: Determines the intent of a user query.  
- **RetrieverAgent**: Searches relevant documents from Pinecone vector database.  
- **ResponderAgent**: Generates responses using Groq LLM API.  

The system is designed to run on **AWS EC2** but can also be run locally. Streamlit provides an interactive interface for querying the model.

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

