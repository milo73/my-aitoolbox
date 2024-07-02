# AI Toolbox

AI Toolbox is a versatile web application that offers a suite of AI-powered tools for various tasks. Built with Streamlit, it leverages OpenAI's Whisper for audio processing and Ollama for language model interactions.

## Features

The application consists of four main tabs:

1. **Ollama Chat**: Engage in conversations with various language models via the Ollama API.
2. **Audio Summary**: Transcribe and summarize audio files in multiple languages using Whisper.
3. **Web Summary**: Generate concise summaries of web content from URLs.
4. **Subtitle Creation**: Transcribe video files and create SRT subtitle files from the transcriptions.

## Requirements

- Python 3.7+
- Streamlit
- Whisper
- Ollama
- Requests
- Newspaper3k
- FFmpeg (for audio processing)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-toolbox.git
   cd ai-toolbox
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - On Ubuntu or Debian: `sudo apt-get install ffmpeg`
   - On macOS with Homebrew: `brew install ffmpeg`
   - On Windows: Download from [FFmpeg official website](https://ffmpeg.org/download.html)

4. Set up Ollama:
   Follow the instructions on the [Ollama GitHub page](https://github.com/jmorganca/ollama) to install and set up Ollama on your system.

5. Configure environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   MODEL_NAME=your_default_model_name
   WHISPER_MODEL=base
   ```

## Usage

1. Start the application:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the provided local URL (usually http://localhost:8501).

3. Use the tabs at the top of the page to switch between different tools:

### Ollama Chat
- Select a language model from the sidebar.
- Type your message in the chat input and press Enter to send.
- View the model's responses in the chat history.

### Audio Summary
- Upload an audio file (WAV, MP3, or M4A format).
- Click "Transcribe Audio" to start the process.
- View the detected language, transcription, and summary.

### Web Summary
- Enter a URL in the text input field.
- Click the summarize button to generate a concise summary of the web content.

### Subtitle Creation
- Upload a video file (MP4 or MOV format).
- Click "Transcribe Video" to start the process.
- Once complete, you can download the generated SRT subtitle file.

## Supported Languages

The Whisper model supports a wide range of languages for audio transcription and summarization, including but not limited to:

Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

## Privacy and Security

- Temporary files (audio, video) are removed after processing to ensure data privacy.
- No user data is stored or retained by the application.
- All processing is done locally on your machine.

## Troubleshooting

- If you encounter issues with audio or video processing, ensure FFmpeg is correctly installed and accessible from the command line.
- For Ollama-related problems, check the Ollama documentation and ensure the service is running correctly on your system.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for the Whisper model
- Ollama team for their language model API
- Streamlit team for the wonderful web app framework