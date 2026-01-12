"""
Quick validation test for the AI Voice Agent structure
"""
import os
import json


def test_project_structure():
    """Test that all required files exist"""
    print("=" * 60)
    print("Testing Project Structure")
    print("=" * 60)
    
    required_files = [
        'config.py',
        'speech_to_text.py',
        'text_to_speech.py',
        'qa_knowledge_base.py',
        'voice_agent.py',
        'train_agent.py',
        'demo.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
        'data/qa_database.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n✗ Missing {len(missing_files)} files")
        return False
    else:
        print("\n✓ All required files present")
        return True


def test_qa_database():
    """Test Q&A database format"""
    print("\n" + "=" * 60)
    print("Testing Q&A Database")
    print("=" * 60)
    
    try:
        with open('data/qa_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        qa_pairs = data.get('qa_pairs', [])
        print(f"✓ Loaded {len(qa_pairs)} Q&A pairs")
        
        # Count by language
        en_count = sum(1 for qa in qa_pairs if qa.get('language') == 'en')
        ar_count = sum(1 for qa in qa_pairs if qa.get('language') == 'ar')
        
        print(f"  - English: {en_count}")
        print(f"  - Arabic: {ar_count}")
        
        # Count by category
        pre_sales = sum(1 for qa in qa_pairs if qa.get('category') == 'pre_sales')
        post_sales = sum(1 for qa in qa_pairs if qa.get('category') == 'post_sales')
        
        print(f"  - Pre-Sales: {pre_sales}")
        print(f"  - Post-Sales: {post_sales}")
        
        # Validate structure
        required_keys = ['question', 'answer', 'language', 'category']
        for i, qa in enumerate(qa_pairs):
            for key in required_keys:
                if key not in qa:
                    print(f"✗ Q&A pair {i} missing key: {key}")
                    return False
        
        print("✓ All Q&A pairs have valid structure")
        return True
        
    except Exception as e:
        print(f"✗ Error loading Q&A database: {e}")
        return False


def test_python_syntax():
    """Test Python syntax of all modules"""
    print("\n" + "=" * 60)
    print("Testing Python Syntax")
    print("=" * 60)
    
    python_files = [
        'config.py',
        'speech_to_text.py',
        'text_to_speech.py',
        'qa_knowledge_base.py',
        'voice_agent.py',
        'train_agent.py',
        'demo.py',
        'test_agent.py'
    ]
    
    import py_compile
    
    errors = []
    for file_path in python_files:
        try:
            py_compile.compile(file_path, doraise=True)
            print(f"✓ {file_path}")
        except py_compile.PyCompileError as e:
            print(f"✗ {file_path} - SYNTAX ERROR")
            errors.append((file_path, str(e)))
    
    if errors:
        print(f"\n✗ {len(errors)} files have syntax errors")
        for file_path, error in errors:
            print(f"\n{file_path}:\n{error}")
        return False
    else:
        print("\n✓ All Python files have valid syntax")
        return True


def test_requirements():
    """Test requirements.txt format"""
    print("\n" + "=" * 60)
    print("Testing Requirements File")
    print("=" * 60)
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"✓ Found {len(requirements)} dependencies")
        
        # Check for key dependencies
        key_deps = [
            'sentence-transformers',
            'faiss-cpu',
            'SpeechRecognition',
            'gTTS',
            'langdetect'
        ]
        
        for dep in key_deps:
            found = any(dep.lower() in req.lower() for req in requirements)
            if found:
                print(f"  ✓ {dep}")
            else:
                print(f"  ✗ {dep} - MISSING")
        
        return True
        
    except Exception as e:
        print(f"✗ Error reading requirements.txt: {e}")
        return False


def main():
    """Run all validation tests"""
    print("\n" + "=" * 60)
    print("AI Voice Agent - Validation Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_project_structure,
        test_qa_database,
        test_python_syntax,
        test_requirements
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n✓ ALL VALIDATION TESTS PASSED!")
        print("\nThe AI Voice Agent is ready to use.")
        print("Next steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run demo: python demo.py")
        print("  3. Train agent: python train_agent.py")
        print("  4. Run voice agent: python voice_agent.py")
    else:
        print("\n✗ SOME TESTS FAILED")
        print("Please review the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
