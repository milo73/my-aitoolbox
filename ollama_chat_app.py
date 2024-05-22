import streamlit as st
import ollama
from typing import Dict, Iterable

def create_ollama_chat_app():
  """
  This function builds the Streamlit UI and functionalities for the Ollama chat app.
  """

  def fetch_ollama_replies(model: str, chat_history: Dict) -> Iterable:
      # Existing logic for fetching replies remains here
      responses = ollama.chat(model=model, messages=chat_history, stream=True)
      for response in responses:
          yield response['message']['content']

  def get_models() -> list[str]:
      # Existing logic for getting models remains here
      return [model["name"] for model in ollama.list()["models"]]

  with st.sidebar:
      st.session_state.selected_model = st.selectbox("Active model:", get_models())
      st.caption("streamlit + ollama chatbot boilerplate")

  st.title("Chat with " + st.session_state.selected_model)

  if "selected_model" not in st.session_state:
      st.session_state.selected_model = ""
  if "messages" not in st.session_state:
      st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  if prompt := st.chat_input():
      st.session_state.messages.append({"role": "user", "content": prompt})
        
      with st.chat_message("user"):
          st.markdown(prompt)
      with st.chat_message("assistant"):
          response = st.write_stream(fetch_ollama_replies(
              st.session_state.selected_model, st.session_state.messages))
            
      st.session_state.messages.append(
          {"role": "assistant", "content": response})

# Call the function within your main app (main.py)
# create_ollama_chat_app()
