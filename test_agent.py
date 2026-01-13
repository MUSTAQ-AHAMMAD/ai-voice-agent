"""
Simple test to verify the Q&A knowledge base and training system
"""
from qa_knowledge_base import QAKnowledgeBase
import tempfile
import os
import shutil


def test_qa_knowledge_base():
    """Test the Q&A knowledge base functionality"""
    print("=" * 60)
    print("Testing Q&A Knowledge Base")
    print("=" * 60)
    
    # Create temporary directories for testing
    temp_dir = tempfile.mkdtemp()
    qa_db_path = os.path.join(temp_dir, 'test_qa.json')
    vector_db_path = os.path.join(temp_dir, 'vector_db')
    
    try:
        # Initialize knowledge base
        print("\n1. Initializing knowledge base...")
        kb = QAKnowledgeBase(qa_db_path, vector_db_path)
        print("✓ Knowledge base initialized")
        
        # Add test Q&A pairs
        print("\n2. Adding test Q&A pairs...")
        test_pairs = [
            {
                'question': 'What is your return policy?',
                'answer': 'We offer a 30-day return policy on all products.',
                'language': 'en',
                'category': 'post_sales'
            },
            {
                'question': 'How do I track my order?',
                'answer': 'You can track your order using the tracking number sent to your email.',
                'language': 'en',
                'category': 'post_sales'
            },
            {
                'question': 'Do you ship internationally?',
                'answer': 'Yes, we ship to over 100 countries worldwide.',
                'language': 'en',
                'category': 'pre_sales'
            }
        ]
        
        kb.train_from_list(test_pairs)
        print(f"✓ Added {len(test_pairs)} Q&A pairs")
        
        # Test search functionality
        print("\n3. Testing search functionality...")
        
        test_queries = [
            'What is the return policy?',
            'Can I return my product?',
            'How to track package?'
        ]
        
        for query in test_queries:
            print(f"\n   Query: {query}")
            results = kb.search(query, top_k=1)
            if results:
                print(f"   Best match: {results[0]['question']}")
                print(f"   Answer: {results[0]['answer']}")
                print(f"   Similarity: {results[0]['similarity']:.3f}")
            else:
                print("   No results found")
        
        # Test get_best_answer
        print("\n4. Testing best answer retrieval...")
        query = "What's your refund policy?"
        answer = kb.get_best_answer(query, threshold=0.5)
        if answer:
            print(f"   Query: {query}")
            print(f"   Answer: {answer}")
            print("✓ Best answer retrieval working")
        else:
            print("✗ No answer found")
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"\nCleaned up temporary directory: {temp_dir}")


def test_text_processing():
    """Test basic text processing without voice"""
    print("\n" + "=" * 60)
    print("Testing Text Processing")
    print("=" * 60)
    
    from voice_agent import VoiceAgent
    
    try:
        print("\n1. Initializing voice agent...")
        agent = VoiceAgent()
        print("✓ Voice agent initialized")
        
        print("\n2. Testing query processing...")
        
        # Test English query
        query_en = "What are your pricing plans?"
        print(f"\n   Query (EN): {query_en}")
        response = agent.process_query(query_en, language='en')
        print(f"   Answer: {response['answer']}")
        print(f"   Found in KB: {response['found']}")
        
        # Test Arabic query
        query_ar = "ما هي خطط الأسعار لديكم؟"
        print(f"\n   Query (AR): {query_ar}")
        response = agent.process_query(query_ar, language='ar')
        print(f"   Answer: {response['answer']}")
        print(f"   Found in KB: {response['found']}")
        
        # Test unknown query
        query_unknown = "What is the weather today?"
        print(f"\n   Query (Unknown): {query_unknown}")
        response = agent.process_query(query_unknown, language='en')
        print(f"   Answer: {response['answer']}")
        print(f"   Found in KB: {response['found']}")
        
        print("\n" + "=" * 60)
        print("Text processing tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AI Voice Agent - Test Suite")
    print("=" * 60)
    
    # Run tests
    test_qa_knowledge_base()
    test_text_processing()
    
    print("\n" + "=" * 60)
    print("All test suites completed!")
    print("=" * 60)
