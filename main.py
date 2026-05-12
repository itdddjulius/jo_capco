from rag import RAGBot

if __name__ == "__main__":
    print("Initialising RAGBot...\n")
    rag = RAGBot()
    print("Reading and embedding data...\n")
    rag.read_and_embed_data(folder_path="data/")

    print(
        "Hi, I'm your RAGBot. Ask me anything about Jupiter, Ada Lovelace, or CRISPR\n"
    )

    while True:
        question = input("Me:")
        response = rag.ask(question=question)
        print(f"RAGBot: {response}\n")
