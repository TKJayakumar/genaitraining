
from dotenv import load_dotenv

from chunkmanager import ChunkManager
from storagemanager import StoreManager
from retrivemanager import RetrieveManager

load_dotenv()

REPORT_PATH = "binance_hack.md"

with open(REPORT_PATH, "r", encoding="utf-8") as f:
    markdown_doc = f.read()

chunkMan = ChunkManager()

chunks = chunkMan.chunk_markdown(markdown_doc)

for i, chunk in enumerate(chunks):
    print(f"...>>>>... chunk num{i} has length {len(chunk)}")
    print(chunk[:100])

storeMan = StoreManager()

documents, vector_store = storeMan.embed_and_store(chunks)

retrieveMan = RetrieveManager()

search_query = "What is the value of the attack in binance?"

results = retrieveMan.query_hybrid(
    search_query,
    documents=documents,
    vector_store=vector_store,
    n_results=3
)

final_results = retrieveMan.rerank_documents(
    search_query,
    results,
    top_n=3
)

print("\nFinal Reranked Results")

for i, res in enumerate(final_results):

    print(f"\n*** Result {i + 1} ***")
    print(f"Content:\n{res.page_content}")
    print(f"Metadata:\n{res.metadata}")
