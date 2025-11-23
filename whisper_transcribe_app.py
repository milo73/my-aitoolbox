"""
Pure audio transcription using Whisper.
"""
import streamlit as st
import whisper
import tempfile
import os
import logging
import json
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)


@st.cache_resource
def load_whisper_model(model_name: str):
    """Load and cache Whisper model."""
    return whisper.load_model(model_name)


def format_timestamp_srt(seconds: float) -> str:
    """Format timestamp for SRT format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    """Format timestamp for VTT format (HH:MM:SS.mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def generate_plain_text(segments: List[Dict]) -> str:
    """Generate plain text transcription."""
    return "\n".join(seg['text'].strip() for seg in segments)


def generate_timestamped_text(segments: List[Dict]) -> str:
    """Generate timestamped text transcription."""
    lines = []
    for seg in segments:
        timestamp = format_timestamp_vtt(seg['start'])
        text = seg['text'].strip()
        lines.append(f"[{timestamp}] {text}")
    return "\n".join(lines)


def generate_srt(segments: List[Dict]) -> str:
    """Generate SRT subtitle format."""
    srt_content = ""
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_srt(seg['start'])
        end = format_timestamp_srt(seg['end'])
        text = seg['text'].strip()
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt_content


def generate_vtt(segments: List[Dict]) -> str:
    """Generate WebVTT subtitle format."""
    vtt_content = "WEBVTT\n\n"
    for i, seg in enumerate(segments, 1):
        start = format_timestamp_vtt(seg['start'])
        end = format_timestamp_vtt(seg['end'])
        text = seg['text'].strip()
        vtt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
    return vtt_content


def generate_json(segments: List[Dict], language: str) -> str:
    """Generate JSON format with full metadata."""
    data = {
        "language": language,
        "segments": [
            {
                "id": i,
                "start": seg['start'],
                "end": seg['end'],
                "text": seg['text'].strip()
            }
            for i, seg in enumerate(segments, 1)
        ]
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def create_whisper_transcribe_app(whisper_model_name: str, model_name: str, temperature: float) -> None:
    """
    Build the Streamlit UI for pure audio transcription.

    Args:
        whisper_model_name: Name of the Whisper model to use
        model_name: Name of the Ollama model (not used)
        temperature: Temperature parameter (not used)
    """
    st.markdown("### 🎧 Audio Transcription")
    st.caption("Convert speech to text with multiple export formats")

    # Instructions
    with st.expander("📖 How to use", expanded=False):
        st.markdown("""
        1. **Upload** your audio file (WAV, MP3, M4A, FLAC, OGG, or WEBM)
        2. **Select** transcription options (language, task)
        3. **Click** "Transcribe Audio"
        4. **Choose** your preferred download format
        5. **Download** the transcription

        **Available Formats:**
        - **Plain Text (.txt)** - Simple text without timestamps
        - **Timestamped Text (.txt)** - Text with timestamps for each segment
        - **SRT (.srt)** - Standard subtitle format for video players
        - **WebVTT (.vtt)** - Web-friendly subtitle format
        - **JSON (.json)** - Structured data with full metadata
        """)

    st.markdown("---")

    # Settings and upload
    col1, col2 = st.columns([3, 1])

    with col1:
        audio_file = st.file_uploader(
            "📁 Upload Audio File",
            type=["wav", "mp3", "m4a", "flac", "ogg", "webm"],
            help="Supported formats: WAV, MP3, M4A, FLAC, OGG, WEBM"
        )

    with col2:
        st.markdown("**⚙️ Options**")
        task = st.selectbox(
            "Task",
            options=["transcribe", "translate"],
            help="Transcribe keeps original language, Translate converts to English"
        )
        language = st.selectbox(
            "Language",
            options=["Auto-detect", "en", "es", "fr", "de", "it", "pt", "nl", "ru", "zh", "ja", "ko", "ar"],
            help="Select source language or auto-detect"
        )

    if audio_file:
        st.success(f"✅ Audio loaded: **{audio_file.name}** ({audio_file.size / 1024 / 1024:.2f} MB)")

    # Transcribe button
    if st.button("🎤 Transcribe Audio", type="primary", use_container_width=True, disabled=audio_file is None):
        if audio_file is None:
            st.error("Please upload an audio file.")
            return

        audio_path = None
        try:
            with st.status("🔄 Transcribing audio...", expanded=True) as status:
                # Load model
                st.write("📥 Loading Whisper model...")
                model = load_whisper_model(whisper_model_name)

                # Save temp file with proper extension for FFmpeg
                st.write("💾 Processing audio file...")
                file_ext = audio_file.name.rsplit('.', 1)[-1] if '.' in audio_file.name else 'wav'
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp_audio:
                    temp_audio.write(audio_file.read())
                    audio_path = temp_audio.name

                # Transcribe
                st.write("✍️ Transcribing...")
                lang = None if language == "Auto-detect" else language
                result = model.transcribe(
                    audio_path,
                    task=task,
                    language=lang,
                    fp16=False
                )

                detected_lang = result.get('language', 'unknown')
                segments = result['segments']

                status.update(label="✅ Transcription complete!", state="complete", expanded=False)

            # Store in session state for persistence
            st.session_state.transcription_result = {
                'segments': segments,
                'language': detected_lang,
                'filename': audio_file.name.rsplit('.', 1)[0]
            }

        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            st.error(f"❌ **Transcription Error**")
            st.error(f"Details: {str(e)}")
            st.info("💡 **Troubleshooting:**\n- Ensure the audio file is valid\n- Try a different format\n- Check if FFmpeg is installed")

        finally:
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception as e:
                    logger.warning(f"Could not remove temp file: {e}")

    # Display results if available
    if 'transcription_result' in st.session_state:
        result = st.session_state.transcription_result
        segments = result['segments']
        detected_lang = result['language']
        base_filename = result['filename']

        st.success(f"🎉 Transcription ready! Detected language: **{detected_lang.upper()}**")

        # Results tabs
        tab1, tab2, tab3 = st.tabs(["📝 Preview", "💾 Download", "📊 Statistics"])

        with tab1:
            st.markdown("### 📝 Transcription Preview")
            full_text = generate_plain_text(segments)
            st.text_area("Transcription", full_text, height=300)

        with tab2:
            st.markdown("### 💾 Download Options")
            st.markdown("Choose your preferred format:")

            # Generate all formats
            plain_text = generate_plain_text(segments)
            timestamped_text = generate_timestamped_text(segments)
            srt_text = generate_srt(segments)
            vtt_text = generate_vtt(segments)
            json_text = generate_json(segments, detected_lang)

            # Download buttons in columns
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📄 Text Formats**")
                st.download_button(
                    "📄 Plain Text (.txt)",
                    plain_text,
                    file_name=f"{base_filename}_transcription.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.caption("Simple text without timestamps")

                st.download_button(
                    "⏱️ Timestamped Text (.txt)",
                    timestamped_text,
                    file_name=f"{base_filename}_timestamped.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.caption("Text with timestamps for each segment")

                st.download_button(
                    "📊 JSON (.json)",
                    json_text,
                    file_name=f"{base_filename}_transcription.json",
                    mime="application/json",
                    use_container_width=True
                )
                st.caption("Structured data with full metadata")

            with col2:
                st.markdown("**🎬 Subtitle Formats**")
                st.download_button(
                    "🎬 SRT Subtitles (.srt)",
                    srt_text,
                    file_name=f"{base_filename}_subtitles.srt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.caption("Standard subtitle format for video players")

                st.download_button(
                    "🌐 WebVTT (.vtt)",
                    vtt_text,
                    file_name=f"{base_filename}_subtitles.vtt",
                    mime="text/vtt",
                    use_container_width=True
                )
                st.caption("Web-friendly subtitle format (HTML5 video)")

            # Format comparison
            with st.expander("📋 Format Comparison"):
                st.markdown("""
                | Format | Best For | Features |
                |--------|----------|----------|
                | **Plain Text** | Reading, editing, copying | Clean text only |
                | **Timestamped** | Reference, searching | Timestamps + text |
                | **SRT** | VLC, Premiere, YouTube | Industry standard |
                | **WebVTT** | Web browsers, HTML5 | Modern web format |
                | **JSON** | Developers, APIs | Full metadata, programmable |
                """)

        with tab3:
            st.markdown("### 📊 Transcription Statistics")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🌍 Language", detected_lang.upper())
            with col2:
                st.metric("📝 Segments", len(segments))
            with col3:
                word_count = sum(len(seg['text'].split()) for seg in segments)
                st.metric("📖 Words", word_count)
            with col4:
                duration = segments[-1]['end'] if segments else 0
                st.metric("⏱️ Duration", f"{int(duration // 60)}:{int(duration % 60):02d}")

            # Additional stats
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                char_count = sum(len(seg['text']) for seg in segments)
                st.metric("🔤 Characters", char_count)
            with col2:
                avg_segment = duration / len(segments) if segments else 0
                st.metric("⏳ Avg Segment", f"{avg_segment:.1f}s")

        # Clear results button
        if st.button("🗑️ Clear Results", use_container_width=True):
            del st.session_state.transcription_result
            st.rerun()

    else:
        # Empty state
        st.info("👆 Upload an audio file above to get started")
        st.markdown("""
        **What you'll get:**
        - 🎤 Accurate speech-to-text transcription
        - 🌍 Support for 90+ languages
        - 📄 Multiple download formats (TXT, SRT, VTT, JSON)
        - ⏱️ Precise timestamps for each segment
        """)
