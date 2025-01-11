import os
import json
import pickle
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import os
import nest_asyncio
from nemoguardrails import RailsConfig, LLMRails

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGAssistant:
    def __init__(self, 
                 document_path: str, 
                 cache_dir: str = ".cache",
                 model_name: str = "gpt-3.5-turbo",
                 sessions_file: str = "conversation_sessions.json"):
        """
        Initialize RAG-based AI Student Assistant
        
        :param document_path: Path to the knowledge base document
        :param cache_dir: Directory to store cached embeddings
        :param model_name: OpenAI model to use
        :param sessions_file: File to store conversation sessions
        """
        self.document_path = document_path
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.sessions_file = sessions_file
        
        # Initialize models
        self.embeddings = HuggingFaceEmbeddings()
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7
        )
        
        # Load or create vectorstore
        self.vectorstore = self._initialize_knowledge_base()
        
        # Define student persona and topics
        self.student_persona = """You are a curious and engaged student who is carefully studying a research paper. 
        You ask thoughtful questions about specific aspects of the paper, seek clarification when needed, 
        and try to build connections between different sections. Your questions should be focused, 
        specific, and directly related to the paper's content."""
        
        self.topics = [
            "motivation",
            "problem statement",
            "comparison with existing models",
            "proposed methodology",
            "experiments",
            "findings",
            "conclusions"
        ]
        
        self.current_topic = None
        self.conversation_history = []
        self.context_window = 5
        
        # Initialize session metadata
        self.session_start_time = datetime.now().isoformat()
        self.session_id = hashlib.md5(f"{self.session_start_time}".encode()).hexdigest()[:10]

    def _initialize_knowledge_base(self) -> FAISS:
        """Initialize or load cached knowledge base"""
        cache_key = self._generate_cache_key()
        cache_path = self.cache_dir / f"vectorstore_{cache_key}.pkl"
        
        if cache_path.exists():
            print("Loading knowledge base from cache...")
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        
        print("Creating new knowledge base...")
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
    
    def _generate_cache_key(self) -> str:
        """Generate cache key based on document content"""
        with open(self.document_path, 'rb') as f:
            content = f.read()
        mod_time = os.path.getmtime(self.document_path)
        return hashlib.md5(f"{content}{mod_time}".encode()).hexdigest()
    
    def _get_relevant_context(self, query: str) -> str:
        """Retrieve relevant context from knowledge base"""
        results = self.vectorstore.similarity_search(query, k=3)
        return "\n".join(doc.page_content for doc in results)
    
    def _format_conversation_history(self) -> str:
        """Format recent conversation history"""
        recent_history = self.conversation_history[-self.context_window:]
        return "\n".join([
            f"{'Teacher' if msg['role'] == 'user' else 'Student'}: {msg['content']}"
            for msg in recent_history
        ])

    def generate_initial_question(self) -> str:
        """Generate an initial question about the paper"""
        if not self.current_topic:
            self.current_topic = self.topics[0]
        
        context = self._get_relevant_context(self.current_topic)
        
        prompt = f"""As a student studying this research paper, generate a thoughtful initial question about the {self.current_topic}.
        Use this context from the paper:
        {context}
        
        Frame a specific, focused question that shows engagement with the material and seeks deeper understanding.
        The question should be directly related to the content found in the context."""
        
        response = self.llm.invoke(prompt)
        
        # Store the initial question in conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response.content
        })
        
        return response.content

    def generate_follow_up_question(self, teacher_response: str) -> str:
        """Generate a follow-up question based on teacher's response"""
        context = self._get_relevant_context(teacher_response)
        history = self._format_conversation_history()
        
        prompt = f"""As a student with this persona:
        {self.student_persona}
        
        Given the teacher's response and the paper context:
        Teacher's response: {teacher_response}
        
        Paper context:
        {context}
        
        Recent conversation history:
        {history}
        
        Generate a focused follow-up question that:
        1. Builds on the teacher's response
        2. References specific content from the paper
        3. Shows understanding while seeking deeper insight
        4. Maintains focus on the current topic: {self.current_topic}
        
        Keep your question concise and specific."""
        
        response = self.llm.invoke(prompt)
        
        # Store the follow-up question in conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response.content
        })
        
        return response.content

    def process_teacher_response(self, teacher_response: str) -> str:
        """
        Process teacher's response with guardrails check for both input and output
        
        :param teacher_response: Teacher's input response
        :return: Student's next question or guardrails rejection message
        """
        # Initialize Nemo Guardrails
        rails = LLMRails(RailsConfig.from_path("./config_output_rails"))
        
        # Check input message against guardrails
        input_guardrail_response = rails.generate(messages=[{
            "role": "user",
            "content": teacher_response
        }])
        
        # Get the input response content
        if isinstance(input_guardrail_response, dict):
            input_response_content = input_guardrail_response.get('content', "I'm sorry, I can't respond to that.")
        else:
            input_response_content = str(input_guardrail_response)
        
        # If input guardrails blocked the message, store and return the rejection
        if input_response_content == "I'm sorry, I can't respond to that.":
            reject_response = "It seems you are talking about something not covered in the research paper. Could you please focus on the topics discussed in the research paper"
            self.conversation_history.append({
                "role": "assistant",
                "content": reject_response
            })
            return reject_response
            
        # Store teacher's response if it passes guardrails
        self.conversation_history.append({
            "role": "user",
            "content": teacher_response
        })
        
        # Check if we should move to next topic
        if len(self.conversation_history) >= 6:  # After ~3 exchanges about current topic
            current_index = self.topics.index(self.current_topic)
            if current_index < len(self.topics) - 1:
                self.current_topic = self.topics[current_index + 1]
                next_question = self.generate_initial_question()
                
                # Check output against guardrails
                output_guardrail_response = rails.generate(messages=[{
                    "role": "assistant",
                    "content": next_question
                }])
                
                if isinstance(output_guardrail_response, dict):
                    output_response_content = output_guardrail_response.get('content', "I'm sorry, I can't respond to that.")
                else:
                    output_response_content = str(output_guardrail_response)
                
                if output_response_content == "I'm sorry, I can't respond to that.":
                    return "I apologize, but I need to reformulate my question. Could we continue discussing the current topic?"
                    
                return next_question
        
        # Generate follow-up question
        follow_up = self.generate_follow_up_question(teacher_response)
        
        # Check output against guardrails
        output_guardrail_response = rails.generate(messages=[{
            "role": "assistant",
            "content": follow_up
        }])
        
        # Get the output response content
        if isinstance(output_guardrail_response, dict):
            output_response_content = output_guardrail_response.get('content', "I'm sorry, I can't respond to that.")
        else:
            output_response_content = str(output_guardrail_response)
        
        # If output violates guardrails, return a reformulated question
        if output_response_content == "I'm sorry, I can't respond to that.":
            return "I apologize, but I need to reformulate my question. Could we continue discussing the current topic?"
        
        return follow_up

    def save_session(self):
        """Save current session to the sessions file"""
        session_data = {
            "session_id": self.session_id,
            "start_time": self.session_start_time,
            "end_time": datetime.now().isoformat(),
            "current_topic": self.current_topic,
            "messages": self.conversation_history,
            "context_examples": [
                doc.page_content 
                for msg in self.conversation_history 
                if msg["role"] == "user"
                for doc in self.vectorstore.similarity_search(msg["content"], k=1)
            ]
        }

        # Load existing sessions or create new file
        try:
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            sessions = []

        # Add new session
        sessions.append(session_data)

        # Save updated sessions
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=4)

        return session_data

    def clear_conversation(self):
        """Clear conversation history and start new session"""
        # Save current session if there are messages
        if self.conversation_history:
            self.save_session()
        
        # Reset conversation and session
        self.conversation_history = []
        self.current_topic = None
        self.session_start_time = datetime.now().isoformat()
        self.session_id = hashlib.md5(f"{self.session_start_time}".encode()).hexdigest()[:10]

def main():
    # Example usage
    document_path = 'arxiv.pdf'  # Your knowledge base document
    assistant = RAGAssistant(
        document_path,
        model_name="gpt-3.5-turbo"
    )
    
    print("AI Student Assistant initialized!")
    print("Starting conversation about the research paper...")
    
    # Generate initial question
    initial_question = assistant.generate_initial_question()
    print("\nStudent:", initial_question)
    
    try:
        while True:
            teacher_input = input("\nTeacher: ").strip()
            
            if teacher_input.lower() == 'quit':
                session_data = assistant.save_session()
                print(f"\nSession saved! Session ID: {session_data['session_id']}")
                print(f"Session file: {assistant.sessions_file}")
                break
            elif teacher_input.lower() == 'clear':
                assistant.clear_conversation()
                print("Conversation cleared! New session started.")
                initial_question = assistant.generate_initial_question()
                print("\nStudent:", initial_question)
                continue
            
            next_question = assistant.process_teacher_response(teacher_input)
            print("\nStudent:", next_question)
    
    except KeyboardInterrupt:
        session_data = assistant.save_session()
        print(f"\nSession saved! Session ID: {session_data['session_id']}")
        print(f"Session file: {assistant.sessions_file}")

if __name__ == "__main__":
    main()