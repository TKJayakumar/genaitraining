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
        "langfuse_session_id": "gold_session_1",
        "langfuse_user_id": "Gold_Market_User"
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
#     "What was the gold rate in Chennai on November 11, 2026?",
#     config=config
# )
# print(response.content)

conversation = [
    SystemMessage(
        content="You are a Chennai gold market expert who provides precise answers."
    ),
    HumanMessage(content="What is the difference between 22K and 24K gold?"),
    AIMessage(content="22K gold is mainly used for jewellery, while 24K gold is used for investment-grade coins and bars."),
    HumanMessage(content="What were the gold rates in Chennai on November 11, 2026?")
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

context_gold = ""

with open("gold_casetudy.md", "r", encoding="utf-8") as fi:
    all_lines = fi.readlines()

    for this_line in all_lines:
        context_gold += this_line + "\n"

conversation_template = ChatPromptTemplate([
    (
        "system",
        """You are a Chennai gold market expert who provides precise answers.

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
#     context=context_gold,
#     chat_history=conversation,
#     question="What were the gold rates in Chennai on November 11, 2026?"
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
    "context": context_gold,
    "chat_history": conversation,
    "question": "What were the 22K and 24K and 18K gold prices in Chennai on November 11, 2026?"
}

response = chain.invoke(
    dict_input,
    config=config
)

print("\nAnswer:")
print(response.msg)

print("\nReference:")
print(response.reference)