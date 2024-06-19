import aiohttp
import asyncio
import requests
import time
import gradio as gr
import json
from typing import List, Optional, Tuple
from backend.app.core.constants import API_BASE_URL, MEMORY_WINDOW_SIZE
from frontend.gradio.utils import add_message_to_db, start_chat
from llm.memory.memory_management import format_memory

## Chat History Management
def delete_previous_chat(history: List[Tuple[str, Optional[str]]], request: gr.Request) -> List[Tuple[str, Optional[str]]]:
    if history:
        history.pop()
    return history

def delete_previous_chat_arena(history_1: List[Tuple[str, Optional[str]]], history_2: List[Tuple[str, Optional[str]]], request: gr.Request) -> List[Tuple[str, Optional[str]]]:
    if history_1:
        history_1.pop()
    if history_2:
        history_2.pop()
    return history_1, history_2

def delete_previous_system_message(history: List[Tuple[str, Optional[str]]], request: gr.Request) -> List[Tuple[str, Optional[str]]]:
    if history:
        history[-1][1] = None
    return history

def delete_previous_system_message_arena(history_1: List[Tuple[str, Optional[str]]], history_2: List[Tuple[str, Optional[str]]], request: gr.Request) -> List[Tuple[str, Optional[str]]]:
    if history_1:
        history_1[-1][1] = None
    if history_2:
        history_2[-1][1] = None
    return history_1, history_2

def add_text_in_history(user_message: str, history: List[Tuple[str, Optional[str]]], request: gr.Request) -> Tuple[str, List[Tuple[str, Optional[str]]]]:
    return "", history + [(user_message, None)]

def add_text_in_history_arena(user_message: str, history_1: List[Tuple[str, Optional[str]]], history_2: List[Tuple[str, Optional[str]]], request: gr.Request) -> Tuple[str, List[Tuple[str, Optional[str]]], List[Tuple[str, Optional[str]]]]:
    return "", history_1 + [(user_message, None)], history_2 + [(user_message, None)]

## Vote Management
def disable_vote_buttons():
    disable_btn = gr.Button(interactive=False)
    return [disable_btn, disable_btn]

def disable_vote_buttons_arena():
    disable_btn = gr.Button(interactive=False)
    return [disable_btn, disable_btn, disable_btn, disable_btn]

def enable_vote_buttons():
    enable_btn = gr.Button(interactive=True)
    return [enable_btn, enable_btn]

def enable_vote_buttons_arena():
    enable_btn = gr.Button(interactive=True)
    return [enable_btn, enable_btn, enable_btn, enable_btn]

def add_rating_to_db(state: gr.State, rating_type: str):
    chat_id = state.value['current_chat_id']
    if chat_id:
        rating_api_endpoint = API_BASE_URL + "api/v1/ratings/"
        rating_data = {
            "chat_id": chat_id,
            "rating_type": rating_type
        }
        response = requests.post(rating_api_endpoint, json=rating_data)
        assert response.status_code == 200

## Text Generation
async def fetch_llm_stream(session: aiohttp.ClientSession,
                          llm_api_endpoint: str,
                          llm_data: dict,
                          history: List[Tuple[str, Optional[str]]]):
    full_response = ""
    async with session.post(llm_api_endpoint, json=llm_data) as response:
        if response.status == 403:
            llm_response = "Quota limit reached. Please try again later."
            history[-1][1] = llm_response
            yield history, llm_response
        else:
            response.raise_for_status()  # Raise an error for other bad responses

            # Initialize the model response in the chat history
            if history:
                history[-1][1] = ""
            else:
                history.append((llm_data["user_input"], ""))

            # Process the streaming response
            async for chunk in response.content.iter_any():
                chunk_text = chunk.decode('utf-8')
                history[-1][1] += chunk_text
                yield history, chunk_text
                full_response += chunk_text
                await asyncio.sleep(0.01)  # Control the streaming speed for the interface

    yield history, full_response

def llm_text_completion_stream(state: gr.State, model_name: str, history: List[Tuple[str, Optional[str]]], request: gr.Request):
    
    # Fetch data from state
    user_id = state.value['user_id']
    user_message = history[-1][0] if history else ""
    model_endpoint = state.value['model_map'][model_name]

    # Call the LLM model with streaming
    llm_api_endpoint = API_BASE_URL + "api/v1/llm/generation/stream/text"
    llm_data = {
        "user_id": user_id,
        "api_endpoint": model_endpoint,
        "user_input": user_message,
        "is_arena": False
    }

    with requests.post(llm_api_endpoint, json=llm_data, stream=True) as response:
        # Check if the quota limit is reached
        if response.status_code == 403:
            llm_response = "Quota limit reached. Please try again later."
            full_response = llm_response
            history[-1][1] = llm_response
            yield history
        else:
            response.raise_for_status()  # Raise an error for other bad responses

            # Initialize the model response in the chat history
            if history:
                history[-1][1] = ""
            else:
                history.append((user_message, ""))

            # Process the streaming response
            full_response = ""
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                history[-1][1] += chunk
                yield history
                full_response += chunk
                time.sleep(0.01)  # Control the streaming speed for the interface

    # Add Message data(user) into DB
    message_api_endpoint = API_BASE_URL + "api/v1/messages/"
    message_data_user = {
        "user_id": user_id,
        "content": user_message,
        "message_type": "text",
        "origin": "user"
    }
    message_response = requests.post(message_api_endpoint, json=message_data_user)
    assert message_response.status_code == 200

    # Add the complete model response to the DB
    message_data_model = {
        "user_id": user_id,
        "content": full_response,
        "message_type": "text",
        "origin": "model"
    }
    message_response = requests.post(message_api_endpoint, json=message_data_model)
    assert message_response.status_code == 200

    # Final yield to ensure the entire message is updated in the interface
    yield history

