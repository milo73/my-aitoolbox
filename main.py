import streamlit as st

# Import functions from individual apps
from ollama_chat_app import create_ollama_chat_app
from whisper_app import create_whisper_app
#from web_summary_app import create_web_summary_app

# Create tabs for each app
tab1, tab2 = st.tabs(["Ollama Chat", "Whisper App"])
#tab1, tab2, tab3 = st.tabs(["Ollama Chat", "Whisper App", "Website Summary"])

with tab1:
  create_ollama_chat_app()  # Initializes the Ollama Chat app within the first tab

with tab2:
  create_whisper_app()  # Initializes the Whisper app within the second tab

# with tab3:
#   create_web_summary_app()  # The code for initializing a Website Summary app is commented out
