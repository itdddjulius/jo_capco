import os
from pathlib import Path
from typing import Any, Dict, List

import httpx
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI
from sentence_transformers import SentenceTransformer

load_dotenv()


class RAGBot:
    def __init__(self):
        """
        JO - Instantiates Azure OpenAI client and local SentenceTransformer model.
        """
        self.openai_client = AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("OPENAI_API_VERSION"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            http_client=httpx.Client(verify=False),
        )
        self.sentence_transformer = SentenceTransformer("models/all-MiniLM-L6-v2")
        self.model_name = os.environ.get("MODEL_NAME")

        # In-memory vector store for this prototype.
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray | None = None

    def _chunk_text(self, text: str, chunk_size: int = 700, overlap: int = 120) -> List[str]:
        """
        JO - Simple overlapping character chunking.
        JO - This is pragmatic for a small 45-minute RAG prototype.
        """
        cleaned_text = " ".join(text.split())

        if not cleaned_text:
            return []

        chunks = []
        start = 0
        step = chunk_size - overlap

        while start < len(cleaned_text):
            end = start + chunk_size
            chunk = cleaned_text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += step

        return chunks

    def read_and_embed_data(self, folder_path):
        """
        JO - Loads all .txt files from the given folder path,
        JO - chunks the documents, generates embeddings,
        JO - and stores them in memory for retrieval.
        """
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Data folder not found: {folder_path}")

        documents = sorted(folder.glob("*.txt"))

        if not documents:
            raise FileNotFoundError(f"No .txt files found in: {folder_path}")

        self.chunks = []

        for document_path in documents:
            text = document_path.read_text(encoding="utf-8")
            document_chunks = self._chunk_text(text)

            for index, chunk_text in enumerate(document_chunks):
                self.chunks.append(
                    {
                        "source": document_path.name,
                        "chunk_id": index,
                        "text": chunk_text,
                    }
                )

        chunk_texts = [chunk["text"] for chunk in self.chunks]

        self.embeddings = self.sentence_transformer.encode(
            chunk_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        print(f"Embedded {len(self.chunks)} chunks from {len(documents)} documents.")

    def _retrieve(self, question: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        JO - Embeds the user question and returns the top-k most relevant chunks.
        JO - Because embeddings are normalized, dot product equals cosine similarity.
        """
        if self.embeddings is None or not self.chunks:
            raise RuntimeError("No embeddings found. Call read_and_embed_data() first.")

        question_embedding = self.sentence_transformer.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        scores = np.dot(self.embeddings, question_embedding)
        top_indices = np.argsort(scores)[-k:][::-1]

        results = []
        for index in top_indices:
            chunk = dict(self.chunks[index])
            chunk["score"] = float(scores[index])
            results.append(chunk)

        return results

    def ask(self, question, k=3):
        """
        JO - Accepts a user query, retrieves the top-k most relevant
        JO - document chunks based on similarity, and returns a context-aware
        JO - answer from Azure OpenAI.
        """
        relevant_chunks = self._retrieve(question=question, k=k)

        context = "\n\n".join(
            f"Source: {chunk['source']} | Chunk: {chunk['chunk_id']} | Score: {chunk['score']:.3f}\n{chunk['text']}"
            for chunk in relevant_chunks
        )

        user_prompt = f"""
Use the context below to answer the question.

Rules:
- Answer only using the provided context.
- If the answer is not in the context, say: "I don't know based on the provided documents."
- Keep the answer concise and clear.
- Mention the source document name when useful.

Context:
{context}

Question:
{question}

Answer:
""".strip()

        response = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful retrieval-augmented assistant.",
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content
