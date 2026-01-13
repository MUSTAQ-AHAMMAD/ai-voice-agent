# Quick Start Guide

## Prerequisites

Before running the AI Voice Agent, make sure you have:

1. **Python 3.8+** installed
2. **Microphone** (for voice input)
3. **Speakers/Headphones** (for voice output)
4. **Internet connection** (for speech recognition)

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

**Note**: Some dependencies like PyAudio and FFmpeg require system-level installation. See README.md for detailed instructions.

### 2. For Quick Testing (Without Audio Hardware)

If you don't have a microphone or want to test without audio:

```bash
python validate.py  # Validate the installation
python demo.py      # Select option 1 for text-only demo
```

## Basic Usage

### Option 1: Text-Only Demo (No Audio Required)

```bash
python demo.py
# Select option 1 - Text-only mode
```

This will:
- Show example questions and answers
- Test English and Arabic Q&A
- Demonstrate fallback responses

### Option 2: Full Voice Agent (Requires Microphone & Speakers)

```bash
python voice_agent.py
```

This will:
- Greet you with voice
- Listen for your questions
- Auto-detect language (English or Arabic)
- Respond with voice

**To exit**: Say "exit", "quit", or "goodbye"

### Option 3: Train with Custom Q&A

```bash
python train_agent.py
# Follow the prompts to add your own Q&A pairs
```

## Example Q&A

### English Questions:
- "What products do you offer?"
- "Do you offer a free trial?"
- "What are your pricing plans?"
- "How can I contact support?"

### Arabic Questions:
- "ما هي المنتجات التي تقدمونها؟"
- "هل تقدمون تجربة مجانية؟"
- "كيف يمكنني الاتصال بالدعم؟"

## Programmatic Usage

```python
from voice_agent import VoiceAgent

# Initialize
agent = VoiceAgent()

# Process a text query (no voice)
response = agent.process_query("What are your pricing plans?", language='en')
print(response['answer'])

# Add custom Q&A pairs
agent.train([
    {
        'question': 'Do you have a mobile app?',
        'answer': 'Yes, we have apps for iOS and Android.',
        'language': 'en',
        'category': 'pre_sales'
    }
])
```

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Microphone not found"
- Check microphone connection
- Grant microphone permissions to terminal/Python
- Test with: `python -m speech_recognition`

### "Audio playback issues"
- Ensure speakers are connected
- Check system volume
- Install FFmpeg (see README.md)

### "No matches found for queries"
- The knowledge base needs more Q&A pairs
- Add more training data using `train_agent.py`
- Lower the similarity threshold in `qa_knowledge_base.py`

## Next Steps

1. **Add your own Q&A pairs**: Edit `data/qa_database.json` or use `train_agent.py`
2. **Customize greetings**: Edit `voice_agent.py` greet() method
3. **Add more languages**: Update `config.py` and add Q&A pairs
4. **Integrate with your system**: Use the VoiceAgent class in your application

## Getting Help

- Read the full README.md for detailed documentation
- Check the code comments for implementation details
- Open an issue on GitHub for bugs or questions

## Files Overview

- `voice_agent.py` - Main agent (run this)
- `demo.py` - Demo script (test without full setup)
- `train_agent.py` - Add Q&A pairs
- `validate.py` - Validate installation
- `data/qa_database.json` - Q&A knowledge base
- `config.py` - Configuration settings
