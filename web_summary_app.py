import streamlit as st
import ollama_utils
import requests
import newspaper
from typing import Dict, Iterable

def create_web_summary_app(model: str, temperature: float):
    st.title("Website Summarization with Ollama")
    st.subheader("This tool will summarize the content of a webpage")
    url = st.text_input("Enter the URL of the webpage to summarize")
    if url:
        try:
            web_content = fetch_web_content(url)
            if web_content:
                system_prompt = "Your task is to summarise the content of the page, which is a news article. Only extract the relevant context. Ignore the CSS and other HTML code. Also try to ignore the JavaScript code. Ignore the privacy policy. Provide the summary in markdown format. Summarize this content: "
                prompt = system_prompt + str(web_content)
                summary = ollama_utils.generate_summary(model, prompt, temperature)
                st.markdown("Summary:")
                st.markdown(summary)
            else:
                st.warning("No content could be extracted from the provided URL.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching the webpage: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.info("Please enter a URL to summarize.")

def fetch_web_content(url: str) -> dict:
    try:
        article = newspaper.Article(url=url, language='en')
        article.download()
        article.parse()

        return {
            "title": str(article.title),
            "text": str(article.text),
            "authors": article.authors,
            "published_date": str(article.publish_date),
            "top_image": str(article.top_image),
            "videos": article.movies,
            "keywords": article.keywords,
            "content": str(article.text)
        }
    except newspaper.ArticleException as e:
        st.error(f"Error parsing the article: {e}")
        return None