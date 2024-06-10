import os
import streamlit as st
from dotenv import load_dotenv 

load_dotenv()

# Load model parameters
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL")
WHISPER_MODEL = os.getenv("WHISPER_MODEL")

# Import functions from individual apps
from ollama_chat_app import create_ollama_chat_app
from whisper_app import create_whisper_app
from web_summary_app import create_web_summary_app

with st.sidebar:
      st.header("LLM Model")
      model_name = st.text_input("Model name", value=MODEL_NAME)
      temperature = st.slider("Temperature", value=0.1, min_value=0.0, max_value=1.0)
      st.session_state.selected_model = model_name

      st.header("Whisper Model")
      model_name = st.text_input("Model name", value=WHISPER_MODEL)

# Create tabs for each app
#tab1, tab2 = st.tabs(["Ollama Chat", "Whisper App"])
tab1, tab2, tab3 = st.tabs(["Ollama Chat", "Whisper App", "Website Summary"])

with tab1:
  create_ollama_chat_app()  # Initializes the Ollama Chat app within the first tab

with tab2:
  create_whisper_app()  # Initializes the Whisper app within the second tab

with tab3:
  create_web_summary_app()  # The code for initializing a Website Summary app is commented out
