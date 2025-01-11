import os
import pandas as pd
from ragas import EvaluationDataset
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas.metrics import RubricsScore
from ragas.dataset_schema import SingleTurnSample
from ragas import evaluate
import asyncio
import json
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
def create_conversation_samples(conversation_data: Dict) -> List[SingleTurnSample]:
    """Create samples for each turn in a conversation."""
    samples = []
    messages = conversation_data['messages']
    
    # Filter out system messages and pair assistant questions with user responses
    conversation_turns = []
    
    try:
        # Print debugging information
        print(f"\nProcessing conversation: {conversation_data['topic']}")
        print(f"Number of messages: {len(messages)}")
        
        for i in range(len(messages)):
            if messages[i]['role'] == 'assistant' and i + 1 < len(messages) and messages[i + 1]['role'] == 'user':
                conversation_turns.append((messages[i], messages[i+1]))
        
        print(f"Number of valid turns found: {len(conversation_turns)}")
        
        for question_msg, answer_msg in conversation_turns:
            sample = SingleTurnSample(
                user_input=question_msg['content'],
                retrieved_contexts=[conversation_data['context']],
                response=answer_msg['content']
            )
            samples.append(sample)
            
    except Exception as e:
        print(f"Error processing conversation {conversation_data.get('topic', 'unknown')}: {str(e)}")
    
    return samples

def load_conversations(json_data: List[Dict]) -> Dict[str, List[SingleTurnSample]]:
    """Load all conversations and organize them by topic."""
    conversations = {}
    for conversation in json_data:
        topic = conversation['topic']
        if topic not in conversations:
            conversations[topic] = []
        samples = create_conversation_samples(conversation)
        if samples:  # Only add if we got valid samples
            conversations[topic].extend(samples)
        else:
            print(f"Warning: No valid samples extracted for topic: {topic}")
    
    # Print summary of loaded conversations
    print("\nLoaded conversations summary:")
    for topic, samples in conversations.items():
        print(f"{topic}: {len(samples)} turns")
    
    return conversations

async def evaluate_conversation(samples: List[SingleTurnSample]) -> Tuple[List[float], bool]:
    """Evaluate all turns in a conversation."""
    scores = []
    success = False
    
    try:
        for i, sample in enumerate(samples, 1):
            score = await rubric_metric.single_turn_ascore(sample)
            print(f"\nTurn {i}:")
            print(f"Question: {sample.user_input[:150]}...")
            print(f"Response excerpt: {sample.response[:150]}...")
            print(f"Score: {score}")
            scores.append(score)
        success = True
    except Exception as e:
        print(f"Error during conversation evaluation: {str(e)}")
    
    return scores, success

async def evaluate_all_conversations(conversations: Dict[str, List[SingleTurnSample]]):
    """Evaluate all conversations and calculate normalized scores."""
    results = []
    
    for topic, samples in conversations.items():
        print(f"\n=== Evaluating conversation: {topic} ===")
        
        if not samples:
            print(f"Skipping {topic} - no valid samples")
            continue
            
        try:
            scores, success = await evaluate_conversation(samples)
            
            if success and scores:  # Only process if we have valid scores
                avg_score = sum(scores) / len(scores)
                
                result = {
                    'topic': topic,
                    'num_turns': len(samples),
                    'individual_scores': scores,
                    'normalized_score': avg_score
                }
                results.append(result)
                
                print(f"\nSummary for {topic}:")
                print(f"Number of turns: {len(samples)}")
                print(f"Individual scores: {scores}")
                print(f"Normalized score: {avg_score:.2f}")
            else:
                print(f"Warning: No valid scores for topic: {topic}")
                
        except Exception as e:
            print(f"Error processing topic {topic}: {str(e)}")
            continue
    
    return results

# Initialize the evaluator and metric (moved outside main for clarity)
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4"))
rubric_metric = RubricsScore(
    name="explanatory_depth",
    llm=evaluator_llm,
    rubrics={
        "score1_description": "The response is superficial, lacks detail, and fails to adequately explain the concepts. There is minimal elaboration on key points and no clear structure to the explanation.",
        "score2_description": "The response provides basic explanations but lacks depth in critical areas. Some concepts are explained but without sufficient detail or real-world connections. The structure is basic and some key points are missing.",
        "score3_description": "The response offers clear explanations with moderate depth. Most key concepts are covered with some supporting details and examples. The explanation has a logical structure but could benefit from more elaborate connections or practical applications.",
        "score4_description": "The response provides comprehensive explanations with good depth. Concepts are well-explained with relevant examples and clear connections. The explanation is well-structured and includes practical applications or implications.",
        "score5_description": "The response demonstrates exceptional explanatory depth with thorough, nuanced explanations. Complex concepts are broken down effectively with rich examples, clear analogies, and practical applications. The explanation is exceptionally well-structured with clear transitions and connections between ideas."
    }
)

# Main execution
if __name__ == "__main__":
    try:
        # Load your JSON data (same as before)
        with open('advanced_rag_dataset.json', 'r') as f:
            json_data = json.load(f)
        
        # Process conversations
        print("Loading conversations...")
        conversations = load_conversations(json_data)
        
        if not conversations:
            print("Error: No valid conversations loaded")
            exit(1)
            
        # Run evaluation
        print("\nStarting evaluation...")
        results = asyncio.run(evaluate_all_conversations(conversations))
        
        if not results:
            print("Error: No valid results generated")
            exit(1)
            
        # Convert results to DataFrame for better visualization
        df_results = pd.DataFrame(results)
        print("\nFinal Results:")
        print(df_results[['topic', 'num_turns', 'normalized_score']])
        
        # Save results to CSV
        df_results.to_csv('conversation_evaluation_results.csv', index=False)
        print("\nResults have been saved to 'conversation_evaluation_results.csv'")
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        raise