"""
Utilities for interacting with Ollama API.
"""
import ollama
from typing import Dict, Iterable, List
import logging
from config import Config

logger = logging.getLogger(__name__)


def fetch_ollama_replies(model: str, chat_history: List[Dict], temperature: float) -> Iterable[str]:
    """
    Fetch streaming responses from Ollama API.

    Args:
        model: The name of the Ollama model to use
        chat_history: List of message dictionaries with 'role' and 'content'
        temperature: Temperature parameter for response generation (0.0-1.0)

    Yields:
        String chunks of the model's response

    Raises:
        Exception: If Ollama API request fails
    """
    try:
        responses = ollama.chat(
            model=model,
            messages=chat_history,
            stream=True,
            options={"temperature": temperature}
        )
        for response in responses:
            yield response['message']['content']
    except Exception as e:
        logger.error(f"Error fetching Ollama replies: {e}")
        raise


def get_models() -> List[str]:
    """
    Get list of available Ollama models.

    Returns:
        List of model names
    """
    try:
        response = ollama.list()
        # Handle both old dict-style and new Pydantic-style responses
        if hasattr(response, 'models'):
            # New Pydantic model (ollama >= 0.4)
            return [m.model if hasattr(m, 'model') else m.name for m in response.models]
        else:
            # Old dict-style response
            return [model["name"] for model in response["models"]]
    except Exception as e:
        logger.warning(f"Could not fetch Ollama models: {e}. Using default.")
        return [Config.MODEL_NAME]


def generate_summary(model: str, prompt: str, temperature: float) -> str:
    """
    Generate a summary using the Ollama model.

    Args:
        model: The name of the Ollama model to use
        prompt: The prompt to send to the model
        temperature: Temperature parameter for response generation (0.0-1.0)

    Returns:
        The generated summary as a string

    Raises:
        Exception: If summary generation fails
    """
    try:
        llm_result = [{"role": "user", "content": prompt}]
        summary_generator = fetch_ollama_replies(model, llm_result, temperature)
        return "".join([response for response in summary_generator])
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise

