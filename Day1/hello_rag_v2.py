
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer, CrossEncoder

load_dotenv()


def chunk_markdown(markdown_text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["### ", "## ", "# ", "\n\n", "\n", " ", ""],
    )

    return text_splitter.split_text(markdown_text)


REPORT_PATH = "binance_hack.md"

with open(REPORT_PATH, "r", encoding="utf-8") as f:
    markdown_doc = f.read()

chunks = chunk_markdown(markdown_doc)

for i, chunk in enumerate(chunks):
    print(f"...>>>>... chunk num{i} has length {len(chunk)}")
    print(chunk[:100])


def embed_and_store(
    chunks: list[str],
    source: str = "binance_hack.md",
    persist_dir: str = "./chroma_db",
    collection_name: str = "binance_incident",
):

    print("...entering the conversion.....")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    vector_store.reset_collection()

    metadata_rows = []
    documents = []

    for i, chunk in enumerate(chunks):

        heading_lines = [
            line.strip()
            for line in chunk.splitlines()
            if line.strip().startswith('#')
        ]

        title = heading_lines[0] if heading_lines else "Untitled"

        metadata = {
            "source": source,
            "title": title,
            "chunk_index": str(i),
            "chunk_length": str(len(chunk))
        }

        metadata_rows.append(metadata)

        documents.append(
            Document(
                page_content=chunk,
                metadata=metadata
            )
        )

    vector_store.add_documents(
        documents=documents,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(".....converted the chunks to embedding...")

    return documents, vector_store


def query_chroma_db(
    query: str,
    collection_name: str = "binance_incident",
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
    query: str,
    documents: list[Document],
    top_n: int = 3
) -> list[Document]:

    reranker: CrossEncoder = CrossEncoder(
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

    return [doc for doc, score in top_pairs]


documents, vector_store = embed_and_store(chunks)

search_query = "How much money is lost due to the hack?"

search_results = query_hybrid(
    search_query,
    documents=documents,
    vector_store=vector_store,
    n_results=3
)

final_results = rerank_documents(
    search_query,
    search_results,
    top_n=3
)

print("\nFinal Reranked Results")

for i, res in enumerate(final_results):

    print(f"\n*** Result {i + 1} ***")
    print(f"Content:\n{res.page_content}")
    print(f"Metadata:\n{res.metadata}")
