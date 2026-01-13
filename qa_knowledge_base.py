"""
Q&A Knowledge Base module for AI Voice Agent
Handles question-answer pairs and semantic search using FAISS
"""
import json
import os
import logging
from typing import List, Dict, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QAKnowledgeBase:
    """Manages question-answer knowledge base with semantic search"""
    
    def __init__(self, qa_database_path: str, vector_db_path: str):
        """
        Initialize the Q&A knowledge base
        
        Args:
            qa_database_path: Path to the JSON file containing Q&A pairs
            vector_db_path: Path to store/load the vector database
        """
        self.qa_database_path = qa_database_path
        self.vector_db_path = vector_db_path
        self.qa_pairs = []
        self.index = None
        
        # Initialize sentence transformer model for semantic search
        logger.info("Loading sentence transformer model...")
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        logger.info("Model loaded successfully.")
        
        # Load Q&A database
        self.load_qa_database()
        
        # Build or load vector index
        self.build_or_load_index()
    
    def load_qa_database(self):
        """Load Q&A pairs from JSON file"""
        try:
            if os.path.exists(self.qa_database_path):
                with open(self.qa_database_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.qa_pairs = data.get('qa_pairs', [])
                logger.info(f"Loaded {len(self.qa_pairs)} Q&A pairs from database.")
            else:
                logger.warning(f"Q&A database not found at {self.qa_database_path}. Starting with empty database.")
                self.qa_pairs = []
        except Exception as e:
            logger.error(f"Error loading Q&A database: {e}")
            self.qa_pairs = []
    
    def save_qa_database(self):
        """Save Q&A pairs to JSON file"""
        try:
            # Validate and normalize the path to prevent directory traversal
            normalized_path = os.path.abspath(self.qa_database_path)
            base_dir = os.path.abspath(os.getcwd())
            
            # Ensure the path is within the project directory
            if not normalized_path.startswith(base_dir):
                logger.error(f"Invalid path: {self.qa_database_path} is outside project directory")
                return
            
            os.makedirs(os.path.dirname(normalized_path), exist_ok=True)
            with open(normalized_path, 'w', encoding='utf-8') as f:
                json.dump({'qa_pairs': self.qa_pairs}, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.qa_pairs)} Q&A pairs to database.")
        except Exception as e:
            logger.error(f"Error saving Q&A database: {e}")
    
    def add_qa_pair(self, question: str, answer: str, language: str = 'en', category: str = 'general'):
        """
        Add a new Q&A pair to the knowledge base
        
        Args:
            question: Question text
            answer: Answer text
            language: Language code (en or ar)
            category: Category (pre_sales, post_sales, general)
        """
        qa_pair = {
            'question': question,
            'answer': answer,
            'language': language,
            'category': category
        }
        self.qa_pairs.append(qa_pair)
        logger.info(f"Added Q&A pair: {question[:50]}...")
    
    def build_or_load_index(self):
        """Build or load FAISS index for semantic search"""
        if not self.qa_pairs:
            logger.warning("No Q&A pairs to index.")
            return
        
        index_file = os.path.join(self.vector_db_path, 'faiss.index')
        metadata_file = os.path.join(self.vector_db_path, 'index_metadata.json')
        
        try:
            # Check if index exists and is up-to-date
            should_rebuild = False
            
            if os.path.exists(index_file) and os.path.exists(metadata_file):
                # Load metadata to check if index matches current Q&A data
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Compare number of Q&A pairs and questions
                current_questions = [qa['question'] for qa in self.qa_pairs]
                stored_count = metadata.get('qa_count', 0)
                
                if stored_count != len(self.qa_pairs):
                    logger.info("Q&A count changed, rebuilding index...")
                    should_rebuild = True
                else:
                    logger.info("Loading existing FAISS index...")
                    self.index = faiss.read_index(index_file)
                    logger.info("FAISS index loaded successfully.")
            else:
                should_rebuild = True
            
            if should_rebuild:
                logger.info("Building new FAISS index...")
                self._build_index()
                logger.info("FAISS index built successfully.")
                
        except Exception as e:
            logger.error(f"Error with FAISS index: {e}. Rebuilding...")
            self._build_index()
    
    def _build_index(self):
        """Build FAISS index from Q&A pairs"""
        if not self.qa_pairs:
            return
        
        # Extract questions
        questions = [qa['question'] for qa in self.qa_pairs]
        
        # Generate embeddings
        logger.info("Generating embeddings for questions...")
        embeddings = self.model.encode(questions, show_progress_bar=True)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        # Save index and metadata
        os.makedirs(self.vector_db_path, exist_ok=True)
        index_file = os.path.join(self.vector_db_path, 'faiss.index')
        metadata_file = os.path.join(self.vector_db_path, 'index_metadata.json')
        
        faiss.write_index(self.index, index_file)
        
        # Save metadata for validation
        metadata = {
            'qa_count': len(self.qa_pairs),
            'dimension': dimension,
            'questions': questions[:5]  # Store first 5 questions as sample for debugging
        }
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"FAISS index saved to {index_file}")
    
    def search(self, query: str, top_k: int = 3, language: Optional[str] = None) -> List[Dict]:
        """
        Search for similar questions in the knowledge base
        
        Args:
            query: User's question
            top_k: Number of top results to return
            language: Optional language filter
            
        Returns:
            List of matching Q&A pairs with similarity scores
        """
        if not self.qa_pairs or self.index is None:
            logger.warning("Knowledge base is empty or index not built.")
            return []
        
        try:
            # Generate embedding for query
            query_embedding = self.model.encode([query])
            
            # Search in FAISS index
            distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
            
            # Prepare results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.qa_pairs):
                    qa_pair = self.qa_pairs[idx].copy()
                    qa_pair['similarity'] = 1 / (1 + distances[0][i])  # Convert distance to similarity
                    
                    # Filter by language if specified
                    if language is None or qa_pair.get('language') == language:
                        results.append(qa_pair)
            
            return results
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []
    
    def get_best_answer(self, query: str, language: Optional[str] = None, threshold: float = 0.7) -> Optional[str]:
        """
        Get the best answer for a query
        
        Args:
            query: User's question
            language: Optional language filter
            threshold: Minimum similarity threshold
            
        Returns:
            Best matching answer or None
        """
        results = self.search(query, top_k=1, language=language)
        
        if results and results[0]['similarity'] >= threshold:
            return results[0]['answer']
        
        return None
    
    def train_from_list(self, qa_list: List[Dict]):
        """
        Train the knowledge base from a list of Q&A pairs
        
        Args:
            qa_list: List of dictionaries with 'question', 'answer', 'language', 'category'
        """
        for qa in qa_list:
            self.add_qa_pair(
                question=qa.get('question', ''),
                answer=qa.get('answer', ''),
                language=qa.get('language', 'en'),
                category=qa.get('category', 'general')
            )
        
        # Save and rebuild index
        self.save_qa_database()
        self._build_index()
        logger.info(f"Training completed with {len(qa_list)} Q&A pairs.")