async def llm_text_completion_stream_async(
        state: gr.State,
        model_name: str,
        system_prompt: str,
        temperature: float,
        top_p: float,
        history: List[Tuple[str, Optional[str]]],
        request: gr.Request):
    
    # Fetch data from state
    user_id = state.value['user_id']
    user_message = history[-1][0] if history else ""
    model_endpoint = state.value['model_map'][model_name]
    mode = state.value['mode']

    # Start a chat
    chat_id = await start_chat(user_id, mode)
    state.value['current_chat_id'] = chat_id

    # Call the LLM model with streaming
    llm_api_endpoint = API_BASE_URL + "api/v1/llm/generation/stream/text"
    llm_params = {
        "system_prompt": system_prompt,
        "temperature": temperature,
        "top_p": top_p
    }
    llm_data = {
        "user_id": user_id,
        "chat_id": chat_id,
        "api_endpoint": model_endpoint,
        "user_input": user_message,
        "is_arena": False,
        "llm_params": llm_params
    }

    async with aiohttp.ClientSession() as session:
        fetch_task = fetch_llm_stream(session, llm_api_endpoint, llm_data, history)

        full_response = ""
        while True:
            task_done = False

            try:
                history, full_response = await fetch_task.__anext__()
                yield state, history
            except StopAsyncIteration:
                task_done = True

            if task_done:
                break

        # Add Message data(user) into DB
        await add_message_to_db(session, chat_id, user_message, "text", "user")

        # Add Message data(model) into DB
        await add_message_to_db(session, chat_id, full_response, "text", "model")

    # Final yield to ensure the entire message is updated in the interface
    yield state, history

async def llm_text_completion_memory_stream_async(
        state: gr.State,
        model_name: str,
        system_prompt: str,
        temperature: float,
        top_p: float,
        history: List[Tuple[str, Optional[str]]],
        request: gr.Request):
    
    # Fetch data from state
    user_id = state.value['user_id']
    user_message = history[-1][0] if history else ""
    model_endpoint = state.value['model_map'][model_name]
    mode = state.value['mode']
    formated_history = format_memory(history[:-1], window_size=MEMORY_WINDOW_SIZE)

    # Start a chat
    chat_id = await start_chat(user_id, mode)
    state.value['current_chat_id'] = chat_id

    # Call the LLM model with streaming
    llm_api_endpoint = API_BASE_URL + "api/v1/llm/generation/stream/text/memory"
    llm_params = {
        "system_prompt": system_prompt,
        "temperature": temperature,
        "top_p": top_p
    }
    llm_data = {
        "user_id": user_id,
        "chat_id": chat_id,
        "api_endpoint": model_endpoint,
        "user_input": user_message,
        "is_arena": False,
        "llm_params": llm_params,
        'formated_history': formated_history
    }

    async with aiohttp.ClientSession() as session:
        fetch_task = fetch_llm_stream(session, llm_api_endpoint, llm_data, history)

        full_response = ""
        while True:
            task_done = False

            try:
                history, full_response = await fetch_task.__anext__()
                yield state, history
            except StopAsyncIteration:
                task_done = True

            if task_done:
                break

        # Add Message data(user) into DB
        await add_message_to_db(session, chat_id, user_message, "text", "user")

        # Add Message data(model) into DB
        await add_message_to_db(session, chat_id, full_response, "text", "model")

    # Final yield to ensure the entire message is updated in the interface
    yield state, history

