import pytest
from api.prompts import get_rag_prompt

@pytest.mark.parametrize(
    "category, search_context, query, language, expected_substring",
    [
        # Test with context for a specific category
        ("physics", "F=ma", "Explain Newton's second law", "en-US", "expert physics tutor"),
        # Test with context for a general category
        ("general_knowledge", "The sky is blue.", "Why is the sky blue?", "en-US", "Synthesize a comprehensive answer"),
        # Test with no context
        ("programming", "", "What is a variable?", "en-US", "What is a variable? Respond in English."),
        # Test with a different language
        ("chemistry", "H2O is water", "What is water?", "ur-PK", "expert chemistry tutor"),
        ("chemistry", "H2O is water", "What is water?", "ur-PK", "Respond in Urdu"),
        # Test fallback for unknown category with context
        ("unknown_category", "Some context", "A question", "en-US", "Synthesize a comprehensive answer"),
    ]
)
def test_get_rag_prompt(category, search_context, query, language, expected_substring):
    """
    Tests that get_rag_prompt generates the correct prompt structure
    for various inputs.
    """
    prompt = get_rag_prompt(category, search_context, query, language)
    assert expected_substring in prompt
    assert query in prompt
    if search_context:
        assert search_context in prompt