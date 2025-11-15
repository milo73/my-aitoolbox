"""
Centralized configuration module for AI Toolbox application.
Loads and validates environment variables.
"""
import os
from dotenv import load_dotenv
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class."""

    # Model configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3")
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")

    # API configuration (currently not used but kept for future use)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_URL: str = os.getenv("OPENAI_URL", "http://localhost:11434/v1")

    # Application settings
    MAX_UPLOAD_SIZE_MB: int = 500
    SUPPORTED_AUDIO_FORMATS: List[str] = ["wav", "mp3", "m4a"]
    SUPPORTED_VIDEO_FORMATS: List[str] = ["mp4", "mov"]
    WHISPER_MODEL_OPTIONS: List[str] = ["tiny", "base", "small", "medium", "large"]

    # Validate critical configuration
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.MODEL_NAME:
            logger.warning("MODEL_NAME not set, using default: llama3")
        if not cls.WHISPER_MODEL:
            logger.warning("WHISPER_MODEL not set, using default: base")
        elif cls.WHISPER_MODEL not in cls.WHISPER_MODEL_OPTIONS:
            logger.warning(f"Invalid WHISPER_MODEL '{cls.WHISPER_MODEL}', using default: base")
            cls.WHISPER_MODEL = "base"
        return True

    @classmethod
    def get_info(cls) -> dict:
        """Get configuration information as a dictionary."""
        return {
            "model_name": cls.MODEL_NAME,
            "whisper_model": cls.WHISPER_MODEL,
            "max_upload_size_mb": cls.MAX_UPLOAD_SIZE_MB,
            "supported_audio_formats": cls.SUPPORTED_AUDIO_FORMATS,
            "supported_video_formats": cls.SUPPORTED_VIDEO_FORMATS,
        }


# Validate configuration on import
Config.validate()
logger.info("Configuration loaded successfully")
