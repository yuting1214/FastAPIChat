from typing import Any, Dict
import gradio as gr
from frontend.gradio.text.event_listeners import (
    delete_previous_system_message,
    delete_previous_chat,
    add_text_in_history,
    enable_vote_buttons,
    disable_vote_buttons,
    add_rating_to_db,
    llm_text_completion_memory_stream_async
)
from frontend.gradio.utils import load_demo, load_terms_of_use_js, load_acknowledgement_md
from backend.app.core.constants import CONCURRENCY_LIMIT
from llm.prompt.base_text_templates import TEXT_PROMPT_TEMPLATE_V1

def build_demo(template_type: str, arena_ui: bool = False):
    with gr.Blocks(
        title="🤖 LLM Chat",
        theme=gr.themes.Default(),
    ) as demo:
        
        # Prepare the state to store data
        url_params = gr.State(value={"template_type": template_type, "arena_ui": arena_ui})
        state = gr.State({})

        # Gradio Layout
        with gr.Row():
            with gr.Column(scale=8):
                with gr.Accordion(f"Overview", open=True):
                    gr_markdown = gr.Markdown()
            with gr.Column(scale=1):
                toggle_dark = gr.Button(value="Toggle Dark")

        with gr.Group(elem_id="share-region-named"):
            
            model_selector = gr.Dropdown()

            with gr.Accordion("Parameters", open=False):
                system_prompt = gr.Textbox(label="System Prompt", value=TEXT_PROMPT_TEMPLATE_V1, lines=2)
                temperature = gr.Slider(label="Temperature", minimum=0.0, maximum=2.0, value=1.0)
                top_p = gr.Slider(label="Top-p", minimum=0.0, maximum=1.0, value=1.0)

            with gr.Row(elem_id="model_selector_row"):
                chatbot = gr.Chatbot(
                    elem_id="chatbot",
                    label="Scroll down and start chatting",
                    height=300,
                    show_copy_button=True,
                )
                                    
            with gr.Row():
                upvote_btn = gr.Button(value="👍  Upvote", interactive=False)
                downvote_btn = gr.Button(value="👎  Downvote", interactive=False)

        with gr.Row():
            textbox = gr.Textbox(
                show_label=False,
                placeholder="👉 Enter your prompt and press ENTER",
                elem_id="input_box",
            )
            send_btn = gr.Button(value="Send", variant="primary", scale=0)

        with gr.Row():
            regenerate_btn = gr.Button(value="🔄  Regenerate", interactive=True)
            delete_pre_btn = gr.Button(value="❌  Delete Previous", interactive=True)
            clear_btn = gr.Button(value="🗑️  Clear history", interactive=True)

        with gr.Row():
            with gr.Accordion(f"Acknowledgment", open=False):
                gr_ac_markdown =  gr.Markdown(load_acknowledgement_md(), elem_id="ack_markdown")
        
        # Event Listeners
        ## Dark Mode
        toggle_dark.click(
            None,
            js="""
            () => {
                document.body.classList.toggle('dark');
                document.querySelector('gradio-app').style.backgroundColor = 'var(--color-background-primary)'
            }
            """,
        )
    
        ## User Text Input
        textbox.submit(
            add_text_in_history,
            [textbox, chatbot],
            [textbox, chatbot]
        ).then(
            disable_vote_buttons,
            None,
            [upvote_btn, downvote_btn]
        ).then(
            llm_text_completion_memory_stream_async,
            [state, model_selector, system_prompt, temperature, top_p, chatbot],
            [state, chatbot]
        ).then(
            enable_vote_buttons,
            None,
            [upvote_btn, downvote_btn]
        )

        send_btn.click(
            add_text_in_history,
            [textbox, chatbot],
            [textbox, chatbot]
        ).then(
            disable_vote_buttons,
            None,
            [upvote_btn, downvote_btn]
        ).then(
            llm_text_completion_memory_stream_async,
            [state, model_selector, system_prompt, temperature, top_p, chatbot],
            [state, chatbot]
        ).then(
            enable_vote_buttons,
            None,
            [upvote_btn, downvote_btn]
        )

        ## Vote buttons
        upvote_btn.click(
            lambda state: add_rating_to_db(state, 'upvote'),
            state,
            None
        ).then(
            disable_vote_buttons,
            None,
            [upvote_btn, downvote_btn]
        )

        downvote_btn.click(
            lambda state: add_rating_to_db(state, 'downvote'),
            state,
            None
        ).then(
            disable_vote_buttons,
            None,
            [upvote_btn, downvote_btn]
        )
        
        ## Regenerate button
        regenerate_btn.click(
            delete_previous_system_message,
            [chatbot],
            chatbot
        ).then(
            llm_text_completion_memory_stream_async,
            [state, model_selector, system_prompt, temperature, top_p, chatbot],
            [state, chatbot]
        ).then(
            enable_vote_buttons,
            None,
            [upvote_btn, downvote_btn]
        )

        ## Delete Previous button
        delete_pre_btn.click(
            delete_previous_chat,
            [chatbot],
            chatbot
        )

        ## Clear button
        clear_btn.click(
            lambda: None,
            None,
            chatbot
        )

        # Preload the demo
        demo.load(
            load_demo,
            [url_params],
            [state, gr_markdown, model_selector],
            js = load_terms_of_use_js()
        )

        # Set Concurrencies
        demo.queue(default_concurrency_limit=CONCURRENCY_LIMIT,
                   api_open=False)

    return demo