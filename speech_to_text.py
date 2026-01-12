"""
Speech-to-Text module for AI Voice Agent
Handles audio input and converts speech to text in multiple languages
"""
import speech_recognition as sr
from langdetect import detect
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechToText:
    """Handles speech-to-text conversion for multiple languages"""
    
    def __init__(self):
        """Initialize the speech recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        logger.info("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logger.info("Microphone calibration complete.")
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[sr.AudioData]:
        """
        Listen for audio input from the microphone
        
        Args:
            timeout: Maximum time to wait for phrase to start
            phrase_time_limit: Maximum time for the phrase
            
        Returns:
            Audio data or None if no speech detected
        """
        try:
            logger.info("Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            logger.info("Audio captured successfully.")
            return audio
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out. No speech detected.")
            return None
        except Exception as e:
            logger.error(f"Error while listening: {e}")
            return None
    
    def recognize(self, audio: sr.AudioData, language: str = 'en') -> Optional[str]:
        """
        Convert audio to text using Google Speech Recognition
        
        Args:
            audio: Audio data to recognize
            language: Language code (en for English, ar for Arabic)
            
        Returns:
            Recognized text or None if recognition failed
        """
        if audio is None:
            return None
        
        try:
            # Map language codes to Google Speech API codes
            lang_map = {
                'en': 'en-US',
                'ar': 'ar-SA'
            }
            lang_code = lang_map.get(language, 'en-US')
            
            logger.info(f"Recognizing speech in {language}...")
            text = self.recognizer.recognize_google(audio, language=lang_code)
            logger.info(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            logger.error(f"Error during recognition: {e}")
            return None
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        
        Args:
            text: Input text
            
        Returns:
            Language code (en or ar)
        """
        try:
            detected = detect(text)
            # Map detected language to supported languages
            if detected == 'ar':
                return 'ar'
            else:
                return 'en'
        except Exception as e:
            logger.warning(f"Language detection failed: {e}. Defaulting to English.")
            return 'en'
    
    def listen_and_recognize(self, language: str = 'en', auto_detect: bool = True) -> Tuple[Optional[str], str]:
        """
        Listen and recognize speech in one call
        
        Args:
            language: Expected language code
            auto_detect: Whether to auto-detect language from text
            
        Returns:
            Tuple of (recognized_text, detected_language)
        """
        audio = self.listen()
        if audio is None:
            return None, language
        
        text = self.recognize(audio, language)
        if text and auto_detect:
            detected_lang = self.detect_language(text)
            return text, detected_lang
        
        return text, language
