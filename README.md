# AI Voice Agent for Pre-Sales and Post-Sales Support

A powerful AI-powered voice agent built with Python that handles customer inquiries in both English and Arabic. The agent can be trained with custom question-answer pairs and provides intelligent responses using semantic search and natural language processing.

## 🌟 Features

- **Multilingual Support**: Handles conversations in English and Arabic
- **Speech-to-Text**: Converts voice input to text using Google Speech Recognition
- **Text-to-Speech**: Converts responses to natural-sounding speech using gTTS
- **Intelligent Q&A**: Uses semantic search with FAISS and sentence transformers for accurate answers
- **Trainable**: Easily train the agent with custom Q&A pairs
- **Pre-Sales & Post-Sales**: Supports both sales inquiries and customer support
- **Language Detection**: Automatically detects the language of user input
- **Conversation History**: Tracks conversation history for better context

## 🛠️ Technologies Used

- **Speech Recognition**: `SpeechRecognition` library with Google Speech API
- **Text-to-Speech**: `gTTS` (Google Text-to-Speech)
- **Semantic Search**: `sentence-transformers` with multilingual models
- **Vector Database**: `FAISS` for efficient similarity search
- **NLP**: `transformers` and `langdetect` for language processing
- **Audio Processing**: `pydub` and `soundfile`

## 📋 Prerequisites

- Python 3.8 or higher
- Microphone (for voice input)
- Speakers/Headphones (for voice output)
- Internet connection (for speech recognition and TTS)

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/MUSTAQ-AHAMMAD/ai-voice-agent.git
cd ai-voice-agent
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install PyAudio** (required for microphone input):

   - **On Ubuntu/Debian**:
     ```bash
     sudo apt-get install portaudio19-dev python3-pyaudio
     pip install pyaudio
     ```
   
   - **On macOS**:
     ```bash
     brew install portaudio
     pip install pyaudio
     ```
   
   - **On Windows**:
     ```bash
     pip install pipwin
     pipwin install pyaudio
     ```

5. **Install FFmpeg** (required for audio processing):

   - **On Ubuntu/Debian**:
     ```bash
     sudo apt-get install ffmpeg
     ```
   
   - **On macOS**:
     ```bash
     brew install ffmpeg
     ```
   
   - **On Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## ⚙️ Configuration

1. **Copy the example environment file**:
```bash
cp .env.example .env
```

2. **Edit `.env` file** to customize settings:
```env
AGENT_NAME=Sales Assistant
DEFAULT_LANGUAGE=en
ENABLE_ARABIC=true
```

## 📚 Training the Agent

The agent comes with pre-loaded Q&A pairs for common pre-sales and post-sales questions in both English and Arabic. You can add more Q&A pairs in two ways:

### Option 1: Train from a JSON file

```bash
python train_agent.py data/qa_database.json
```

### Option 2: Interactive training

```bash
python train_agent.py
```

Then select option 2 and follow the prompts to add Q&A pairs interactively.

### Q&A Data Format

The training data should be in JSON format:

```json
{
  "qa_pairs": [
    {
      "question": "What products do you offer?",
      "answer": "We offer enterprise software solutions...",
      "language": "en",
      "category": "pre_sales"
    },
    {
      "question": "ما هي المنتجات التي تقدمونها؟",
      "answer": "نقدم مجموعة واسعة من حلول البرمجيات...",
      "language": "ar",
      "category": "pre_sales"
    }
  ]
}
```

## 🎯 Usage

### Demo Mode (No Microphone Required)

Run the demo to test the agent without a microphone:

```bash
python demo.py
```

Select from three demo modes:
1. **Text-only mode**: Test Q&A without audio
2. **TTS demo**: Hear the agent's responses (requires speakers)
3. **Full voice mode**: Complete voice interaction (requires microphone and speakers)

### Full Voice Agent Mode

Run the agent with full voice capabilities:

```bash
python voice_agent.py
```

The agent will:
1. Greet you in the default language
2. Listen for your questions
3. Automatically detect the language
4. Find the best answer from the knowledge base
5. Respond with voice

**To exit**: Say "exit", "quit", "goodbye", or "وداعا" (Arabic for goodbye)

## 📖 Code Structure

```
ai-voice-agent/
├── config.py              # Configuration settings
├── speech_to_text.py      # Speech recognition module
├── text_to_speech.py      # Text-to-speech module
├── qa_knowledge_base.py   # Q&A knowledge base with semantic search
├── voice_agent.py         # Main voice agent orchestrator
├── train_agent.py         # Training script
├── demo.py                # Demo script
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment configuration
└── data/
    ├── qa_database.json   # Q&A pairs database
    └── vector_db/         # FAISS vector database
```

## 🔧 API Usage

You can also use the agent programmatically:

```python
from voice_agent import VoiceAgent

# Initialize the agent
agent = VoiceAgent()

# Process a text query
response = agent.process_query("What products do you offer?", language='en')
print(response['answer'])

# Train with new Q&A pairs
qa_pairs = [
    {
        'question': 'New question?',
        'answer': 'New answer',
        'language': 'en',
        'category': 'pre_sales'
    }
]
agent.train(qa_pairs)

# Run in interactive voice mode
agent.run()
```

## 🌍 Supported Languages

Currently supported languages:
- **English** (en)
- **Arabic** (ar)

The agent uses multilingual models that can be extended to support additional languages with minimal changes.

## 🎨 Customization

### Adding New Languages

1. Update `config.py` to add the language code
2. Add Q&A pairs in the new language to the database
3. The multilingual model will automatically handle the new language

### Changing TTS Voice

You can modify `text_to_speech.py` to use different TTS engines:
- `pyttsx3` for offline TTS
- `gTTS` for online TTS (current)
- Cloud TTS services (Google Cloud, Amazon Polly, etc.)

### Improving Q&A Accuracy

- Add more Q&A pairs to the database
- Use more specific questions in training data
- Adjust the similarity threshold in `qa_knowledge_base.py`

## 🐛 Troubleshooting

### Microphone Not Working
- Check microphone permissions
- Verify microphone is properly connected
- Test with other applications

### Audio Playback Issues
- Ensure speakers/headphones are connected
- Check system volume
- Verify FFmpeg is installed

### Recognition Errors
- Speak clearly and at a moderate pace
- Ensure minimal background noise
- Check internet connection (required for Google Speech API)

### FAISS Installation Issues
- Use `faiss-cpu` instead of `faiss-gpu` if you don't have CUDA
- On some systems, you may need to install from conda: `conda install -c pytorch faiss-cpu`

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For questions and support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Google Speech Recognition for speech-to-text
- gTTS for text-to-speech
- Sentence Transformers for multilingual embeddings
- FAISS for efficient similarity search

## 🔮 Future Enhancements

- [ ] Add more languages
- [ ] Integration with CRM systems
- [ ] Real-time sentiment analysis
- [ ] Voice analytics and reporting
- [ ] Web interface
- [ ] API endpoints for integration
- [ ] Database backend for Q&A storage
- [ ] Admin dashboard for managing Q&A pairs
- [ ] Custom wake word detection
- [ ] Offline mode support