async def llm_text_completion_stream_arena(
        state: gr.State,
        model_1_name: str,
        system_prompt_1: str,
        temperature_1: float,
        top_p_1: float,
        model_2_name: str,
        system_prompt_2: str,
        temperature_2: float,
        top_p_2: float,
        history_1: List[Tuple[str, Optional[str]]],
        history_2: List[Tuple[str, Optional[str]]],
        request: gr.Request):
    
    # Fetch data from state
    user_id = state.value['user_id']
    user_message = history_1[-1][0] if history_1 else ""
    mode = state.value['mode']
    model_endpoint_1 = state.value['model_map'][model_1_name]
    model_endpoint_2 = state.value['model_map'][model_2_name]

    # Start a chat
    chat_id = await start_chat(user_id, mode)
    state.value['current_chat_id'] = chat_id

    # Call the LLM model with streaming
    llm_api_endpoint = API_BASE_URL + "api/v1/llm/generation/stream/text"
    llm_params_1 = {
        "system_prompt": system_prompt_1,
        "temperature": temperature_1,
        "top_p": top_p_1
    }  
    llm_data_1 = {
        "user_id": user_id,
        "api_endpoint": model_endpoint_1,
        "user_input": user_message,
        "chat_id": chat_id,
        "llm_label": "model_1",
        "is_arena": True,
        "llm_params": llm_params_1
    }

    llm_params_2 = {
        "system_prompt": system_prompt_2,
        "temperature": temperature_2,
        "top_p": top_p_2
    }     
    llm_data_2 = {
        "user_id": user_id,
        "api_endpoint": model_endpoint_2,
        "user_input": user_message,
        "chat_id": chat_id,
        "llm_label": "model_2",
        "is_arena": True,
        "llm_params": llm_params_2
    }

    async with aiohttp.ClientSession() as session:
        fetch_task_1 = fetch_llm_stream(session, llm_api_endpoint, llm_data_1, history_1)
        fetch_task_2 = fetch_llm_stream(session, llm_api_endpoint, llm_data_2, history_2)

        response_1 = ""
        response_2 = ""
        while True:
            task_1_done = False
            task_2_done = False

            try:
                history_1, response_1 = await fetch_task_1.__anext__()
                yield state, history_1, history_2
            except StopAsyncIteration:
                task_1_done = True
            
            try:
                history_2, response_2 = await fetch_task_2.__anext__()
                yield state, history_1, history_2
            except StopAsyncIteration:
                task_2_done = True

            if task_1_done and task_2_done:
                break

        await add_message_to_db(session, chat_id, user_message, "text", "user")
        await add_message_to_db(session, chat_id, response_1, "text", "model")
        await add_message_to_db(session, chat_id, response_2, "text", "model")

    # Final yield to ensure the entire message is updated in the interface
    yield state, history_1, history_2

async def llm_text_completion_memory_stream_arena(
        state: gr.State,
        model_1_name: str,
        system_prompt_1: str,
        temperature_1: float,
        top_p_1: float,
        model_2_name: str,
        system_prompt_2: str,
        temperature_2: float,
        top_p_2: float,
        history_1: List[Tuple[str, Optional[str]]],
        history_2: List[Tuple[str, Optional[str]]],
        request: gr.Request):
    
    # Fetch data from state
    user_id = state.value['user_id']
    user_message = history_1[-1][0] if history_1 else ""
    mode = state.value['mode']
    model_endpoint_1 = state.value['model_map'][model_1_name]
    model_endpoint_2 = state.value['model_map'][model_2_name]
    formated_history_1 = format_memory(history_1[:-1], window_size=MEMORY_WINDOW_SIZE)
    formated_history_2 = format_memory(history_2[:-1], window_size=MEMORY_WINDOW_SIZE)

    # Start a chat
    chat_id = await start_chat(user_id, mode)
    state.value['current_chat_id'] = chat_id

    # Call the LLM model with streaming
    llm_api_endpoint = API_BASE_URL + "api/v1/llm/generation/stream/text/memory"
    llm_params_1 = {
        "system_prompt": system_prompt_1,
        "temperature": temperature_1,
        "top_p": top_p_1
    }  
    llm_data_1 = {
        "user_id": user_id,
        "api_endpoint": model_endpoint_1,
        "user_input": user_message,
        "chat_id": chat_id,
        "llm_label": "model_1",
        "is_arena": True,
        "llm_params": llm_params_1,
        'formated_history': formated_history_1
    }

    llm_params_2 = {
        "system_prompt": system_prompt_2,
        "temperature": temperature_2,
        "top_p": top_p_2
    }     
    llm_data_2 = {
        "user_id": user_id,
        "api_endpoint": model_endpoint_2,
        "user_input": user_message,
        "chat_id": chat_id,
        "llm_label": "model_2",
        "is_arena": True,
        "llm_params": llm_params_2,
        'formated_history': formated_history_2
    }

    async with aiohttp.ClientSession() as session:
        fetch_task_1 = fetch_llm_stream(session, llm_api_endpoint, llm_data_1, history_1)
        fetch_task_2 = fetch_llm_stream(session, llm_api_endpoint, llm_data_2, history_2)

        response_1 = ""
        response_2 = ""
        while True:
            task_1_done = False
            task_2_done = False

            try:
                history_1, response_1 = await fetch_task_1.__anext__()
                yield state, history_1, history_2
            except StopAsyncIteration:
                task_1_done = True
            
            try:
                history_2, response_2 = await fetch_task_2.__anext__()
                yield state, history_1, history_2
            except StopAsyncIteration:
                task_2_done = True

            if task_1_done and task_2_done:
                break

        await add_message_to_db(session, chat_id, user_message, "text", "user")
        await add_message_to_db(session, chat_id, response_1, "text", "model")
        await add_message_to_db(session, chat_id, response_2, "text", "model")

    # Final yield to ensure the entire message is updated in the interface
    yield state, history_1, history_2
