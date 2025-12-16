"""
Whisper audio transcription and summarization application.
"""
import streamlit as st
import whisper
import tempfile
import os
import ollama_utils
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def create_whisper_app(whisper_model: str, model_name: str, temperature: float) -> None:
    """
    Build the Streamlit UI and functionalities for the Whisper audio summarization app.

    Args:
        whisper_model: Name of the Whisper model to use (e.g., 'base', 'small', 'medium')
        model_name: Name of the Ollama model for summarization
        temperature: Temperature parameter for summary generation (0.0-1.0)
    """
    st.markdown("### 🎙️ Audio Transcription & Summarization")
    st.caption("Upload audio files in any language for automatic transcription and intelligent summarization")

    # Instructions
    with st.expander("📖 How to use", expanded=False):
        st.markdown("""
        1. **Upload** your audio file (WAV, MP3, or M4A format)
        2. **Customize** the system prompt (optional)
        3. **Click** "Transcribe & Summarize" button
        4. **Wait** for processing (this may take a few minutes depending on file size)
        5. **Review** the transcription and AI-generated summary

        **Supported Languages:** 90+ languages including English, Spanish, French, German, Chinese, Japanese, and more!
        """)

    st.markdown("---")

    # Two-column layout for settings
    col1, col2 = st.columns([2, 1])

    with col1:
        system_prompt = st.text_area(
            "🎯 System Prompt",
            value="You are a professional writer and reliable, professional minute-maker. Create accurate minutes of the following transcription: ",
            height=120,
            help="Customize how the AI should summarize your audio content"
        )

    with col2:
        st.markdown("**⚙️ Current Settings**")
        st.info(f"**Whisper Model:** {whisper_model}\n\n**LLM Model:** {model_name}\n\n**Temperature:** {temperature}")

    # File uploader with better styling
    audio_file = st.file_uploader(
        "📁 Upload Audio File",
        type=["wav", "mp3", "m4a"],
        help="Maximum file size: 200MB"
    )

    if audio_file:
        st.success(f"✅ File loaded: **{audio_file.name}** ({audio_file.size / 1024 / 1024:.2f} MB)")

    # Process button
    if st.button("🚀 Transcribe & Summarize", type="primary", use_container_width=True):
        if audio_file is None:
            st.error("⚠️ Please upload an audio file first!")
            return

        try:
            with st.status("🔄 Processing audio...", expanded=True) as status:
                st.write("📥 Loading Whisper model...")
                loaded_model = whisper.load_model(whisper_model)

                st.write("🎵 Transcribing audio...")
                transcription, language = process_audio(audio_file, loaded_model)

                status.update(label="✅ Transcription complete!", state="complete", expanded=False)

            # Results in tabs - OUTSIDE the status block so they persist
            result_tab1, result_tab2, result_tab3 = st.tabs(["📝 Summary", "📄 Transcription", "ℹ️ Details"])

            with result_tab1:
                st.markdown("### 📝 AI Summary")
                with st.spinner("🤖 Generating summary with AI..."):
                    summary = summarize_text(model_name, system_prompt, transcription, temperature)
                st.markdown(summary)
                st.download_button(
                    "💾 Download Summary",
                    summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

            with result_tab2:
                st.markdown("### 📄 Full Transcription")
                st.markdown(transcription)
                st.download_button(
                    "💾 Download Transcription",
                    transcription,
                    file_name="transcription.txt",
                    mime="text/plain"
                )

            with result_tab3:
                st.markdown("### ℹ️ Metadata")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🌍 Language", language.upper())
                with col2:
                    st.metric("📊 Model", whisper_model)
                with col3:
                    st.metric("📏 Length", f"{len(transcription.split())} words")

        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            st.error(f"❌ **Processing Error**")
            st.error(f"Details: {str(e)}")
            st.info("💡 **Troubleshooting:**\n- Ensure the audio file is valid\n- Check if Whisper is properly installed\n- Try a smaller file or different format\n- Ensure FFmpeg is installed")

def process_audio(audio_file, whisper_model) -> Tuple[str, str]:
    """
    Process audio file and extract transcription and language.

    Args:
        audio_file: Uploaded audio file from Streamlit
        whisper_model: Loaded Whisper model

    Returns:
        Tuple of (transcription text, detected language)

    Raises:
        Exception: If audio processing fails
    """
    audio_path = None
    try:
        # Get file extension from uploaded file
        file_ext = audio_file.name.rsplit('.', 1)[-1] if '.' in audio_file.name else 'tmp'
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp_audio:
            temp_audio.write(audio_file.read())
            audio_path = temp_audio.name

        # Use transcribe directly - handles language detection internally
        # This is more compatible with different Whisper versions
        transcription = whisper_model.transcribe(audio_path, task='translate', fp16=False)
        detected_lang = transcription.get("language", "unknown")

        return transcription["text"], detected_lang
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise
    finally:
        # Clean up temporary file
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except Exception as e:
                logger.warning(f"Could not remove temporary file {audio_path}: {e}")


def summarize_text(model_name: str, system_prompt: str, transcription: str, temperature: float) -> str:
    """
    Generate a summary of transcribed text.

    Args:
        model_name: Name of the Ollama model to use
        system_prompt: System prompt to guide summarization
        transcription: The transcribed text to summarize
        temperature: Temperature parameter for summary generation (0.0-1.0)

    Returns:
        Generated summary as a string

    Raises:
        Exception: If summarization fails
    """
    prompt = system_prompt + transcription
    return ollama_utils.generate_summary(model_name, prompt, temperature)

if __name__ == "__main__":
    st.set_page_config(page_title="Audio Summarization App", page_icon="🎙️")
    create_whisper_app("base", "llama2", 0.7)