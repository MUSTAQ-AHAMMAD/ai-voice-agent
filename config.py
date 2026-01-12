"""
Configuration module for AI Voice Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the voice agent"""
    
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Agent Configuration
    AGENT_NAME = os.getenv('AGENT_NAME', 'Sales Assistant')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
    ENABLE_ARABIC = os.getenv('ENABLE_ARABIC', 'true').lower() == 'true'
    
    # Audio Settings
    SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', 16000))
    AUDIO_CHANNELS = int(os.getenv('AUDIO_CHANNELS', 1))
    
    # TTS Settings
    TTS_ENGINE = os.getenv('TTS_ENGINE', 'gtts')
    SPEECH_RATE = int(os.getenv('SPEECH_RATE', 150))
    
    # Database Paths
    QA_DATABASE_PATH = os.getenv('QA_DATABASE_PATH', './data/qa_database.json')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './data/vector_db')
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'ar': 'Arabic'
    }
    
    # Language codes for TTS
    TTS_LANGUAGE_CODES = {
        'en': 'en',
        'ar': 'ar'
    }
