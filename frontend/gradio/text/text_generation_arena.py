from typing import Any, Dict
import gradio as gr
from frontend.gradio.text.event_listeners import (
    delete_previous_chat_arena,
    delete_previous_system_message_arena,
    enable_vote_buttons_arena,
    disable_vote_buttons_arena,
    add_text_in_history_arena,
    add_rating_to_db,
    llm_text_completion_memory_stream_arena
)
from frontend.gradio.utils import load_demo, load_terms_of_use_js, load_acknowledgement_md
from llm.prompt.base_text_templates import TEXT_PROMPT_TEMPLATE_V1

def build_arena_demo(template_type: str, arena_ui: bool = False):
    with gr.Blocks(
        title="⚔️ LLM Arena",
        theme=gr.themes.Default(),
    ) as demo:
        num_sides = 2
        chatbots = [None] * num_sides
        params = [ [None, None, None] for i in range(num_sides)]
        model_labels = ['Model A', 'Model B']

        # Prepare the state to store data
        url_params = gr.State(value={"template_type": template_type, "arena_ui": arena_ui})
        state = gr.State({})

        # Gradio Layout(Preload from load_demo function)
        with gr.Row():
            with gr.Column(scale=8):
                with gr.Accordion(f"Overview", open=True):
                    gr_markdown = gr.Markdown()
            with gr.Column(scale=1):
                toggle_dark = gr.Button(value="Toggle Dark")

        with gr.Group(elem_id="share-region-named"):
            with gr.Row():
                for i in range(num_sides):
                    with gr.Column():
                        if i == 0:
                            model_1_selector = gr.Dropdown()
                        else:
                            model_2_selector = gr.Dropdown()

                        with gr.Accordion(f"Parameters_{i+1}", open=False):
                            params[i][0] = gr.Textbox(label="System Prompt", value=TEXT_PROMPT_TEMPLATE_V1, lines=5)
                            params[i][1] = gr.Slider(label="Temperature", minimum=0.0, maximum=2.0, value=1.0)
                            params[i][2] = gr.Slider(label="Top-p", minimum=0.0, maximum=1.0, value=1.0)
                        
                        chatbots[i] = gr.Chatbot(
                            label=model_labels[i],
                            elem_id=f"chatbot_{i}",
                            height=550,
                            show_copy_button=True,
                        )

            with gr.Row():
                model_1_better_btn = gr.Button(value="👈 better", interactive=False)
                model_2_better_btn = gr.Button(value="👉 better", interactive=False)
                tie_btn = gr.Button(value="🤝 Tie", interactive=False)
                both_bad_btn = gr.Button(value="👎 Both bad", interactive=False)

        with gr.Row():
            textbox = gr.Textbox(
                show_label=False,
                placeholder="👉 Enter your prompt and press ENTER",
                elem_id="input_box",
            )
            send_btn = gr.Button(value="Send", variant="primary", scale=0)

        with gr.Row() as button_row:
            regenerate_btn = gr.Button(value="🔄  Regenerate", interactive=True)
            delete_pre_btn = gr.Button(value="❌  Delete Previous", interactive=True)
            clear_btn = gr.Button(value="🗑️  Clear history", interactive=True)

        with gr.Row():
            with gr.Accordion(f"Acknowledgment", open=True):
                gr_ac_markdown =  gr.Markdown(load_acknowledgement_md(), elem_id="ack_markdown")

        # Event Listeners
        llm_input_boxes = [state] + [model_1_selector] + params[0] + [model_2_selector] + params[1] + [chatbots[0], chatbots[1]]

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
            add_text_in_history_arena,
            [textbox, chatbots[0], chatbots[1]],
            [textbox, chatbots[0], chatbots[1]]
        ).then(
            disable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        ).then(
            llm_text_completion_memory_stream_arena,
            llm_input_boxes,
            [state, chatbots[0], chatbots[1]]
        ).then(
            enable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        )

        send_btn.click(
            add_text_in_history_arena,
            [textbox, chatbots[0], chatbots[1]],
            [textbox, chatbots[0], chatbots[1]]
        ).then(
            disable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        ).then(
            llm_text_completion_memory_stream_arena,
            llm_input_boxes,
            [state, chatbots[0], chatbots[1]]
        ).then(
            enable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        )

        ## Vote buttons
        model_1_better_btn.click(
            lambda state: add_rating_to_db(state, 'model_1_better'),
            state,
            None
        ).then(
            disable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        )

        model_2_better_btn.click(
            lambda state: add_rating_to_db(state, 'model_2_better'),
            state,
            None
        ).then(
            disable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        )
    
        tie_btn.click(
            lambda state: add_rating_to_db(state, 'tie'),
            state,
            None
        ).then(
            disable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        )

        both_bad_btn.click(
            lambda state: add_rating_to_db(state, 'both_bad'),
            state,
            None
        ).then(
            disable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        )

        ## Regenerate button
        regenerate_btn.click(
            delete_previous_system_message_arena,
            [chatbots[0], chatbots[1]],
            [chatbots[0], chatbots[1]]
        ).then(
            llm_text_completion_memory_stream_arena,
            llm_input_boxes,
            [state, chatbots[0], chatbots[1]]
        ).then(
            enable_vote_buttons_arena,
            None,
            [model_1_better_btn, model_2_better_btn, tie_btn, both_bad_btn]
        )

        ## Delete Previous button
        delete_pre_btn.click(
            delete_previous_chat_arena,
            [chatbots[0], chatbots[1]],
            [chatbots[0], chatbots[1]]
        )

        ## Clear button
        clear_btn.click(
            lambda x, y: (None, None),
            [chatbots[0], chatbots[1]],
            [chatbots[0], chatbots[1]]
        )

        # Preload the demo
        demo.load(
            load_demo,
            [url_params],
            [state, gr_markdown, model_1_selector, model_2_selector],
            js = load_terms_of_use_js()
        )

    return demo