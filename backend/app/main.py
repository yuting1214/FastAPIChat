import os
import uvicorn
import gradio as gr
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app.core.init_settings import args, global_settings
from backend.app.core.constants import API_BASE_URL
from backend.app.api.v1.endpoints import (
    user,
    chat,
    rating,
    api_usage,
    api_calldetail,
    message,
    llm_management,
    text_generation,
    quota,
    doc
)
from backend.app.crud.llm import create_llm_crud_async
from backend.app.dependencies.database import init_db, AsyncSessionLocal
from backend.data.llm_models import models_data
from llm.llm_text_chain import llm_OpenRouter_chain_chat_stream
from frontend.gradio.text.text_generation import build_demo
from frontend.gradio.text.text_generation_arena import build_arena_demo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database connection
    init_db()

    # Insert the available LLM models into the database
    async with AsyncSessionLocal() as db:
        try:
            for model in models_data:
                await create_llm_crud_async(db, model)  # Use await for async function call
        finally:
            await db.close()

    yield


app = FastAPI(lifespan=lifespan)

# Frontend
templates = Jinja2Templates(directory="frontend/login/templates")
app.mount("/static", StaticFiles(directory="frontend/login/static"), name="static")

# Set Middleware
# Define the allowed origins
origins = [
    global_settings.API_BASE_URL,
    "http://localhost",
    "http://localhost:5000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Document protection middleware
@app.middleware("http")
async def add_doc_protect(request: Request, call_next):
    if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
        if not request.session.get('authenticated'):
            return RedirectResponse(url="/login")
    response = await call_next(request)
    return response
# Add session middleware with a custom expiration time (e.g., 30 minutes)
app.add_middleware(SessionMiddleware, 
                   secret_key="your_secret_key", 
                   max_age=18000)  # 18000 seconds = 300 minutes

# Add the routers to the FastAPI app
app.include_router(user.router, prefix="/api/v1", tags=["user"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(rating.router, prefix="/api/v1", tags=["rating"])
app.include_router(api_usage.router, prefix="/api/v1", tags=["api_usage"])
app.include_router(api_calldetail.router, prefix="/api/v1", tags=["api_calldetail"])
app.include_router(message.router, prefix="/api/v1", tags=["message"])
app.include_router(text_generation.router, prefix="/api/v1", tags=["llm_generation"])
app.include_router(llm_management.router, prefix="/api/v1", tags=["llm_management"])
app.include_router(quota.router, prefix="/api/v1", tags=["quota"])
app.include_router(doc.router, prefix="", tags=["doc"])

# Gradio app
demo_1 = gr.ChatInterface(
    fn=llm_OpenRouter_chain_chat_stream,
    textbox=gr.Textbox(
        placeholder="Ask a question", container=False, lines=1, scale=8
    ),
    title="LLM App",
    undo_btn="Delete Previous",
    clear_btn="Clear",
)

demo_2 = build_demo("text")

demo_3 = build_arena_demo("text", arena_ui=True)

# Mounting the Gradio app for text generation
app = gr.mount_gradio_app(app, demo_1, path="/chatbot-without-tracking", root_path="/chatbot-without-tracking", favicon_path = "frontend/favicon.png")
# Mounting the Gradio app for text generation with API tracking
app = gr.mount_gradio_app(app, demo_2, path="/chatbot", root_path="/chatbot", favicon_path = "frontend/favicon.png")
# Mounting the Gradio app for text generation with Arena
app = gr.mount_gradio_app(app, demo_3, path="/arena", root_path="/arena", favicon_path = "frontend/favicon.png")

if __name__ == "__main__":
    # mounting at the root path
    uvicorn.run(
        app="backend.app.main:app",
        host = args.host,
        port=int(os.getenv("PORT", 5000)),
        reload=args.mode == "dev"  # Enables auto-reloading in development mode
    )