"""
Main AI Voice Agent for Pre-Sales and Post-Sales Support
Orchestrates speech-to-text, Q&A matching, and text-to-speech
"""
import logging
from typing import Optional, Dict
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from qa_knowledge_base import QAKnowledgeBase
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceAgent:
    """Main AI Voice Agent class"""
    
    def __init__(self, config: Config = None):
        """
        Initialize the Voice Agent
        
        Args:
            config: Configuration object
        """
        self.config = config or Config()
        
        logger.info(f"Initializing {self.config.AGENT_NAME}...")
        
        # Initialize components
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.kb = QAKnowledgeBase(
            qa_database_path=self.config.QA_DATABASE_PATH,
            vector_db_path=self.config.VECTOR_DB_PATH
        )
        
        # Conversation state
        self.conversation_history = []
        self.current_language = self.config.DEFAULT_LANGUAGE
        
        logger.info(f"{self.config.AGENT_NAME} initialized successfully!")
    
    def greet(self):
        """Greet the user in multiple languages"""
        greetings = {
            'en': f"Hello! I am {self.config.AGENT_NAME}. How can I help you today?",
            'ar': f"مرحباً! أنا {self.config.AGENT_NAME}. كيف يمكنني مساعدتك اليوم؟"
        }
        
        # Greet in default language
        greeting_text = greetings.get(self.current_language, greetings['en'])
        logger.info(f"Agent: {greeting_text}")
        self.tts.speak(greeting_text, language=self.current_language)
    
    def process_query(self, query: str, language: str = 'en') -> Dict:
        """
        Process a text query and generate response
        
        Args:
            query: User's question
            language: Language code
            
        Returns:
            Dictionary with response and metadata
        """
        logger.info(f"Processing query ({language}): {query}")
        
        # Search knowledge base
        answer = self.kb.get_best_answer(query, language=language)
        
        if answer:
            response = {
                'answer': answer,
                'found': True,
                'language': language
            }
        else:
            # Generate fallback response
            fallback_responses = {
                'en': "I apologize, but I don't have an answer to that question. Could you please rephrase or ask something else?",
                'ar': "أعتذر، لكن ليس لدي إجابة على هذا السؤال. هل يمكنك إعادة صياغته أو طرح سؤال آخر؟"
            }
            response = {
                'answer': fallback_responses.get(language, fallback_responses['en']),
                'found': False,
                'language': language
            }
        
        # Add to conversation history
        self.conversation_history.append({
            'query': query,
            'response': response['answer'],
            'language': language
        })
        
        return response
    
    def handle_conversation(self):
        """Handle a single conversation turn"""
        try:
            # Listen for user input
            text, detected_language = self.stt.listen_and_recognize(
                language=self.current_language,
                auto_detect=True
            )
            
            if text is None:
                logger.info("No speech detected or recognition failed.")
                return False
            
            logger.info(f"User ({detected_language}): {text}")
            
            # Update current language
            self.current_language = detected_language
            
            # Check for exit commands
            exit_commands = ['exit', 'quit', 'goodbye', 'bye', 'وداعا', 'إنهاء']
            if any(cmd in text.lower() for cmd in exit_commands):
                farewell = {
                    'en': "Thank you for contacting us. Goodbye!",
                    'ar': "شكراً لتواصلك معنا. وداعاً!"
                }
                farewell_text = farewell.get(detected_language, farewell['en'])
                logger.info(f"Agent: {farewell_text}")
                self.tts.speak(farewell_text, language=detected_language)
                return False
            
            # Process the query
            response = self.process_query(text, detected_language)
            
            # Speak the response
            logger.info(f"Agent: {response['answer']}")
            self.tts.speak(response['answer'], language=detected_language)
            
            return True
        except KeyboardInterrupt:
            logger.info("\nConversation interrupted by user.")
            return False
        except Exception as e:
            logger.error(f"Error handling conversation: {e}")
            return False
    
    def run(self):
        """Run the voice agent in interactive mode"""
        logger.info("=" * 60)
        logger.info(f"{self.config.AGENT_NAME} - Starting...")
        logger.info("=" * 60)
        
        # Greet the user
        self.greet()
        
        # Main conversation loop
        while True:
            if not self.handle_conversation():
                break
        
        logger.info("=" * 60)
        logger.info("Voice Agent session ended.")
        logger.info("=" * 60)
    
    def train(self, qa_pairs: list):
        """
        Train the agent with new Q&A pairs
        
        Args:
            qa_pairs: List of dictionaries with question, answer, language, category
        """
        logger.info(f"Training agent with {len(qa_pairs)} Q&A pairs...")
        self.kb.train_from_list(qa_pairs)
        logger.info("Training completed successfully!")
    
    def get_conversation_history(self) -> list:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared.")


def main():
    """Main entry point"""
    try:
        # Initialize agent
        agent = VoiceAgent()
        
        # Run agent
        agent.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    main()
