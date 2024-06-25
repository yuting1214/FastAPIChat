from typing import List, Dict, Optional, Tuple, Any
import aiohttp
import requests
import gradio as gr
from urllib.parse import urljoin
from backend.app.core.constants import (
    API_BASE_URL,
    TEXT_API_QUOTA_LIMIT
)

def get_client_ip(request: gr.Request) -> str:
    """Get the client's IP address from the request."""
    if request is None:
        return "Client IP not available"
    elif "cf-connecting-ip" in request.headers:
        return request.headers["cf-connecting-ip"]
    elif "x-forwarded-for" in request.headers:
        return request.headers["x-forwarded-for"]
    else:
        return request.client.host

def fetch_available_models(llm_type: str) -> Dict[str, str]:
    """Fetch available large language models from the base API URL."""
    models = {}
    url = urljoin(API_BASE_URL, f"api/v1/llms/type/{llm_type}")
    response = requests.get(url)
    assert response.status_code == 200
    model_info = response.json()

    for model in model_info:
        models[model["llm_model_name"]] = model["api_endpoint"]

    return models

async def start_chat(user_id: str, mode: str) -> str:
    url = urljoin(API_BASE_URL, "api/v1/chats/async")
    chat_data = {"user_id": user_id, "mode": mode}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=chat_data) as response:
            assert response.status == 200
            data = await response.json()
            return data["id"]

async def add_message_to_db(session: aiohttp.ClientSession, chat_id: str, content: str, message_type: str, origin: str):
    url = urljoin(API_BASE_URL, "api/v1/messages/async")
    message_data = {
        "chat_id": chat_id,
        "content": content,
        "message_type": message_type,
        "origin": origin
    }
    async with session.post(url, json=message_data) as message_response:
        assert message_response.status == 200

def load_terms_of_use_js() -> str:
    get_window_url_params_with_tos_js = """
    function() {
        const params = new URLSearchParams(window.location.search);
        url_params = Object.fromEntries(params);
        console.log("url_params", url_params);

        msg = "Users of this website are required to agree to the following terms:\\n\\nYour IP address will be logged for granting access to the service.\\n\\nFor the purpose of improving the service, user dialogue data, including both text and images, will be collected.\\n\\nThe service provides limited safety measures and may generate offensive content. It must not be used for any illegal, harmful, violent, racist, or sexual purposes.\\n\\nFor data privacy concerns, please refer to our local-host and self-hosting options.\\n "
        alert(msg);
        return url_params;
        }
    """
    return get_window_url_params_with_tos_js

def load_acknowledgement_md() -> str:
    acknowledgment_md = """
        ### Terms of Service

        Users of this website are required to agree to the following terms:

        * Your IP address will be logged for granting access to the service.
        * For the purpose of improving the service, user dialogue data, including both text and images, will be collected.
        * The service provides limited safety measures and may generate offensive content. It must not be used for any illegal, harmful, violent, racist, or sexual purposes.
        * For data privacy concerns, please refer to our local-host and self-hosting options.
        
        ### Acknowledgment
        This project is inspired by [LMSYS - FastChat](https://github.com/lm-sys/FastChat) and built upon on 
        * [FastAPI](https://fastapi.tiangolo.com/)
        * [Gradio](https://www.gradio.app/)
        * [OpenRouter](https://openrouter.ai/)

        <div style="display: flex; justify-content: left; align-items: center; margin: 20px 10px; gap: 20px;">
            <a href="https://fastapi.tiangolo.com/" target="_blank">
                <img src="https://fastapi.tiangolo.com/img/favicon.png" alt="FastAPI" style="max-width: 100px; height: auto;">
            </a>
            <a href="https://www.gradio.app/" target="_blank">
                <img src="https://www.gradio.app/_app/immutable/assets/gradio.CHB5adID.svg" alt="Gradio" style="max-width: 100px; height: auto;">
            </a>
            <a href="https://openrouter.ai/" target="_blank">
                <img src="https://avatars.githubusercontent.com/u/139423088?s=200&v=4" alt="OpenRouter" style="max-width: 100px; height: auto;">
            </a>
        </div>
    """
    return acknowledgment_md

