import streamlit as st
import ollama
import requests
from typing import Dict, Iterable

def create_web_summary_app(url: str) -> str:
    """
    This function builds the Streamlit UI and functionalities for the Ollama chat app,
    fetches content from a given URL, sends it to the Ollama model for summarization,
    and returns the summary.
    """

    def fetch_web_content(url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text

    def fetch_ollama_replies(model: str, chat_history: Dict) -> Iterable:
        responses = ollama.chat(model=model, messages=chat_history, stream=True)
        for response in responses:
            yield response['message']['content']

    def get_models() -> list[str]:
        return [model["name"] for model in ollama.list()["models"]]

    web_content = fetch_web_content(url)
    models = get_models()
    if models:
        model = models[0]  # Assuming the first model is suitable for summarization
        chat_history = {"user": f"Summarize this content: {web_content}"}
        summary_generator = fetch_ollama_replies(model, chat_history)
        summary = next(summary_generator)  # Fetch the first summary response
        return summary
    else:
        return "No models available for summarization."

