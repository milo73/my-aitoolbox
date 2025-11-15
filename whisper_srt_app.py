"""
Video subtitle creation using Whisper transcription.
"""
import streamlit as st
import whisper
import tempfile
import os
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@st.cache_resource
def load_whisper_model(model_name: str):
    """
    Load and cache Whisper model to avoid reloading on every interaction.

    Args:
        model_name: Name of the Whisper model to load

    Returns:
        Loaded Whisper model
    """
    return whisper.load_model(model_name)


def format_timestamp(seconds: int) -> str:
    """
    Format timestamp for SRT format.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted timestamp string (HH:MM:SS,mmm)
    """
    return str(0) + str(timedelta(seconds=int(seconds))) + ',000'


def create_whisper_srt_app(whisper_model_name: str, model_name: str, temperature: float) -> None:
    """
    Build the Streamlit UI and functionalities for creating subtitles from video files.

    Args:
        whisper_model_name: Name of the Whisper model to use
        model_name: Name of the Ollama model (not used in this app but kept for consistency)
        temperature: Temperature parameter (not used in this app but kept for consistency)
    """
    st.markdown("### 📝 Video Subtitle Generator")
    st.caption("Automatically generate SRT subtitle files from your video content using AI")

    # Instructions
    with st.expander("📖 How to use", expanded=False):
        st.markdown("""
        1. **Upload** your video file (MP4 or MOV format)
        2. **Click** "Generate Subtitles" button
        3. **Wait** for transcription (this may take several minutes for long videos)
        4. **Preview** the generated subtitles
        5. **Download** the SRT file to use with your video player or editing software

        **Supported Formats:** MP4, MOV

        **Tip:** SRT files can be used in video players like VLC, or video editing software like Premiere Pro, Final Cut Pro, or DaVinci Resolve.
        """)

    st.markdown("---")

    # Settings display
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**📹 Upload Video**")
        # Upload video file
        video_file = st.file_uploader(
            "Choose a video file",
            type=["mp4", "mov"],
            help="Maximum recommended file size: 500MB"
        )
    with col2:
        st.markdown("**⚙️ Settings**")
        st.info(f"**Whisper Model:**\n{whisper_model_name}\n\n**Multi-language:**\nAuto-detect")

    if video_file:
        # Show video info
        st.success(f"✅ Video loaded: **{video_file.name}** ({video_file.size / 1024 / 1024:.2f} MB)")

        # Show estimated processing time
        estimated_time = (video_file.size / 1024 / 1024) * 0.5  # Rough estimate: 0.5 min per MB
        st.info(f"⏱️ Estimated processing time: ~{estimated_time:.1f} minutes")

    # Process button
    if st.button("🎬 Generate Subtitles", type="primary", use_container_width=True, disabled=video_file is None):
        if video_file is None:
            st.error("Please upload a video file.")
            return

        video_file_abs_path = None
        try:
            with st.status("🔄 Processing video...", expanded=True) as status:
                # Load the model (cached)
                st.write("📥 Loading Whisper model...")
                loaded_model = load_whisper_model(whisper_model_name)

                # Temporary storage for video file
                st.write("💾 Saving video file...")
                with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_video:
                    temp_video.write(video_file.read())
                    video_file_abs_path = os.path.abspath(temp_video.name)

                # Load and process audio from video
                st.write("🎵 Extracting audio from video...")
                audio = whisper.load_audio(video_file_abs_path)
                audio = whisper.pad_or_trim(audio)

                # Generate Mel spectrogram
                mel = whisper.log_mel_spectrogram(audio).to(loaded_model.device)

                # Language detection
                _, probs = loaded_model.detect_language(mel)
                detected_language = max(probs, key=probs.get)
                st.write(f"🌍 Detected language: **{detected_language.upper()}**")

                # Transcription process
                st.write("✍️ Transcribing video content...")

                # Generate transcription segments
                transcription = loaded_model.transcribe(video_file_abs_path, fp16=False)
                segments = transcription['segments']
                segment_srt = ""

                # Create SRT format from segments
                for segment in segments:
                    start_time = format_timestamp(segment['start'])
                    end_time = format_timestamp(segment['end'])
                    text = segment['text']
                    segment_id = segment['id'] + 1
                    # Strip leading space if present
                    text = text[1:] if text and text[0] == ' ' else text
                    segment_srt += f"{segment_id}\n{start_time} --> {end_time}\n{text}\n\n"

                status.update(label="✅ Subtitles generated successfully!", state="complete", expanded=False)

                # Display results in tabs
                st.success(f"🎉 Successfully generated {len(segments)} subtitle segments!")

                tab1, tab2, tab3 = st.tabs(["📝 Preview", "💾 Download", "📊 Statistics"])

                with tab1:
                    st.markdown("### 📝 Subtitle Preview")
                    st.text_area(
                        "SRT Content",
                        segment_srt,
                        height=400,
                        help="This is the standard SRT format that can be used in video players and editors"
                    )

                with tab2:
                    st.markdown("### 💾 Download Subtitles")
                    st.download_button(
                        label="📥 Download SRT File",
                        data=segment_srt,
                        file_name=f"{video_file.name.rsplit('.', 1)[0]}_subtitles.srt",
                        mime="text/plain",
                        use_container_width=True,
                        type="primary"
                    )
                    st.info("💡 **Tip:** Import this SRT file into your video editor or player to display subtitles synchronized with your video.")

                    st.markdown("---")
                    st.markdown("**🎬 How to use SRT files:**")
                    st.markdown("""
                    - **VLC Player:** Right-click video → Subtitle → Add Subtitle File
                    - **YouTube:** Upload video → Subtitles → Upload file
                    - **Premiere Pro:** Import SRT file and sync with video timeline
                    """)

                with tab3:
                    st.markdown("### 📊 Transcription Statistics")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("🌍 Language", detected_language.upper())
                    with col2:
                        st.metric("📝 Segments", len(segments))
                    with col3:
                        total_words = sum(len(seg['text'].split()) for seg in segments)
                        st.metric("📖 Words", total_words)
                    with col4:
                        duration = segments[-1]['end'] if segments else 0
                        st.metric("⏱️ Duration", f"{int(duration // 60)}:{int(duration % 60):02d}")

        except Exception as e:
            logger.error(f"Error transcribing video: {e}")
            st.error(f"❌ **Processing Error**")
            st.error(f"Details: {str(e)}")
            st.info("💡 **Troubleshooting:**\n- Ensure the video file is valid\n- Check if Whisper is properly installed\n- Try a smaller file\n- Ensure FFmpeg is installed for video processing")

        finally:
            # Clean up the temporary file after processing
            if video_file_abs_path and os.path.exists(video_file_abs_path):
                try:
                    os.remove(video_file_abs_path)
                except Exception as e:
                    logger.warning(f"Could not remove temporary file {video_file_abs_path}: {e}")
    else:
        # Empty state
        st.info("👆 Upload a video file above to get started")
        st.markdown("""
        **What you'll get:**
        - 📝 Industry-standard SRT subtitle file
        - 🌍 Automatic language detection
        - ⏱️ Precise timing for each subtitle
        - 💾 Ready to use with any video player or editor
        """)