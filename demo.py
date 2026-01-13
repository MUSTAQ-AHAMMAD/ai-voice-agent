"""
Demo script for AI Voice Agent
Demonstrates the agent without requiring microphone input
"""
from voice_agent import VoiceAgent
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_text_mode():
    """Demo the agent in text-only mode (no voice)"""
    print("=" * 60)
    print("AI Voice Agent - Text Mode Demo")
    print("=" * 60)
    
    # Initialize agent
    print("\nInitializing agent...")
    agent = VoiceAgent()
    
    print("\n" + "=" * 60)
    print("Agent initialized successfully!")
    print("=" * 60)
    
    # Demo questions in English
    print("\n\n" + "=" * 60)
    print("Demo: English Questions")
    print("=" * 60)
    
    english_questions = [
        "What products do you offer?",
        "Do you offer a free trial?",
        "What are your pricing plans?",
        "How can I contact support?",
        "What is your refund policy?"
    ]
    
    for question in english_questions:
        print(f"\n👤 User: {question}")
        response = agent.process_query(question, language='en')
        print(f"🤖 Agent: {response['answer']}")
        print("-" * 60)
    
    # Demo questions in Arabic
    print("\n\n" + "=" * 60)
    print("Demo: Arabic Questions")
    print("=" * 60)
    
    arabic_questions = [
        "ما هي المنتجات التي تقدمونها؟",
        "هل تقدمون تجربة مجانية؟",
        "كيف يمكنني الاتصال بالدعم؟"
    ]
    
    for question in arabic_questions:
        print(f"\n👤 User: {question}")
        response = agent.process_query(question, language='ar')
        print(f"🤖 Agent: {response['answer']}")
        print("-" * 60)
    
    # Demo unknown question
    print("\n\n" + "=" * 60)
    print("Demo: Unknown Question (Fallback)")
    print("=" * 60)
    
    unknown_question = "What is the meaning of life?"
    print(f"\n👤 User: {unknown_question}")
    response = agent.process_query(unknown_question, language='en')
    print(f"🤖 Agent: {response['answer']}")
    print("-" * 60)
    
    # Show conversation history
    print("\n\n" + "=" * 60)
    print("Conversation History")
    print("=" * 60)
    history = agent.get_conversation_history()
    print(f"\nTotal interactions: {len(history)}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


def demo_with_tts():
    """Demo the agent with text-to-speech (no microphone needed)"""
    print("=" * 60)
    print("AI Voice Agent - TTS Demo")
    print("=" * 60)
    print("\nThis demo will speak the responses using text-to-speech.")
    print("Make sure your speakers are on!")
    
    input("\nPress Enter to continue...")
    
    # Initialize agent
    print("\nInitializing agent...")
    agent = VoiceAgent()
    
    # Greet the user
    print("\n" + "=" * 60)
    agent.greet()
    
    # Demo a few questions with TTS
    questions = [
        ("What products do you offer?", "en"),
        ("ما هي خطط الأسعار لديكم؟", "ar")
    ]
    
    for question, lang in questions:
        print("\n" + "=" * 60)
        print(f"Question ({lang}): {question}")
        response = agent.process_query(question, language=lang)
        print(f"Response: {response['answer']}")
        agent.tts.speak(response['answer'], language=lang)
        input("\nPress Enter for next question...")
    
    print("\n" + "=" * 60)
    print("TTS Demo completed!")
    print("=" * 60)


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("AI Voice Agent Demo")
    print("=" * 60)
    print("\nSelect demo mode:")
    print("1. Text-only mode (no audio)")
    print("2. Text-to-Speech demo (requires speakers)")
    print("3. Full voice mode (requires microphone and speakers)")
    
    choice = input("\nSelect mode (1/2/3): ").strip()
    
    if choice == '1':
        demo_text_mode()
    elif choice == '2':
        demo_with_tts()
    elif choice == '3':
        print("\nStarting full voice mode...")
        print("The agent will listen for your questions and respond with voice.")
        print("Say 'exit', 'quit', or 'goodbye' to end the conversation.\n")
        input("Press Enter to start...")
        agent = VoiceAgent()
        agent.run()
    else:
        print("Invalid choice. Running text-only demo by default.")
        demo_text_mode()


if __name__ == "__main__":
    main()
