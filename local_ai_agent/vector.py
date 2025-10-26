# This is like a local database - chroma db is used to store embeddings and other vector data for efficient retrieval and similarity searches.

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd
import os

df = pd.read_csv("dummy.csv")  # Assume a CSV file with a 'text' column

embeddings = OllamaEmbeddings(model="llama3:latest")

db_location = "./chroma_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=row["title"],
            metadata={"rating": row.get("rating", "N/A")},
        )
        ids.append(str(i))
        documents.append(document)

vector_store = Chroma(
    collection_name="dummy_collection",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)