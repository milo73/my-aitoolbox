import streamlit as st
import ollama_utils
import requests
import newspaper
from typing import Dict, Iterable

def create_web_summary_app():
    """
    This function builds the Streamlit UI and functionalities for the Ollama chat app,
    fetches content from a given URL, sends it to the Ollama model for summarization,
    and returns the summary.
    """
    st.title("Website Summarization with Ollama")
    st.subheader("This tool will summarize the content of a webpage")
    url = st.text_input("Enter the URL of the webpage to summarize")
    if url:
        try:
            web_content = fetch_web_content(url)
            models = ollama_utils.get_models()
            if models:
                model = models[0]  # Assuming the first model is suitable for summarization
                chat_history = [{"role": "user", "content": f"Your task is to summarise the content of the page, which is a news article. Only extract the relevant context. Ignore the CSS and other HTML code. Also try to ignore the JavaScript code. Ignore the privacy policy. Summarize this content: {web_content}"}]
                summary_generator = ollama_utils.fetch_ollama_replies(model, chat_history)
                summary = " ".join([response for response in summary_generator])
                st.write("Summary:")
                st.write(summary)
            else:
                st.error("No models available for summarization.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the webpage: {e}")
    else:
        st.info("Please enter a URL to summarize.")

def fetch_web_content(url: str) -> str:
    #response = requests.get(url)
    #response.raise_for_status()  # Raises an HTTPError for bad responses
    #return response.text
    article = newspaper.Article(url=url, language='en')
    article.download()
    article.parse()

    article ={
        "title": str(article.title),
        "text": str(article.text),
        "authors": article.authors,
        "published_date": str(article.publish_date),
        "top_image": str(article.top_image),
        "videos": article.movies,
        "keywords": article.keywords,
        "content": str(article.text)
    }
    return article