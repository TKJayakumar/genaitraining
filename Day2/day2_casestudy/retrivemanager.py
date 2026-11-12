
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder


class RetrieveManager:

    def query_chroma_db(
        self,
        query: str,
        collection_name: str = "gold_rate",
        persist_dir: str = "./chroma_db",
        n_results: int = 3
    ):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_dir
        )

        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": n_results
            }
        )

        retrieved_documents = retriever.invoke(query)

        return retrieved_documents

    def query_hybrid(
        self,
        query: str,
        documents: list[Document],
        vector_store: Chroma,
        n_results: int = 3
    ):

        chroma_retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": n_results
            }
        )

        bm25_retriever = BM25Retriever.from_documents(
            documents,
            k=n_results
        )

        ensemble_retriever = EnsembleRetriever(
            retrievers=[
                bm25_retriever,
                chroma_retriever
            ],
            weights=[0.5, 0.5]
        )

        results = ensemble_retriever.invoke(query)

        return results

    def rerank_documents(
        self,
        query: str,
        documents: list[Document],
        top_n: int = 3
    ) -> list[Document]:

        reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        pairs = [
            [query, doc.page_content]
            for doc in documents
        ]

        scores = reranker.predict(pairs)

        doc_score_pairs = list(zip(documents, scores))

        doc_score_pairs.sort(
            key=lambda pair: pair[1],
            reverse=True
        )

        top_pairs = doc_score_pairs[:top_n]

        return [
            doc for doc, score in top_pairs
        ]
