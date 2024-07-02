import streamlit as st
import whisper
import tempfile
import os
import ollama_utils
from langchain_community.llms import Ollama

def create_whisper_app(whisper_model: str, model_name: str, temperature: float):
    """
    Builds the Streamlit UI and functionalities for the Whisper audio summarization app.
    """
    st.title("Multi-lingual Audio Summarization with Whisper and Ollama")

    system_prompt = st.text_area(
        "System Prompt",
        "You are a professional writer and reliable, professional minute-maker. Create accurate minutes of the following transcription: "
    )
    audio_file = st.file_uploader("Upload your audio", type=["wav", "mp3", "m4a"])
    
    if st.button("Transcribe Audio"):
        if audio_file is None:
            st.error("Please upload an audio file.")
            return

        with st.status("Processing audio...", expanded=True) as status:
            try:
                whisper_model = whisper.load_model(whisper_model)
                transcription, language = process_audio(audio_file, whisper_model)
                
                status.update(label="Transcription complete!", state="complete", expanded=False)
                
                st.subheader("Detected Language")
                st.write(language)
                
                st.subheader("Transcription")
                st.markdown(transcription)
                
                summary = summarize_text(model_name, system_prompt, transcription, temperature)
                
                st.subheader("Summary")
                st.markdown(summary)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def process_audio(audio_file, whisper_model):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_audio:
        temp_audio.write(audio_file.read())
        audio_path = temp_audio.name

    try:
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

        _, probs = whisper_model.detect_language(mel)
        detected_lang = max(probs, key=probs.get)

        transcription = whisper_model.transcribe(audio_path, task='translate', fp16=False)
        return transcription["text"], detected_lang
    finally:
        os.remove(audio_path)

def summarize_text(model_name: str, system_prompt: str, transcription: str, temperature: float) -> str:
    prompt = system_prompt + transcription
    return ollama_utils.generate_summary(model_name, prompt, temperature)

if __name__ == "__main__":
    st.set_page_config(page_title="Audio Summarization App", page_icon="🎙️")
    create_whisper_app("base", "llama2", 0.7)