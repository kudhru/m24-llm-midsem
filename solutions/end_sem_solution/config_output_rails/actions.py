
from typing import Optional

from nemoguardrails.actions import action

@action(is_system_action=True)
async def check_blocked_terms(context: Optional[dict] = None):
    bot_response = context.get("bot_message")

    # A quick hard-coded list of proprietary terms. You can also read this from a file.
    proprietary_terms = [
        "confidential",
        "proprietary",
        "secret",
        "classified",
        "internal only",
        "restricted",
        "Merge Sort"
    ]

    for term in proprietary_terms:
        if term in bot_response.lower():
            return True

    return False
from typing import Optional
from nemoguardrails.actions import action
import difflib

@action(is_system_action=True)
async def verify_knowledge_base_alignment(context: Optional[dict] = None):
    """
    Verifies if the bot's response aligns with the provided knowledge base context.
    Returns True if the response should be blocked (doesn't align with context).
    """
    bot_response = context.get("bot_message", "").lower()
    knowledge_context = context.get("relevant_context", "").lower()
    
    # If no context is available, be conservative and block
    if not knowledge_context.strip():
        return True
        
    # Simple verification using sequence matcher
    matcher = difflib.SequenceMatcher(None, knowledge_context, bot_response)
    
    # Calculate similarity ratio
    similarity = matcher.ratio()
    
    # If similarity is too low, block the response
    # You can adjust this threshold based on your needs
    if similarity < 0.3:  # 30% similarity threshold
        return True
        
    return False