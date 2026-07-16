# ============================================================
# Imports
# ============================================================
from openai import OpenAI
from IPython.display import Markdown, display
from enum import Enum
import os

# ============================================================
# Client setup (Vocareum API endpoint)
# ============================================================
client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),  # set this in your environment, don't hardcode it
)

# If using OpenAI's own API endpoint instead, comment out the block above and use:
# client = OpenAI()

# ============================================================
# Model selection + helper functions
# ============================================================
class OpenAIModels(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"


MODEL = OpenAIModels.GPT_41_NANO


def get_completion(system_prompt, user_prompt, model=MODEL):
    """
    Function to get a completion from the OpenAI API.
    Args:
        system_prompt: The system prompt
        user_prompt: The user prompt
        model: The model to use (default is gpt-4.1-mini)
    Returns:
        The completion text
    """
    messages = [
        {"role": "user", "content": user_prompt},
    ]
    if system_prompt is not None:
        messages = [
            {"role": "system", "content": system_prompt},
            *messages,
        ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


def display_responses(*args):
    """Helper function to display responses as Markdown, horizontally."""
    markdown_string = "<table><tr>"
    for arg in args:
        markdown_string += f"<th>System Prompt:<br />{arg['system_prompt']}<br /><br />"
        markdown_string += f"User Prompt:<br />{arg['user_prompt']}</th>"
    markdown_string += "</tr>"
    markdown_string += "<tr>"
    for arg in args:
        markdown_string += f"<td>Response:<br />{arg['response']}</td>"
    markdown_string += "</tr></table>"
    display(Markdown(markdown_string))

# ============================================================
# Baseline test run
# ============================================================
plain_system_prompt = "You are a helpful assistant."
user_prompt = "Give me a simple plan to declutter and organize my workspace."

print(f"Sending prompt to {MODEL} model...")
baseline_response = get_completion(plain_system_prompt, user_prompt)
print("Response received!\n")

display_responses(
    {
        "system_prompt": plain_system_prompt,
        "user_prompt": user_prompt,
        "response": baseline_response,
    }
)
