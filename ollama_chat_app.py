import streamlit as st
import ollama_utils
import logging

logger = logging.getLogger(__name__)


def create_ollama_chat_app(model: str, temperature: float) -> None:
    """
    Build the Streamlit UI and functionalities for the Ollama chat app.

    Args:
        model: The name of the Ollama model to use
        temperature: Temperature parameter for model responses (0.0-1.0)
    """
    st.session_state.selected_model = model

    # Header with model info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 💬 Chat with **{st.session_state.selected_model}**")
        st.caption(f"Temperature: {temperature} • Model responds with {'high creativity' if temperature > 0.7 else 'balanced responses' if temperature > 0.3 else 'focused precision'}")
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Chat cleared! How can I help you?"}]
            st.rerun()

    st.markdown("---")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "👋 Hello! I'm ready to help. Ask me anything!"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = st.write_stream(ollama_utils.fetch_ollama_replies(
                    st.session_state.selected_model, st.session_state.messages, temperature))
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                logger.error(f"Error fetching Ollama response: {e}")
                st.error(f"⚠️ **Connection Error**")
                st.error(f"Failed to get response from model: {str(e)}")
                st.info("💡 **Troubleshooting:**\n- Ensure Ollama is running: `ollama serve`\n- Check if model exists: `ollama list`\n- Pull the model if needed: `ollama pull " + model + "`")