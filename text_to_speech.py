"""
Text-to-Speech module for AI Voice Agent
Handles text-to-speech conversion in multiple languages
"""
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import tempfile
import uuid
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextToSpeech:
    """Handles text-to-speech conversion for multiple languages"""
    
    def __init__(self):
        """Initialize the TTS engine"""
        self.temp_dir = tempfile.gettempdir()
        logger.info("Text-to-Speech engine initialized.")
    
    def speak(self, text: str, language: str = 'en', slow: bool = False) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to convert to speech
            language: Language code (en for English, ar for Arabic)
            slow: Whether to speak slowly
            
        Returns:
            True if successful, False otherwise
        """
        if not text:
            logger.warning("No text provided for speech synthesis.")
            return False
        
        try:
            # Map language codes to gTTS codes
            lang_map = {
                'en': 'en',
                'ar': 'ar'
            }
            lang_code = lang_map.get(language, 'en')
            
            logger.info(f"Generating speech in {language}: {text}")
            
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=slow)
            
            # Save to temporary file with unique name to avoid race conditions
            temp_file = os.path.join(self.temp_dir, f'voice_agent_output_{uuid.uuid4().hex}.mp3')
            tts.save(temp_file)
            
            # Play the audio
            audio = AudioSegment.from_mp3(temp_file)
            play(audio)
            
            # Clean up
            try:
                os.remove(temp_file)
            except Exception as e:
                logger.warning(f"Could not remove temporary file: {e}")
            
            logger.info("Speech synthesis completed successfully.")
            return True
        except Exception as e:
            logger.error(f"Error during speech synthesis: {e}")
            return False
    
    def save_to_file(self, text: str, filename: str, language: str = 'en', slow: bool = False) -> bool:
        """
        Convert text to speech and save to file
        
        Args:
            text: Text to convert to speech
            filename: Output file path
            language: Language code (en for English, ar for Arabic)
            slow: Whether to speak slowly
            
        Returns:
            True if successful, False otherwise
        """
        if not text:
            logger.warning("No text provided for speech synthesis.")
            return False
        
        try:
            # Map language codes to gTTS codes
            lang_map = {
                'en': 'en',
                'ar': 'ar'
            }
            lang_code = lang_map.get(language, 'en')
            
            logger.info(f"Generating speech file in {language}: {filename}")
            
            # Generate speech
            tts = gTTS(text=text, lang=lang_code, slow=slow)
            tts.save(filename)
            
            logger.info(f"Speech saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error during speech synthesis: {e}")
            return False
