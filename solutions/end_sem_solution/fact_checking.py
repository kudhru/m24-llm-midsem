import os
import pandas as pd
import json
from ragas import EvaluationDataset
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas.metrics import AspectCritic
from ragas.dataset_schema import SingleTurnSample
from ragas import evaluate
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_conversation_samples(conversation_data: Dict) -> List[SingleTurnSample]:
    """Create samples for each turn in a conversation."""
    samples = []
    messages = conversation_data['messages']
    conversation_turns = []
    
    for i in range(len(messages)):
        if messages[i]['role'] == 'assistant' and i + 1 < len(messages) and messages[i + 1]['role'] == 'user':
            conversation_turns.append((messages[i], messages[i+1]))
    
    for question_msg, answer_msg in conversation_turns:
        sample = SingleTurnSample(
            user_input=question_msg['content'],
            retrieved_contexts=[conversation_data['context']],
            response=answer_msg['content']
        )
        samples.append(sample)
    
    return samples

def evaluate_samples(json_data: List[Dict]) -> pd.DataFrame:
    """Evaluate all samples using AspectCritic."""
    # Initialize critics
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4"))
    critic = AspectCritic(
        name="correctness",
        definition="Check correctness of the respone wrt to retreived context ",
        llm=evaluator_llm,
    )
    
    all_results = []
    for sample_idx, conversation in enumerate(json_data):
        print(f"\nProcessing sample {sample_idx + 1}/{len(json_data)}: {conversation['topic']}")
        
        # Get turns for this sample
        turns = create_conversation_samples(conversation)
        if not turns:
            continue
            
        # Create evaluation dataset for this sample
        eval_dataset = EvaluationDataset(turns)
        
        # Evaluate all turns
        results = evaluate(eval_dataset, metrics=[critic])
        results_df = results.to_pandas()
        
        # Calculate average score for this sample
        avg_score = results_df['correctness'].mean()
        
        # Store results
        result = {
            'sample_id': sample_idx + 1,
            'topic': conversation['topic'],
            'num_turns': len(turns),
            'turn_scores': results_df['correctness'].tolist(),
            'average_score': avg_score
        }
        all_results.append(result)
        
        print(f"Sample {sample_idx + 1} results:")
        print(f"Number of turns: {len(turns)}")
        print(f"Turn scores: {result['turn_scores']}")
        print(f"Average score: {avg_score:.2f}")
    
    return pd.DataFrame(all_results)

if __name__ == "__main__":
    try:
        # Load dataset
        print("Loading dataset...")
        with open('advanced_rag_dataset.json', 'r') as f:
            json_data = json.load(f)
        
        # Run evaluation
        results_df = evaluate_samples(json_data)
        
        # Calculate overall statistics
        overall_avg = results_df['average_score'].mean()
        
        # Save detailed results
        results_df.to_csv('aspect_critic_results.csv', index=False)
        
        # Print summary
        print("\nEvaluation Summary:")
        print(f"Number of samples evaluated: {len(results_df)}")
        print(f"Overall average score: {overall_avg:.2f}")
        
        # Print per-sample results
        print("\nPer-sample results:")
        print(results_df[['sample_id', 'topic', 'num_turns', 'average_score']])
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        raise