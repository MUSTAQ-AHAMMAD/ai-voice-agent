# Usage Examples

This document provides practical examples of how to use the AI Voice Agent.

## Example 1: Basic Text-Only Usage

```python
from voice_agent import VoiceAgent

# Initialize the agent
agent = VoiceAgent()

# Ask questions in English
response = agent.process_query("What products do you offer?", language='en')
print(f"Answer: {response['answer']}")
print(f"Found in KB: {response['found']}")

# Ask questions in Arabic
response = agent.process_query("ما هي خطط الأسعار لديكم؟", language='ar')
print(f"Answer: {response['answer']}")
```

## Example 2: Adding Custom Q&A Pairs

```python
from voice_agent import VoiceAgent

agent = VoiceAgent()

# Add new Q&A pairs
new_qa_pairs = [
    {
        'question': 'Do you offer technical support?',
        'answer': 'Yes, we offer 24/7 technical support via email, chat, and phone.',
        'language': 'en',
        'category': 'post_sales'
    },
    {
        'question': 'What is your warranty policy?',
        'answer': 'All our products come with a 1-year warranty covering manufacturing defects.',
        'language': 'en',
        'category': 'post_sales'
    },
    {
        'question': 'هل تقدمون دعم فني؟',
        'answer': 'نعم، نقدم دعم فني على مدار الساعة عبر البريد الإلكتروني والدردشة والهاتف.',
        'language': 'ar',
        'category': 'post_sales'
    }
]

# Train the agent
agent.train(new_qa_pairs)

# Test the new knowledge
response = agent.process_query("Do you provide technical support?", language='en')
print(response['answer'])
```

## Example 3: Batch Training from File

```python
import json
from voice_agent import VoiceAgent

# Prepare training data
training_data = {
    'qa_pairs': [
        {
            'question': 'What are your business hours?',
            'answer': 'We are open Monday to Friday, 9 AM to 6 PM EST.',
            'language': 'en',
            'category': 'general'
        },
        {
            'question': 'Do you accept credit cards?',
            'answer': 'Yes, we accept all major credit cards including Visa, MasterCard, and American Express.',
            'language': 'en',
            'category': 'pre_sales'
        }
    ]
}

# Save to file
with open('custom_training.json', 'w', encoding='utf-8') as f:
    json.dump(training_data, f, ensure_ascii=False, indent=2)

# Train from file
agent = VoiceAgent()
with open('custom_training.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    agent.train(data['qa_pairs'])
```

## Example 4: Checking Conversation History

```python
from voice_agent import VoiceAgent

agent = VoiceAgent()

# Have a conversation
agent.process_query("What products do you offer?", language='en')
agent.process_query("Do you offer a free trial?", language='en')
agent.process_query("How can I contact support?", language='en')

# Get conversation history
history = agent.get_conversation_history()

print(f"Total interactions: {len(history)}")
for i, interaction in enumerate(history, 1):
    print(f"\nInteraction {i}:")
    print(f"  User: {interaction['query']}")
    print(f"  Agent: {interaction['response']}")
    print(f"  Language: {interaction['language']}")
```

## Example 5: Custom Configuration

```python
from voice_agent import VoiceAgent
from config import Config

# Create custom config
class CustomConfig(Config):
    AGENT_NAME = "Customer Service Bot"
    DEFAULT_LANGUAGE = "ar"  # Start with Arabic
    QA_DATABASE_PATH = "./custom_data/qa_database.json"

# Initialize with custom config
agent = VoiceAgent(config=CustomConfig())
```

## Example 6: Search Knowledge Base Directly

```python
from qa_knowledge_base import QAKnowledgeBase

# Initialize knowledge base
kb = QAKnowledgeBase(
    qa_database_path='./data/qa_database.json',
    vector_db_path='./data/vector_db'
)

# Search for similar questions
query = "How do I get a refund?"
results = kb.search(query, top_k=3)

print(f"Top {len(results)} results for: {query}\n")
for i, result in enumerate(results, 1):
    print(f"{i}. Question: {result['question']}")
    print(f"   Answer: {result['answer']}")
    print(f"   Similarity: {result['similarity']:.3f}")
    print()
```

## Example 7: Text-to-Speech Only

```python
from text_to_speech import TextToSpeech

tts = TextToSpeech()

# Speak in English
tts.speak("Hello! How can I help you today?", language='en')

# Speak in Arabic
tts.speak("مرحباً! كيف يمكنني مساعدتك اليوم؟", language='ar')

# Save to file instead of speaking
tts.save_to_file(
    "Welcome to our customer service.",
    "welcome.mp3",
    language='en'
)
```

## Example 8: Speech Recognition Only

```python
from speech_to_text import SpeechToText

stt = SpeechToText()

# Listen and recognize
print("Speak now...")
text, language = stt.listen_and_recognize(auto_detect=True)

if text:
    print(f"You said ({language}): {text}")
else:
    print("No speech detected")
```

## Example 9: Building a Custom Bot with Categories

```python
from voice_agent import VoiceAgent

agent = VoiceAgent()

# Define Q&A for different departments
sales_qa = [
    {
        'question': 'What payment plans are available?',
        'answer': 'We offer monthly, quarterly, and annual payment plans with discounts for longer commitments.',
        'language': 'en',
        'category': 'pre_sales'
    }
]

support_qa = [
    {
        'question': 'How do I reset my account?',
        'answer': 'To reset your account, go to Settings > Account > Reset. This will clear all your data.',
        'language': 'en',
        'category': 'post_sales'
    }
]

# Train with different categories
agent.train(sales_qa + support_qa)

# Use the agent
response = agent.process_query("What payment plans do you have?", language='en')
print(response['answer'])
```

## Example 10: Error Handling

```python
from voice_agent import VoiceAgent
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

try:
    agent = VoiceAgent()
    
    # Handle unknown questions gracefully
    response = agent.process_query("What is the meaning of life?", language='en')
    
    if not response['found']:
        print("Question not in knowledge base")
        print(f"Fallback response: {response['answer']}")
        # Log for later training
        logging.warning(f"Unknown question: What is the meaning of life?")
    else:
        print(f"Answer: {response['answer']}")
        
except Exception as e:
    logging.error(f"Error: {e}")
    print("An error occurred. Please try again.")
```

## Tips for Best Results

1. **Training Data Quality**: Add diverse phrasings of the same question
2. **Language Consistency**: Keep Q&A pairs in the same language
3. **Specific Answers**: Provide clear, concise answers
4. **Regular Updates**: Keep adding new Q&A pairs based on customer interactions
5. **Test Thoroughly**: Test with variations of questions to ensure good coverage

## Integration Examples

### Flask Web API

```python
from flask import Flask, request, jsonify
from voice_agent import VoiceAgent

app = Flask(__name__)
agent = VoiceAgent()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query')
    language = data.get('language', 'en')
    
    response = agent.process_query(query, language=language)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
```

### Command Line Interface

```python
import sys
from voice_agent import VoiceAgent

def main():
    agent = VoiceAgent()
    
    if len(sys.argv) > 1:
        # Command line query
        query = ' '.join(sys.argv[1:])
        response = agent.process_query(query, language='en')
        print(response['answer'])
    else:
        # Interactive mode
        print("AI Voice Agent - Type 'exit' to quit")
        while True:
            query = input("\nYou: ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            response = agent.process_query(query, language='en')
            print(f"Agent: {response['answer']}")

if __name__ == "__main__":
    main()
```
