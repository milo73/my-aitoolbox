import ollama
from typing import Dict, Iterable
import os
from dotenv import load_dotenv 

load_dotenv()

# Load model parameters
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL")
WHISPER_MODEL = os.getenv("WHISPER_MODEL")


def fetch_ollama_replies(model: str, chat_history: Dict, temperature: float) -> Iterable:
    responses = ollama.chat(model=model, messages=chat_history, stream=True, options={"temperature": temperature})
    for response in responses:
        yield response['message']['content']

def get_models() -> list[str]:
   # return [model["name"] for model in ollama.list()["models"]]
   return [MODEL_NAME]


def generate_summary(model: str, prompt: str, temperature: float) -> str:
    llm_result = [{"role": "user", "content": prompt}]
    summary_generator = fetch_ollama_replies(model, llm_result, temperature)
    return "".join([response for response in summary_generator])

