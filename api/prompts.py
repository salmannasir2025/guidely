from . import llm, search

LANGUAGE_MAP = {
    "en-US": "English",
    "ur-PK": "Urdu",
    "pa-PK": "Pakistani Punjabi (Shahmukhi script)",
    "ps-PK": "Pashto",
    "sd-PK": "Sindhi"
}

PROMPT_TEMPLATES = {
    "physics": "You are an expert physics tutor. Using the following information: '{search_context}', provide a clear and detailed explanation for the user's question: '{query}'. If there are formulas, explain each variable and its units.{language_instruction}",
    "chemistry": "You are an expert chemistry tutor. Based on this information: '{search_context}', answer the user's question: '{query}'. If there are chemical equations, ensure they are balanced and explain the reaction.{language_instruction}",
    "programming": "You are a friendly programming tutor. Explain the concept in simple terms based on the following information: '{search_context}'. Answer the user's question: '{query}'. If you provide code examples, explain each line clearly.{language_instruction}",
    "ai_concepts": "You are an AI expert who is great at teaching. Using the following information: '{search_context}', explain the concept to a beginner. Use analogies and simple, real-world examples to answer the user's question: '{query}'.{language_instruction}",
    "digital_marketing": "You are a digital marketing expert. Based on the following information: '{search_context}', provide a clear, practical, and easy-to-understand answer to the user's question: '{query}'.{language_instruction}",
    "general_knowledge": "Based on the following information: '{search_context}'. Answer the user's question: '{query}'. Synthesize a comprehensive answer from the provided text.{language_instruction}",
    "no_context": "{query}{language_instruction}"
}

def get_rag_prompt(category: str, search_context: str, query: str, language: str) -> str:
    """Constructs a prompt for the RAG workflow based on the category."""
    language_name = LANGUAGE_MAP.get(language, "English")
    language_instruction = f" Respond in {language_name}."

    # Use the specific category template if it exists to preserve the persona.
    # Otherwise, decide whether to use a general context-based prompt or no-context prompt.
    template_key = category if category in PROMPT_TEMPLATES else ("general_knowledge" if search_context else "no_context")

    template = PROMPT_TEMPLATES[template_key]

    return template.format(search_context=search_context, query=query, language_instruction=language_instruction)