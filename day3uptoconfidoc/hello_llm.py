
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langfuse.langchain import CallbackHandler

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from chunkmanager import ChunkManager
from retrivemanager import RetrieveManager
from storagemanager import StoreManager
from redactmanager import RedactManager
from config import load_config
from prompts import get_prmpt


load_dotenv()

# Load configuration
config = load_config()

# Load prompt version
prompt_det = get_prmpt("binance_qa", 2)


# Initialize managers
chunkman = ChunkManager(config)
storeman = StoreManager(config)
retrieveMan = RetrieveManager(config)
redact_manager = RedactManager(config)


# Langfuse callback
langfuse_handler = CallbackHandler()


# Debug function
def debug_step(data):
    print("...inspecting...")
    return data


# Read source document
with open("binance_hack.md", "r", encoding="utf-8") as fi:
    context_binance = fi.read()


# PII redaction
redacted_context = redact_manager.performRedacting_Of_PII(
    context_binance
)


# Chunking
chunks = chunkman.chunk_markdown(redacted_context)


# Embedding and storage
documents, vector_store = storeman.embed_and_store(chunks)


# Question
question = "What is Binance?"


# Hybrid retrieval
search_results = retrieveMan.query_hybrid(
    question,
    documents,
    vector_store,
    n_results=config["results"]["top"]
)


# Reranking
final_result = retrieveMan.rerank_documents(
    question,
    search_results,
    top_n=config["results"]["top"]
)


# Convert documents into context
retrieved_context = "\n\n".join(
    doc.page_content for doc in final_result
)


print("Redacted context:")
print(redacted_context[:250])


# Prompt template from prompt.yaml
prompt = ChatPromptTemplate.from_template(
    prompt_det["system"]
)


# Gemini LLM from config
llm = ChatGoogleGenerativeAI(
    model=config["llm"]["model"],
    temperature=config["llm"]["temperature"]
)


parser = StrOutputParser()


# Separate PII redaction Runnable
pii_redactor = RunnableLambda(
    redact_manager.performRedacting_Of_PII
)


# Uppercase Runnable
upper_case_convertor = RunnableLambda(
    lambda txt: txt.upper()
)


# Input preparation
def redact_input(data):

    data["question"] = pii_redactor.invoke(
        data["question"]
    )

    data["ctxt"] = retrieved_context

    return data


# Runnable for input preparation
input_redactor = RunnableLambda(redact_input)


# Build LCEL chain
chain = (

    input_redactor

    | prompt

    | llm

    | RunnableLambda(debug_step)

    | parser

    | RunnableLambda(debug_step)

    | upper_case_convertor

)


# Invoke chain with Langfuse metadata
response = chain.invoke(

    {
        "question": question,
        "ctxt": retrieved_context
    },

    config={

        "callbacks": [langfuse_handler],

        "metadata": {

            "langfuse_session_id": config["langfuse"]["session_id"],

            "langfuse_user_id": config["langfuse"]["user_id"],

            "prompt_name": prompt_det["name"],

            "prompt_version": prompt_det["version"]

        }

    }

)


print("\nFinal Response:")
print(response)