def load_demo(url_params: gr.JSON, request: gr.Request) -> Tuple[Optional[Dict[str, str]], gr.Dropdown]:
    """Load the demo."""
    # API Quota Management
    api_quota_map = {
        # llm_type: (quota_limit, resource, task, mode)
        "text": (TEXT_API_QUOTA_LIMIT, "Text_API", "Chat", "chat")
    }

    # Parse the URL parameters
    base_api_url = API_BASE_URL
    llm_type = url_params.get("template_type", "")
    task = api_quota_map[llm_type][2]
    is_arena_ui = url_params.get("arena_ui", False)
    mode = "arena" if is_arena_ui else api_quota_map[llm_type][3]

    # Get the client's IP address
    client_ip = get_client_ip(request)

    # Check if the client is first time user
    user_ip_api_endpoint = urljoin(base_api_url, f"api/v1/users/ip/{client_ip}")
    user_ip_response = requests.get(user_ip_api_endpoint)
    first_time_user = user_ip_response.status_code != 200

    if first_time_user:
        # Create User Profile based on IP address
        user_api_endpoint = urljoin(base_api_url, "api/v1/users/")
        user_data = {"ip_address": client_ip}
        user_response = requests.post(user_api_endpoint, json=user_data)
        user_response.raise_for_status()
        user_id = user_response.json()["id"]
        user_name = user_response.json()["name"]

        # Create a new Quota(Text and Image API) for a the new user
        quota_api_endpoint = urljoin(base_api_url, "api/v1/quotas/")
        for llm_model_type in api_quota_map:
            quota_limit, resource, _, _ = api_quota_map[llm_model_type]
            quota_data = {"users": [{"id": user_id}], "quota_limit": quota_limit, "resource": resource}
            quota_response = requests.post(quota_api_endpoint, json=quota_data)
            assert quota_response.status_code == 200
    else:
        user_id = user_ip_response.json()["id"]
        user_name = user_ip_response.json()["name"]

    # Fetch available models 
    models = fetch_available_models(llm_type)
    model_names = list(models.keys())
    selected_model_1 = model_names[3] if model_names else ""
    selected_model_2 = model_names[1] if model_names else ""

    # Prepare the components in Gradio
    notice_markdown = f"""
        # 🏔️ Chat with Large Language Models

        ## 🌟 Welcome, {user_name}!

        We're excited to have you here. Start chatting with our advanced language models and see what they can do!

        ## 📚 Learn More:
        * [Github](https://github.com/yuting1214/FastAPIChat)
        * Project Walkthrough: [Personal Note](https://app.heptabase.com/w/80fcc9a0476f3a3ac30ac895c36eef51ede0bc4aa090cb7be1c6c0ed507cfda9)
        * See more in the [Gradio](https://www.gradio.app/) 📖

        ## 👇 Choose any models for {task}:
    """.format(user_name=user_name, task=task)

    markdown_update = gr.Markdown(notice_markdown)
    state = gr.State({
        "user_id": user_id,
        "user_name": user_name,
        "model_map": models,
        "mode": mode,
        "current_chat_id": None,
        "history": []
    })
    if is_arena_ui:
        model_1_dropdown_update = gr.Dropdown(label='LLM', choices=model_names, value=selected_model_1, visible=True, show_label=False)
        model_2_dropdown_update = gr.Dropdown(label='LLM', choices=model_names, value=selected_model_2, visible=True, show_label=False)
        return state, markdown_update, model_1_dropdown_update, model_2_dropdown_update
    else:
        model_dropdown_update = gr.Dropdown(label='LLM', choices=model_names, value=selected_model_1, visible=True)
        return state, markdown_update, model_dropdown_update
