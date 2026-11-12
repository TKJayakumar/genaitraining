from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma


class StoreManager:

    def __init__(self, config: dict):

        self.config = config

        self.embedding_model = config["embedding"]["model_name"]

        self.persist_dir = config["storage"]["persist_dir"]

        self.collection_name = config["storage"]["collection_name"]

        self.reset_collection = config["storage"]["reset_collection"]


    def embed_and_store(
        self,
        chunks: list[str],
        source: str = "binance_hack.md"
    ):

        documents = []

        for i, chunk in enumerate(chunks):

            heading_lines = [
                line.strip()
                for line in chunk.splitlines()
                if line.strip().startswith("#")
            ]

            title = heading_lines[0] if heading_lines else "Untitled"

            metadata = {
                "source": source,
                "title": title,
                "chunk_index": str(i),
                "chunk_length": str(len(chunk))
            }

            documents.append(
                Document(
                    page_content=chunk,
                    metadata=metadata
                )
            )


        # Load embedding model from config.yaml
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )


        # Create Chroma vector store
        vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=embeddings,
            persist_directory=self.persist_dir
        )


        # Reset collection based on config
        if self.reset_collection:

            vector_store.reset_collection()


        # Store documents
        if documents:

            vector_store.add_documents(
                documents=documents,
                ids=[f"chunk_{i}" for i in range(len(documents))]
            )


        return documents, vector_store