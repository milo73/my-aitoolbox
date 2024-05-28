import ollama
from typing import Dict, Iterable

def fetch_ollama_replies(model: str, chat_history: Dict) -> Iterable:
    responses = ollama.chat(model=model, messages=chat_history, stream=True)
    for response in responses:
        yield response['message']['content']

def get_models() -> list[str]:
    return [model["name"] for model in ollama.list()["models"]]