"""
AI Toolbox - Main application entry point.

A versatile web application that offers a suite of AI-powered tools including
Ollama chat, audio transcription/summarization, web content summarization,
and subtitle creation.
"""
import streamlit as st
from config import Config

# Import functions from individual apps
from ollama_chat_app import create_ollama_chat_app
from whisper_app import create_whisper_app
from whisper_transcribe_app import create_whisper_transcribe_app
from web_summary_app import create_web_summary_app
from whisper_srt_app import create_whisper_srt_app
import ollama_utils

# Configure Streamlit page
st.set_page_config(
    page_title="AI Toolbox",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🤖 AI Toolbox</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powerful AI tools for chat, transcription, and content analysis</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Settings")

    st.markdown("---")

    # LLM Model Configuration
    with st.expander("🤖 LLM Model", expanded=True):
        # Fetch available models from Ollama
        available_models = ollama_utils.get_models()

        # Determine default index
        default_model = Config.MODEL_NAME
        if default_model in available_models:
            default_index = available_models.index(default_model)
        elif available_models:
            default_index = 0
        else:
            default_index = 0
            available_models = [default_model]  # Fallback if no models found

        model_name = st.selectbox(
            "Select Model",
            options=available_models,
            index=default_index,
            help="Select from available Ollama models"
        )
        temperature = st.slider(
            "Temperature",
            value=0.1,
            min_value=0.0,
            max_value=1.0,
            step=0.1,
            help="Higher values make output more random, lower values more deterministic"
        )
        st.session_state.selected_model = model_name

        # Refresh button for models
        if st.button("🔄 Refresh Models", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Whisper Model Configuration
    with st.expander("🎙️ Whisper Model", expanded=False):
        whisper_options = ["tiny", "base", "small", "medium", "large", "turbo"]
        whisper_default = Config.WHISPER_MODEL if Config.WHISPER_MODEL in whisper_options else "large"
        whisper_model = st.selectbox(
            "Model size",
            options=whisper_options,
            index=whisper_options.index(whisper_default),
            help="Larger models are more accurate but slower. Turbo is the fastest large model."
        )
        st.info("💡 **Model sizes:**\n- Tiny: Fastest, least accurate\n- Base: Good balance\n- Small: Better accuracy\n- Medium: High accuracy\n- Large: Best accuracy, slower\n- Turbo: Fast + accurate (large-v3)")

    st.markdown("---")

    # About section
    with st.expander("ℹ️ About", expanded=False):
        st.markdown("""
        **AI Toolbox** provides:
        - 💬 Chat with local LLMs via Ollama
        - 🎙️ Audio transcription & summarization
        - 🎧 Pure audio transcription (multi-format)
        - 🌐 Web content summarization
        - 📝 Video subtitle generation

        **Requirements:**
        - Ollama installed and running
        - Whisper models downloaded
        - FFmpeg for audio/video processing
        """)

    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit, Ollama & Whisper")

# Create tabs for each app
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Ollama Chat",
    "🎙️ Audio Summary",
    "🎧 Transcription",
    "🌐 Website Summary",
    "📝 Subtitles"
])

with tab1:
    create_ollama_chat_app(model_name, temperature)

with tab2:
    create_whisper_app(whisper_model, model_name, temperature)

with tab3:
    create_whisper_transcribe_app(whisper_model, model_name, temperature)

with tab4:
    create_web_summary_app(model_name, temperature)

with tab5:
    create_whisper_srt_app(whisper_model, model_name, temperature)
