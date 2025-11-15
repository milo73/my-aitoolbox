"""
Web content summarization application.
"""
import streamlit as st
import ollama_utils
import requests
from newspaper import Article, ArticleException
from typing import Dict, Optional
import logging
from url_validator import is_safe_url

logger = logging.getLogger(__name__)


def create_web_summary_app(model: str, temperature: float) -> None:
    """
    Build the Streamlit UI and functionalities for web content summarization.

    Args:
        model: Name of the Ollama model to use
        temperature: Temperature parameter for summary generation (0.0-1.0)
    """
    st.markdown("### 🌐 Website Content Summarizer")
    st.caption("Extract and summarize content from any public webpage using AI")

    # Instructions
    with st.expander("📖 How to use", expanded=False):
        st.markdown("""
        1. **Enter** a valid HTTP or HTTPS URL
        2. **Click** "Summarize" or press Enter
        3. **Wait** for the AI to extract and analyze the content
        4. **Review** the generated summary and article details

        **Best for:** News articles, blog posts, research papers, documentation

        **Security:** Only public URLs are allowed. Private/internal IPs are blocked for security.
        """)

    st.markdown("---")

    # URL input with better UI
    col1, col2 = st.columns([4, 1])
    with col1:
        url = st.text_input(
            "🔗 Enter Website URL",
            placeholder="https://example.com/article",
            help="Enter a valid public HTTP or HTTPS URL"
        )
    with col2:
        st.markdown("**📊 Settings**")
        st.caption(f"Model: {model}")
        st.caption(f"Temp: {temperature}")

    # Example URLs
    with st.expander("💡 Try these example URLs"):
        example_urls = [
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://techcrunch.com/",
            "https://www.bbc.com/news"
        ]
        for example in example_urls:
            if st.button(example, key=example):
                url = example
                st.rerun()

    if url:
        # Validate URL for security
        is_valid, error_message = is_safe_url(url)
        if not is_valid:
            st.error(f"❌ **Invalid URL**")
            st.error(f"Reason: {error_message}")
            st.info("💡 Please enter a valid public HTTP or HTTPS URL. Private/internal URLs are blocked for security.")
            return

        # Process button
        if st.button("🚀 Summarize Website", type="primary", use_container_width=True):
            with st.spinner("🔄 Fetching and analyzing content..."):
                try:
                    # Fetch content
                    st.info("📥 Downloading webpage content...")
                    web_content = fetch_web_content(url)

                    if web_content:
                        # Generate summary
                        st.info("🤖 Generating AI summary...")
                        system_prompt = (
                            "Your task is to summarize the content of the page, which is a news article. "
                            "Only extract the relevant context. Ignore the CSS and other HTML code. "
                            "Also try to ignore the JavaScript code. Ignore the privacy policy. "
                            "Provide the summary in markdown format. Summarize this content: "
                        )
                        prompt = system_prompt + str(web_content)

                        summary = ollama_utils.generate_summary(model, prompt, temperature)

                        st.success("✅ Summary generated successfully!")

                        # Display results in tabs
                        tab1, tab2 = st.tabs(["📝 Summary", "ℹ️ Article Info"])

                        with tab1:
                            st.markdown("### 📝 AI-Generated Summary")
                            st.markdown(summary)

                            # Download button
                            st.download_button(
                                "💾 Download Summary",
                                summary,
                                file_name="web_summary.txt",
                                mime="text/plain"
                            )

                        with tab2:
                            st.markdown("### ℹ️ Article Metadata")

                            if web_content.get("title"):
                                st.markdown(f"**📰 Title:** {web_content['title']}")

                            if web_content.get("authors"):
                                st.markdown(f"**✍️ Authors:** {', '.join(web_content['authors'])}")

                            if web_content.get("published_date"):
                                st.markdown(f"**📅 Published:** {web_content['published_date']}")

                            if web_content.get("keywords"):
                                st.markdown(f"**🏷️ Keywords:** {', '.join(web_content['keywords'][:10])}")

                            if web_content.get("top_image"):
                                st.markdown(f"**🖼️ Featured Image:** [View]({web_content['top_image']})")

                            # Content stats
                            st.markdown("---")
                            st.markdown("**📊 Content Statistics**")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Word Count", len(web_content.get("text", "").split()))
                            with col2:
                                st.metric("Characters", len(web_content.get("text", "")))
                            with col3:
                                st.metric("Keywords", len(web_content.get("keywords", [])))

                    else:
                        st.warning("⚠️ No content could be extracted from the provided URL.")
                        st.info("The webpage might be JavaScript-heavy, paywalled, or have anti-scraping measures.")

                except requests.exceptions.RequestException as e:
                    logger.error(f"Error fetching webpage {url}: {e}")
                    st.error(f"❌ **Network Error**")
                    st.error(f"Failed to fetch the webpage: {str(e)}")
                    st.info("💡 **Troubleshooting:**\n- Check if the URL is accessible\n- Verify your internet connection\n- The website might be blocking automated requests")
                except Exception as e:
                    logger.error(f"Unexpected error processing {url}: {e}")
                    st.error(f"❌ **Processing Error**")
                    st.error(f"Details: {str(e)}")
                    st.info("💡 Try a different URL or check if the content is accessible")
    else:
        # Empty state with helpful message
        st.info("👆 Enter a URL above to get started")
        st.markdown("""
        **Popular use cases:**
        - 📰 Summarize news articles
        - 📚 Extract key points from research papers
        - 📝 Condense blog posts
        - 📖 Digest documentation pages
        """)


def fetch_web_content(url: str) -> Optional[Dict]:
    """
    Fetch and parse web content from a URL.

    Args:
        url: The URL to fetch content from

    Returns:
        Dictionary containing article information or None if parsing fails

    Raises:
        requests.exceptions.RequestException: If fetching the URL fails
        ArticleException: If parsing the article fails
    """
    try:
        article = Article(url=url, language='en')
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
    except ArticleException as e:
        logger.error(f"Error parsing article from {url}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching content from {url}: {e}")
        raise