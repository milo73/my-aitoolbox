import streamlit as st
import whisper
import tempfile
import os
from langchain_community.llms import Ollama
llm = Ollama(model="llama3")


def create_whisper_app():
  """
  This function builds the Streamlit UI and functionalities for the Whisper audio summarization app.
  """

  st.title("Multi-lingual Audio Summarization with Whisper and Ollama")

  # Text prompt to guide the summarization process
  system_prompt = st.text_input("System Prompt", "You are a professional writer and reliable, professional minute-maker. Create accurate minutes of the following transcription: ")

  audio_file = st.file_uploader("Upload your audio", type=["wav", "mp3", "m4a"])
  model = whisper.load_model("base")

  if st.button("Transcribe Audio"):
    if audio_file is not None:
      with st.status("Start transcribing...",expanded=True) as status:
        # Detect language
        st.write("Start detecting language")
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
          temp_audio.write(audio_file.read())

        # Get the absolute path of the temporary audio file
        audio_file_path = os.path.abspath(temp_audio.name)
        print(f"Temporary file path: {audio_file_path}")

        # Load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)

        # Make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Detect the spoken language
        _, probs = model.detect_language(mel)
        st.write(f"Detected language: {max(probs, key=probs.get)}")

        # Start transcribing
        st.write("Transcribing...")

        # Decode the audio
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)

        # Print the recognized text
        st.markdown(result.text)
        st.divider()

        transcription = model.transcribe(audio_file_path, task='translate', fp16=False)
        status.update(label="Transcription complete!", state="complete", expanded=False)

        # Print the transcribed text
        st.markdown(transcription["text"])
        st.divider()

        # Summarization with Ollama (assuming Ollama is implemented elsewhere)
        st.success("Summarizing...")
        prompt = system_prompt + transcription["text"]

        try:
          summary = llm.invoke(prompt)  # Assuming llm is defined elsewhere (e.g., imported from main.py)
        except Exception as e:
          st.error(f"Error during summarization: {e}")
          summary = "An error occurred while summarizing the transcript."

        # Print the summary
        st.success("Summary complete")
        st.markdown(summary)

        # Clean up the temporary file after processing
        os.remove(audio_file_path)
    else:
      st.error("Please upload an audio file.")


# Call the function within your main app (main.py)
# create_whisper_app()
