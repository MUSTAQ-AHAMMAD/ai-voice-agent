"""
Training script for AI Voice Agent
Use this to add new Q&A pairs to the knowledge base
"""
from voice_agent import VoiceAgent
import json


def load_training_data(file_path: str):
    """Load training data from a JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('qa_pairs', [])


def train_agent_from_file(file_path: str):
    """
    Train the agent with Q&A pairs from a JSON file
    
    Args:
        file_path: Path to the JSON file containing Q&A pairs
    """
    print("=" * 60)
    print("AI Voice Agent Training")
    print("=" * 60)
    
    # Load training data
    print(f"\nLoading training data from {file_path}...")
    qa_pairs = load_training_data(file_path)
    print(f"Loaded {len(qa_pairs)} Q&A pairs.")
    
    # Initialize agent
    print("\nInitializing agent...")
    agent = VoiceAgent()
    
    # Train agent
    print("\nTraining agent...")
    agent.train(qa_pairs)
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)


def train_agent_interactive():
    """Train the agent interactively by adding Q&A pairs"""
    print("=" * 60)
    print("AI Voice Agent - Interactive Training")
    print("=" * 60)
    
    # Initialize agent
    agent = VoiceAgent()
    
    qa_pairs = []
    
    print("\nEnter Q&A pairs (type 'done' when finished)")
    print("-" * 60)
    
    while True:
        print("\n")
        question = input("Question (or 'done' to finish): ").strip()
        
        if question.lower() == 'done':
            break
        
        answer = input("Answer: ").strip()
        language = input("Language (en/ar) [default: en]: ").strip() or 'en'
        category = input("Category (pre_sales/post_sales/general) [default: general]: ").strip() or 'general'
        
        qa_pairs.append({
            'question': question,
            'answer': answer,
            'language': language,
            'category': category
        })
        
        print(f"✓ Added Q&A pair (Total: {len(qa_pairs)})")
    
    if qa_pairs:
        print(f"\nTraining agent with {len(qa_pairs)} Q&A pairs...")
        agent.train(qa_pairs)
        print("\n" + "=" * 60)
        print("Training completed successfully!")
        print("=" * 60)
    else:
        print("\nNo Q&A pairs added. Training cancelled.")


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        # Train from file
        file_path = sys.argv[1]
        train_agent_from_file(file_path)
    else:
        # Interactive training
        print("\nTraining Mode:")
        print("1. Train from file")
        print("2. Interactive training")
        
        choice = input("\nSelect mode (1/2): ").strip()
        
        if choice == '1':
            file_path = input("Enter path to training data file: ").strip()
            train_agent_from_file(file_path)
        elif choice == '2':
            train_agent_interactive()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
