from typing import Optional, List, Tuple, Generator
from dotenv import load_dotenv
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from llm.vendors.openrouter import ChatOpenRouter
from llm.prompt.base_text_templates import TEXT_PROMPT_TEMPLATE_V1

_ = load_dotenv('.env')

def llm_OpenRouter_chain_chat(user_input: str, history: Optional[List[str]]):

    # Manage the history of the conversation
    history_langchain_format = []
    for human, ai in zip(history[::2], history[1::2]):
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=user_input))
    
    # Model
    model = ChatOpenRouter(
        model_name = "mistralai/mistral-7b-instruct",
        temperature= 0.4,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TEXT_PROMPT_TEMPLATE_V1),
            ("user", "User Input: {user_input}")
        ]
    )

    chain = (
        {"user_input": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    return chain.invoke(user_input)

def llm_OpenRouter_chain_chat_stream(user_input: str, history: Optional[List[str]]):

    # Manage the history of the conversation
    history_langchain_format = []
    for human, ai in zip(history[::2], history[1::2]):
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=user_input))

    # Model
    model = ChatOpenRouter(
        model_name = "mistralai/mistral-7b-instruct",
        temperature= 0.4,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TEXT_PROMPT_TEMPLATE_V1),
            ("user", "User Input: {user_input}")
        ]
    )

    chain = (
        {"user_input": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    partial_message = ""
    for response in chain.stream(user_input):
        partial_message += response
        yield partial_message

def llm_OpenRouter_chain(user_input: str, model_name: str) -> str:

    # Model
    model = ChatOpenRouter(
        model_name = model_name,
        temperature= 0.4,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TEXT_PROMPT_TEMPLATE_V1),
            ("user", "User Input: {user_input}")
        ]
    )

    chain = (
        {"user_input": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    return chain.invoke(user_input)

def llm_OpenRouter_memory_chain(
        user_input: str,
        memory: List[Tuple[str, str]],
        model_name: str) -> str:

    # Model
    model = ChatOpenRouter(
        model_name = model_name,
        temperature= 0.4,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TEXT_PROMPT_TEMPLATE_V1),
            MessagesPlaceholder(variable_name="history"),
            ("user", "User Input: {user_input}")
        ]
    )

    chain = (
        prompt
        | model
        | StrOutputParser()
    )
    
    return chain.invoke({
        "user_input": user_input,
        "history": memory
    })



def llm_OpenRouter_chain_stream(
        user_input: str,
        model_endpoint: str,
        llm_params: dict
        ) -> Generator[str, None, None]:

    # Model
    model = ChatOpenRouter(
        model_name = model_endpoint,
        temperature= llm_params['temperature'],
        top_p= llm_params['top_p']
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", llm_params['system_prompt']),
            ("user", "User Input: {user_input}")
        ]
    )

    chain = (
        {"user_input": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    
    for partial_response in chain.stream(user_input):
        yield partial_response

def llm_OpenRouter_memory_chain_stream(
        user_input: str,
        model_endpoint: str,
        llm_params: dict,
        memory: List[Tuple[str, str]]
        ) -> Generator[str, None, None]:

    # Model
    model = ChatOpenRouter(
        model_name = model_endpoint,
        temperature= llm_params['temperature'],
        top_p= llm_params['top_p']
    )

    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", llm_params['system_prompt']),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
        ]
    )

    # Chain
    chain = (
        prompt
        | model
        | StrOutputParser()
    )
    
    for partial_response in chain.stream({"user_input": user_input, "history": memory}):
        yield partial_response
