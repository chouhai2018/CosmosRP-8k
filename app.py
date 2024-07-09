import gradio as gr
import logging
from openai import OpenAI
import os

# Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://api.pawan.krd/cosmosrp/v1",
    api_key="no key is needed for this model",
)


def generate_text(
    message,
    history: list[tuple[str, str]],
    my_char,
    my_user,
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    in_text = message
    history_prompt = []
    temp = ""
    # Create system_prompt as a dictionary
    system_prompt = {"role": "system", "content": system_message}

    # Create history_prompt as a list of dictionaries
    for interaction in history:
        user_part = {"role": "user", "content": str(interaction[0])}
        assistant_part = {"role": "assistant", "content": str(interaction[1])}
        history_prompt.extend([user_part, assistant_part])

    # Create user_input_part as a dictionary
    user_input_part = {"role": "user", "content": str(in_text)}

    # Construct input_prompt as a list of dictionaries
    if history:
        input_prompt = [system_prompt] + history_prompt + [user_input_part]
    else:
        input_prompt = [system_prompt] + [user_input_part]
    # input_prompt = [user_input_part]
    # logger.debug(f"Input Prompt: {input_prompt}")
    completion = client.chat.completions.create(
        model="cosmosrp",
        messages=input_prompt,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in completion:
        if (
            hasattr(chunk.choices[0].delta, "content")
            and chunk.choices[0].delta.content is not None
        ):
            temp += chunk.choices[0].delta.content.replace("{{char}}", f"{my_char}").replace("{{user}}", f"{my_user}")
            yield temp

demo = gr.ChatInterface(
    generate_text,
    title="CosmosRP-8k",
    cache_examples=False,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    additional_inputs=[
        gr.Textbox(
            value="Master",
            label="{{char}}",
        ),
        gr.Textbox(
            value="Novice",
            label="{{user}}",
        ),
        gr.Textbox(
            value="你是一个格莱美获奖的音乐人,总是使用音乐语言回应,只讲普通话,仅用中文对话.",
            label="System message",
        ),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.5, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)

if __name__ == "__main__":
    demo.launch()
