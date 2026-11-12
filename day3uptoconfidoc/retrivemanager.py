from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder


class RetrieveManager:

    def __init__(self, config: dict):

        self.config = config

        self.embedding_model = config["embedding"]["model_name"]

        self.collection_name = config["storage"]["collection_name"]

        self.persist_dir = config["storage"]["persist_dir"]

        self.search_type = config["retrieval"]["search_type"]

        self.bm25_weight = config["retrieval"]["bm25_weight"]

        self.vector_weight = config["retrieval"]["vector_weight"]

        self.reranker_model = config["retrieval"]["reranker_model"]


    def query_chroma_db(
        self,
        query: str,
        collection_name: str = None,
        persist_dir: str = None,
        n_results: int = 3
    ):

        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )

        vector_store = Chroma(
            collection_name=collection_name or self.collection_name,
            embedding_function=embeddings,
            persist_directory=persist_dir or self.persist_dir
        )

        retriever = vector_store.as_retriever(
            search_type=self.search_type,
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

        # Chroma vector retriever
        chroma_retriever = vector_store.as_retriever(
            search_type=self.search_type,
            search_kwargs={
                "k": n_results
            }
        )


        # BM25 keyword retriever
        bm25_retriever = BM25Retriever.from_documents(
            documents,
            k=n_results
        )


        # Hybrid retrieval
        ensemble_retriever = EnsembleRetriever(
            retrievers=[
                bm25_retriever,
                chroma_retriever
            ],

            weights=[
                self.bm25_weight,
                self.vector_weight
            ]
        )


        results = ensemble_retriever.invoke(query)

        return results


    def rerank_documents(
        self,
        query: str,
        documents: list[Document],
        top_n: int = 3
    ) -> list[Document]:

        if not documents:
            return []


        # Load reranker model from config.yaml
        reranker = CrossEncoder(
            self.reranker_model
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