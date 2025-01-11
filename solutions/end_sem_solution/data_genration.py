import os
import json
import random
import pickle
import hashlib
from typing import List, Dict, Tuple
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

class CachedAdvancedRAGDatasetGenerator:
    def __init__(self, document_path: str, cache_dir: str = ".cache"):
        """
        Initialize Advanced RAG Dataset Generator with caching
        
        :param document_path: Path to the source document
        :param cache_dir: Directory to store cached embeddings
        """
        self.document_path = document_path
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize models first
        self.embeddings = HuggingFaceEmbeddings()
        self.llm = ChatGroq(
            model_name="llama3-8b-8192", 
            api_key="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", 
            temperature=0.7
        )
        
        # Create a unique cache key based on the document content
        self.cache_key = self._generate_cache_key()
        
        # Try to load from cache first
        self.vectorstore = self._load_or_create_vectorstore()

        # Define persona pairs (each pair has a user and assistant role)
        # self.persona_pairs = [
        #     {
        #         "name": "student_teacher",
        #         "user": {
        #             "role": "system",
        #             "content": "You are a curious student who asks detailed questions about concepts you don't understand."
        #         },
        #         "assistant": {
        #             "role": "system",
        #             "content": "You are a patient teacher who explains concepts clearly and encourages deeper understanding."
        #         },
        #         "typical_initiator": "user"  # Students typically initiate
        #     },
        #     {
        #         "name": "interviewer_candidate",
        #         "user": {
        #             "role": "system",
        #             "content": "You are a technical interview candidate demonstrating your knowledge and problem-solving skills."
        #         },
        #         "assistant": {
        #             "role": "system",
        #             "content": "You are a technical interviewer who asks challenging questions to assess understanding."
        #         },
        #         "typical_initiator": "assistant"  # Interviewer typically initiates
        #     },
        #     {
        #         "name": "researcher_mentor",
        #         "user": {
        #             "role": "system",
        #             "content": "You are a PhD researcher exploring advanced concepts and methodology questions."
        #         },
        #         "assistant": {
        #             "role": "system",
        #             "content": "You are a research mentor who guides exploration while encouraging independent thinking."
        #         },
        #         "typical_initiator": "user"  # Researcher typically initiates
        #     },
        #     {
        #         "name": "practitioner_consultant",
        #         "user": {
        #             "role": "system",
        #             "content": "You are a practitioner seeking advice on implementing ML solutions in real-world scenarios."
        #         },
        #         "assistant": {
        #             "role": "system",
        #             "content": "You are a consultant who proactively identifies potential issues and suggests best practices."
        #         },
        #         "typical_initiator": "assistant"  # Consultant often initiates with assessments
        #     }
        # ]

        self.persona_pairs = [
    {
        "name": "student_teacher",
        "user": {
            "role": "system",
            "content": "You are a teacher who explains relevant portions of the report, clears concepts and encourages deeper understanding."
        },
        "assistant": {
            "role": "system",
            "content": "You are a curious student who asks detailed questions about the contents of a report"
        },
        "typical_initiator": "assistant"  # Assistant (student) typically initiates
    },
]

        # Initialize topics
        # self.topics = [
        #     "Linear Regression",
        #     "Logistic Regression", 
        #     "Naive Bayes",
        #     "Gaussian Discriminant Analysis (GDA)", 
        #     "Neural Networks",
        #     "Perceptron", 
        #     "Support Vector Machines (SVM)", 
        #     "Decision Trees", 
        #     "Random Forests", 
        #     "Gradient Boosting"
        # ]
        self.topics = [
    "motivation",
    "problem statment",
    "comparison with existing models",
    "proposed methodology",
    "experiments",
    "findings",
    "conclusions"
]


    # Rest of the class implementation remains the same...
    def _generate_cache_key(self) -> str:
        """Generate a unique cache key based on document content and metadata"""
        with open(self.document_path, 'rb') as f:
            content = f.read()
        mod_time = os.path.getmtime(self.document_path)
        hash_input = f"{content}{mod_time}".encode()
        return hashlib.md5(hash_input).hexdigest()

    def _get_cache_path(self) -> Path:
        """Get the full path for the cache file"""
        return self.cache_dir / f"vectorstore_{self.cache_key}.pkl"

    def _load_or_create_vectorstore(self) -> FAISS:
        """Load vectorstore from cache if it exists, otherwise create and cache it"""
        cache_path = self._get_cache_path()
        
        if cache_path.exists():
            print("Loading vectorstore from cache...")
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        
        print("Creating new vectorstore...")
        loader = PyMuPDFLoader(self.document_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, 
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(documents)
        
        vectorstore = FAISS.from_documents(
            documents=splits, 
            embedding=self.embeddings
        )
        
        with open(cache_path, 'wb') as f:
            pickle.dump(vectorstore, f)
        
        return vectorstore

    def generate_initial_query(self, topic: str, persona_pair: Dict, initiator: str) -> str:
        """Generate initial query based on the persona and initiator"""
        if initiator == "assistant":
            prompt = f"""As a {persona_pair['assistant']['content']}, 
            generate a short and simple initial question about {topic}.
            The question should reflect your persona's perspective as a curious student.
            Keep the question focused on understanding the {topic} section of the report.
            Example: "I'm reading through the {topic} section of the report and I'm curious about [specific aspect]. Could you help me understand...?" """
        else:
            prompt = f"""As a {persona_pair['user']['content']}, 
            generate a short and to-the-point response or explanation about {topic}.
            The response should reflect your role as a teacher explaining the content.
            Example: "Let me explain the key points from the {topic} section of the report..." """
            
        response = self.llm.invoke(prompt)
        return response.content

    def generate_follow_up(self, topic: str, previous_messages: List[Dict], current_speaker_persona: Dict) -> str:
        """Generate a follow-up message based on conversation history"""
        conversation_history = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in previous_messages 
            if msg['role'] in ['user', 'assistant']
        ])
        
        if current_speaker_persona['content'].startswith("You are a curious student"):
            prompt = f"""As a curious student,
            generate a follow-up question about {topic} based on the previous responses.
            Focus on asking for clarification or deeper understanding of the content.
            
            Previous conversation:
            {conversation_history}
            
            Generate a natural follow-up question that demonstrates curiosity and desire to learn more."""
        else:
            prompt = f"""As a teacher,
            generate a detailed explanation in response to the student's question about {topic}.
            
            Previous conversation:
            {conversation_history}
            
            Provide a clear and informative response that helps the student understand the content better."""
        
        response = self.llm.invoke(prompt)
        return response.content

    def generate_dataset(self, num_conversations: int = 10) -> List[Dict]:
        """Generate dataset with diverse conversation structures"""
        dataset = []
        topics = random.sample(self.topics, min(len(self.topics), num_conversations))
        
        for topic in topics:
            persona_pair = random.choice(self.persona_pairs)
            initiator = persona_pair['typical_initiator'] if random.random() < 0.8 else (
                'user' if persona_pair['typical_initiator'] == 'assistant' else 'assistant'
            )
            
            retrieval_results = self.vectorstore.similarity_search(topic, k=3)
            context = " ".join([doc.page_content for doc in retrieval_results])
            
            conversation_messages = [
                {"role": "system", "content": f"Context: {context}"},
                persona_pair['user'],
                persona_pair['assistant']
            ]
            
            initial_query = self.generate_initial_query(topic, persona_pair, initiator)
            
            if initiator == "user":
                conversation_messages.append({"role": "user", "content": initial_query})
            else:
                conversation_messages.append({"role": "assistant", "content": initial_query})
            
            num_turns = random.randint(4, 5)
            current_speaker = "assistant" if initiator == "user" else "user"
            
            for _ in range(num_turns):
                current_persona = (
                    persona_pair['assistant'] if current_speaker == "assistant" 
                    else persona_pair['user']
                )
                
                follow_up = self.generate_follow_up(
                    topic, 
                    conversation_messages, 
                    current_persona
                )
                
                conversation_messages.append({
                    "role": current_speaker,
                    "content": follow_up
                })
                
                current_speaker = "user" if current_speaker == "assistant" else "assistant"
            
            dataset.append({
                "topic": topic,
                "persona_pair": persona_pair['name'],
                "initiator": initiator,
                "messages": conversation_messages,
                "context": context
            })
        
        return dataset

def main():
    document_path = 'arxiv.pdf'
    cache_dir = ".cache"
    
    generator = CachedAdvancedRAGDatasetGenerator(document_path, cache_dir)
    dataset = generator.generate_dataset(num_conversations=6)
    
    output_file = "advanced_rag_dataset.json"
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nGenerated dataset saved to {output_file}")
    print(f"Total conversations: {len(dataset)}")
    
    initiator_stats = {"user": 0, "assistant": 0}
    for conv in dataset:
        initiator_stats[conv["initiator"]] += 1
    
    print("\nConversation Initiator Statistics:")
    print(f"User-initiated: {initiator_stats['user']}")
    print(f"Assistant-initiated: {initiator_stats['assistant']}")

if __name__ == "__main__":
    main()