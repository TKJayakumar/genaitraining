
from dotenv import load_dotenv
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langfuse.langchain import CallbackHandler
from pydantic import BaseModel, Field

load_dotenv()

langfuse_handler = CallbackHandler()

config = {
    "callbacks": [langfuse_handler],
    "metadata": {
        "langfuse_session_id": "binance_session_1",
        "langfuse_user_id": "Nalla"
    }
}

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.3,
    timeout=15,
    max_tokens=1500,
    max_retries=3
)

# Direct LLM invocation
# response = llm.invoke(
#     "What is the value of the recent hack attack on Binance?",
#     config=config
# )
# print(response.content)

conversation = [
    SystemMessage(
        content="You are a software security expert who provides precise answers."
    ),
    HumanMessage(content="What is Binance?"),
    AIMessage(content="Binance is a popular cryptocurrency exchange company."),
    HumanMessage(content="Was it hacked recently?")
]

class CustomResponse(BaseModel):
    msg: str = Field(description="The short answer")
    reference: Optional[str] = None

llm_with_structure = llm.with_structured_output(CustomResponse)

# Structured output using conversation history
# response = llm_with_structure.invoke(
#     conversation,
#     config=config
# )
# print(response.msg)
# print(response.reference)

context_binance = ""

with open("binance_hack.md", "r", encoding="utf-8") as fi:
    all_lines = fi.readlines()

    for this_line in all_lines:
        context_binance += this_line + "\n"

conversation_template = ChatPromptTemplate([
    (
        "system",
        """You are a software security expert who provides precise answers.

        Answer the question using only the provided context.

        Context:
        {context}

        If the answer is unavailable in the context,
        clearly mention that it is unavailable.

        Do not invent facts or references."""
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# Prompt formatting approach
# formatted_conversation = conversation_template.format_messages(
#     context=context_binance,
#     chat_history=conversation,
#     question="Was Binance hacked recently?"
# )
#
# response = llm_with_structure.invoke(
#     formatted_conversation,
#     config=config
# )
#
# print(response.msg)
# print(response.reference)

def validate(resp: CustomResponse) -> CustomResponse:
    if not resp.reference:
        return CustomResponse(
            msg="Sorry, no reference available.",
            reference=None
        )
    return resp

chain = (
    conversation_template
    | llm_with_structure
    | RunnableLambda(validate)
)

dict_input = {
    "context": context_binance,
    "chat_history": conversation,
    "question": "How much was lost in Nvidia because of Jensen Huang?"
}

response = chain.invoke(
    dict_input,
    config=config
)

print("\nAnswer:")
print(response.msg)

print("\nReference:")
print(response.reference)
