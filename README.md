# Capco – AI Engineer Coding Task Brief

As part of the technical interview process for the **AI Engineer** role, you'll 
complete a short coding task designed to simulate a realistic problem in building retrieval-augmented generation (RAG) systems with LLMs.

This task will be completed during a **live interview, from scratch**, but you 
are receiving this starter code ahead of time to get familiar with the structure and prepare your approach.

**You'll have 45 minutes to complete the task.** You may use any online resources for reference during the task, but you must write the code live.

---

## Objective

Your goal is to build a simple RAGBot that:

1. Reads a set of `.txt` documents.
2. Chunks and embeds them using an embedding model.
3. Retrieves the most relevant chunks in response to a user question.
4. Constructs a prompt using the retrieved context and sends it to an LLM (Azure OpenAI).
5. Returns a context-aware answer.

---

## Project Structure

You have been provided with a .zip file containing:

```
rag-mini/
├── data/                      # .txt files on Ada Lovelace, Jupiter, and CRISPR
│   ├── adalovelace.txt
│   ├── crispr.txt
│   └── jupiter.txt
│
├── models/
│   └── all-MiniLM-L6-v2/      # Preloaded local SentenceTransformer model
│
├── rag.py                     # Your main class to implement
├── main.py                    # Runs the bot
├── requirements.txt           # Dependencies for the task
└── env_example.txt            # example environment file for you to create your own .env file
```

---

## Setup Instructions

### 1. **Create a virtual environment** (recommended)

You may do this by whatever method you're most comfortable with. Below is an example. 
For consistency we recommend using Python version 3.11.10, though versions 3.9-3.10 should also work.
```bash
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
```

### 2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Get access to the LLM**
You’ll be provided with a temporary `.env` file during the interview that contains the environment variables below. During the interview you will get temporary access to, and be expected to call, a GPT-4o model on our Azure OpenAI resource, but feel free to substitute this for an LLM of your choice while you prepare.

```env
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
OPENAI_API_VERSION=...
MODEL_NAME=...  
TOKENIZERS_PARALLELISM = False # Required for SentenceTransformer
```

Make sure this file is saved as `.env` in the project root.

### 4. **Run the bot**
```bash
python main.py
```

You’ll see a CLI where you can ask questions about the provided documents once you have created RagBot.

---

## Your Task

You are expected to implement the following key methods in RagBot in the `rag.py` file:
* `read_and_embed_data()` – Load, chunk, and embed text files.
* `ask()` – Retrieve relevant context and send a prompt to the LLM.

Feel free to add any helper methods inside the `RAGBot` class as needed. You may also create any additional scripts or notebooks to help you develop and test your code.

Do not modify the `main.py` file.

---

## Notes

* Focus on correctness and clarity, not perfect architecture. Be pragmatic.
* Your implementation does not need to scale — treat this as a prototype.
* You will be asked questions about your design decisions during the interview.

---

We’re excited to see how you approach this. Good luck! 

--------------------------------------------------------
J.O. - THR-07-MAY-2026 - CAPCO Solution ----------------
--------------------------------------------------------
Key changes:

- Loads all .txt files from data/
- Chunks text with overlap
- Embeds chunks using local all-MiniLM-L6-v2
- Retrieves top-k chunks via cosine similarity
- Sends retrieved context to Azure OpenAI
- Returns a grounded RAG answer

To Execute:

cd SOLUTION
cd ai-engineer-coding-task-uk

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cp env_example.txt .env

python main.py

--------------------------------------------------------

