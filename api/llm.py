from .config import settings
import google.generativeai as genai
from .cache import redis_cache
import logging
from fastapi.concurrency import run_in_threadpool
from .prompts import PROMPT_TEMPLATES

# Define the model at the module level, but it will be configured on app startup.
model = genai.GenerativeModel("gemini-pro")


def initialize_llm():
    """Configures the Gemini API client with the API key from settings."""
    logging.info("Initializing Gemini API client...")
    genai.configure(api_key=settings.gemini_api_key)
    logging.info("Gemini API client initialized successfully.")


class LLMError(Exception):
    """Custom exception for errors related to the Language Model API."""

    pass


def get_llm_explanation(prompt: str) -> str:
    """
    Gets a response from the Gemini LLM.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(
            "Error calling Gemini API for explanation.",
            extra={"prompt_start": prompt[:100], "error": str(e)},
        )
        raise LLMError("Error generating response from the language model.") from e


async def get_llm_explanation_stream(prompt: str):
    """
    Gets a streaming response from the Gemini LLM.
    Yields chunks of text as they are received.
    """
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        logging.error(
            "Error calling Gemini API stream.",
            extra={"prompt_start": prompt[:100], "error": str(e)},
        )
        raise LLMError("Error generating response from the language model.") from e


@redis_cache(ttl=86400)  # Cache classifications for 24 hours
async def classify_query(query: str) -> str:
    """
    Uses the LLM to classify a query into a predefined category.
    """
    prompt = f"""You are a classification agent. Your only job is to classify the user's query into one of the following categories based on its content: [math, physics, chemistry, programming, ai_concepts, digital_marketing, general_knowledge].

- "math": Use for questions that require calculation, solving algebraic expressions, trigonometry, or calculus. Examples: "What is 5*5?", "solve for x in 2x + 5 = 10".
- "physics": Use for questions about motion, forces, energy, electricity, magnetism, and other physics concepts. Examples: "What is Newton's second law?", "Calculate the kinetic energy of a 5kg object moving at 2m/s".
- "chemistry": Use for questions about chemical reactions, elements, the periodic table, molecules, and chemical formulas. Examples: "What is the chemical formula for water?", "Balance the equation H2 + O2 -> H2O".
- "programming": Use for questions about coding, algorithms, data structures, or specific programming languages like Python, JavaScript, etc. Examples: "How does a for loop work in Python?", "What is an API?".
- "ai_concepts": Use for questions about artificial intelligence, machine learning, neural networks, or large language models. Examples: "What is machine learning?", "Explain how ChatGPT works".
- "digital_marketing": Use for questions about SEO, social media marketing, content marketing, or online advertising. Examples: "What is SEO?", "How to create a social media campaign?".
- "general_knowledge": Use for questions about facts, history, biology, english, people, or any other topic that is not covered by the other categories. Examples: "Who was the first president of the USA?", "What is the capital of Pakistan?".

Respond with a single word from the list of categories. Do not add any explanation or punctuation.

User Query: "{query}"
Classification:"""

    def _classify():
        try:
            response = model.generate_content(prompt)
            category = response.text.strip().lower()
            valid_categories = list(PROMPT_TEMPLATES.keys())
            if category in valid_categories:
                return category
            logging.warning(
                f"LLM classification returned an unexpected value: '{category}'. Defaulting to 'general_knowledge'."
            )
            return "general_knowledge"
        except Exception as e:
            logging.error(
                "Error during LLM classification.",
                extra={"query": query, "error": str(e)},
            )
            return "general_knowledge"

    return await run_in_threadpool(_classify)


@redis_cache(ttl=86400)  # Cache translations for 24 hours
async def translate_text(text: str, target_language: str, source_language: str) -> str:
    """
    Uses the LLM to translate text from a source language to a target language.
    """
    prompt = f"Translate the following text from {source_language} to {target_language}. Provide only the translated text, with no additional commentary or labels.\n\nText to translate:\n---\n{text}\n---"

    def _translate():
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logging.error(
                "Error during LLM translation.",
                extra={"target_language": target_language, "error": str(e)},
            )
            raise LLMError("Error translating text.") from e

    return await run_in_threadpool(_translate)


def check_llm_client() -> bool:
    """Checks if the LLM model client is initialized."""
    return model is not None
