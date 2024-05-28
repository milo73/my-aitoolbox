# My AI Toolbox

This is a simple web application that allows users to do multiple things which I think are useful to me. Now it only contains a couple of tools like simpel chat, transciption and summization of audio file like meetings and a tool to get a summary of a webpage. The application is built using Streamlit and leverages OpenAI's Whisper to perform transcriptions.

## How to Use

* **Upload Audio**: Click on the button and select (or drag and drop) an audio file in WAV, MP3, or M4A format that you want to transcribe.
  ![alt text](https://github.com/fizamusthafa/whisper-app/blob/master/overview.png "Drag or Upload")
* **Transcribe Audio**: Once the audio file is uploaded, click on the "Transcribe Audio" button in the sidebar. The application will start transcribing the audio using the Whisper model.
* **Supported Languages**: The Whisper model supports multiple languages. The application will automatically detect the language of the uploaded audio and provide accurate transcriptions for a wide range of languages. This includes *Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.*
* **Clean-up**: After the transcription is complete, the temporary audio file will be removed to ensure your data privacy.

## Requirements

To run this application locally, you need to have Python installed along with the following packages:

* Streamlit
* Whisper
* Ollama
* Requests
* Newspaper3k

You can install the required packages using the following commands:
```
pip install streamlit
pip install whisper
pip install ollama
pip install requests
pip install newspaper3k
```

## How to Run

* Clone this repository to your local machine.
* Open a terminal or command prompt and navigate to the repository's directory.
* Run the Streamlit application: `streamlit run main.py`
* The application will open in your web browser, and you can start using the tools right away.

## Applications

### Whisper App
* Transcribe and summarize audio files using the Whisper model.

### Ollama Chat App
* Chat with different models using the Ollama API.

### Web Summary App
* Summarize web content by providing a URL.

## Tabs
The application includes the following tabs:
* **Ollama Chat**: Interact with the Ollama chat model.
* **Whisper App**: Transcribe and summarize audio files.
* **Web Summary**: Summarize content from a given URL.
