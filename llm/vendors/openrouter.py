import os
from dotenv import load_dotenv
from typing import Optional
from langchain_community.chat_models import ChatOpenAI

# Reference: https://medium.com/@gal.peretz/openrouter-langchain-leverage-opensource-models-without-the-ops-hassle-9ffbf0016da7

_ = load_dotenv('.env')

class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str

    def __init__(self,
                 model_name: str,
                 openai_api_key: Optional[str] = None,
                 openai_api_base: str = "https://openrouter.ai/api/v1",
                 temperature: float = 1.0,
                 top_p: float = 1.0,
                 **kwargs):
        openai_api_key = os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name,
                         temperature=temperature,
                         top_p=top_p,
                         **kwargs)