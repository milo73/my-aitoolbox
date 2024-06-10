import streamlit as st
import ollama_utils

def create_ollama_chat_app():
  """
  This function builds the Streamlit UI and functionalities for the Ollama chat app.
  """

  st.session_state.selected_model = ollama_utils.get_models()[0]
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
          response = st.write_stream(ollama_utils.fetch_ollama_replies(
              st.session_state.selected_model, st.session_state.messages))
            
      st.session_state.messages.append(
          {"role": "assistant", "content": response})