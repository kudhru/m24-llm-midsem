import os
from ragas import EvaluationDataset
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from ragas.metrics import AspectCritic
from ragas.dataset_schema import SingleTurnSample
from ragas import evaluate
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Initialize evaluator
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
critic = AspectCritic(
    name="correctness",
    definition="Are the queries grounded in research. compare th queries with the given topic and context",
    llm=evaluator_llm,
)

# Define the samples
samples = [
    {
        "topic": "conclusions",
        "query": "I'm reading through the conclusions section of the report and I'm curious about the overall summary of the study's findings. Could you help me understand what the authors are trying to convey by stating that 'the results indicate a statistically significant correlation between [variable 1] and [variable 2]'?",
        "context": """of time, we asked them open-ended questions. We first asked them to comment on EvalGen's approach to generating assertions, and whether they felt that the assertions aligned with their grades. We then asked follow-up questions to learn more about why they felt a particular way or found some aspect of assertion alignment challenging. We limited the post-interview to 10 minutes. At the end, we asked participants to rate how they felt about the assertions' Participants really liked viewing the table of assertion results on all LLM outputs, with all participants expressing interest upon first viewing it (Figure 3)—but they verified the results differently."""
    },
    {
        "topic": "experiments",
        "query": "I'm reading through the experiments section of the report and I'm curious about the different methods used to collect data for the study. Could you help me understand how the researchers ensured that their experimental design minimized external biases and maximized internal validity?",
        "context": """call, rather than code), which happened rarely. (5) Grading more outputs: Participants graded outputs while EvalGen generated and evaluated different candidate assertions. Some participants graded continuously for up to 10 minutes; others stopped after 10 grades. (6) Understanding alignment on graded outputs: Participants viewed the "Report Card" screen"""
    },
    {
        "topic": "proposed_methodology",
        "query": "I'm reading through the proposed methodology section of the report and I'm curious about how the researchers plan to ensure the reliability and validity of their data collection methods.",
        "context": """down" grades. After grading, both participants clicked the button to auto-generate criteria. (4) Refining criteria: After receiving criteria suggestions from EvalGen, participants removed some suggestions and added 1-2 criteria of their own."""
    },
    {
        "topic": "problem_statement",
        "query": "I'm reading through the problem statement section of the report and I'm curious about what specific issues are being addressed.",
        "context": """use of their time. The participant who did not agree said that they would find it useful if, on the grading screen, EvalGen showed what it was doing with the grades. However, three participants found it difficult to enumerate all criteria in their head and grade against all criteria, wanting EvalGen to prompt them to grade per each criteria (P6, P7, P8)."""
    },
    {
        "topic": "comparison_with_existing_models",
        "query": "I'm reading through the comparison with existing models section of the report and I'm curious about how the new model's performance compares to the industry benchmark model.",
        "context": """Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences REFERENCES [1] Ian Arawjo, Chelse Swoopes, Priyan Vaithilingam, Martin Wattenberg, and Elena Glassman. 2023. ChainForge: A Visual Toolkit for Prompt Engineering and LLM Hypothesis Testing."""
    }
]

def evaluate_queries():
    """Evaluate each query for grounding in its context."""
    results = []
    
    for sample in samples:
        # Create evaluation dataset
        eval_sample = SingleTurnSample(
            user_input=sample['query'],
            retrieved_contexts=[sample['context']],
            response="Evaluating query grounding"  # Placeholder response
        )
        eval_dataset = EvaluationDataset([eval_sample])
        
        # Evaluate
        result = evaluate(eval_dataset, metrics=[critic])
        result_df = result.to_pandas()
        
        # Store results
        results.append({
            'topic': sample['topic'],
            'score': result_df['correctness'].iloc[0],
            'query': sample['query'][:100] + "..."  # Truncate for display
        })
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    # Run evaluation
    results_df = evaluate_queries()
    
    # Sort by score (lower scores indicate better grounding)
    results_df = results_df.sort_values('score', ascending=True)
    
    # Calculate consistency metric (higher count = lower consistency)
    inconsistent_count = len(results_df[results_df['score'] > 0.5])
    
    print("\nQuery Grounding Evaluation Results:")
    print(results_df)
    print(f"\nNumber of poorly grounded queries: {inconsistent_count}")
    print(f"Consistency score: {1 - (inconsistent_count/len(results_df)):.2f}")