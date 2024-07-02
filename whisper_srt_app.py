import streamlit as st
import whisper
import tempfile
import os
from datetime import timedelta

def create_whisper_srt_app(whisper_model: str, model_name: str, temperature: float):
    """
    This function builds the Streamlit UI and functionalities for creating subtitles from video files using the Whisper model.
    """
    st.title("Create video Subtitle with Whisper")
    
    # Upload video file
    video_file_path = st.file_uploader("Upload your video", type=["mp4", "mov"])
    whisper_model = whisper.load_model(whisper_model)
    
    if st.button("Transcribe Video"):
        if video_file_path is not None:
            with st.status("Start transcribing...", expanded=True) as status:
                # Temporary storage for video file
                with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                    temp_audio.write(video_file_path.read())
                
                # Absolute path for the temporary audio file
                video_file_path_path = os.path.abspath(temp_audio.name)
                
                # Load and process audio from video
                audio = whisper.load_audio(video_file_path_path)
                audio = whisper.pad_or_trim(audio)
                
                # Generate Mel spectrogram
                mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
                
                # Language detection
                _, probs = whisper_model.detect_language(mel)
                st.write(f"Detected language: {max(probs, key=probs.get)}")
                
                # Transcription process
                st.write("Transcribing...")
                options = whisper.DecodingOptions(fp16=False)
                result = whisper.decode(whisper_model, mel, options)
                st.markdown(result.text)
                st.divider()
                
                # Generate transcription segments
                transcription = whisper_model.transcribe(video_file_path_path, fp16=False)
                segments = transcription['segments']
                segment_srt = ""
                
                # Create SRT format from segments
                for segment in segments:
                    startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
                    endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
                    text = segment['text']
                    segmentId = segment['id']+1
                    segment_srt += f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
                
                # Display and allow download of SRT file
                st.markdown(f"Generated SRT text: {segment_srt}")
                st.download_button(label="Download SRT file", data=segment_srt, file_name="video_subtitles.srt", mime="text/plain")
                
                # Clean up the temporary file after processing
                os.remove(video_file_path_path)
        else:
            st.error("Please upload a video file.")