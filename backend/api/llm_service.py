import os
import logging
from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)


def generate_llm_response(prompt, model_name='gpt-3.5-turbo', temperature=0.7, max_tokens=500, 
                          top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    try:
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            logger.error("OPENAI_API_KEY is not configured")
            raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY environment variable.")
        
        # Log API key prefix for debugging
        logger.info(f"Attempting API call with key starting: {api_key[:15]}...")
        
        client = OpenAI(
            api_key=api_key,
            max_retries=2,
            timeout=30.0
        )
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating LLM response: {type(e).__name__}: {str(e)}", exc_info=True)
        raise


def generate_two_responses(prompt, model_name='gpt-3.5-turbo', 
                          temperature_a=0.7, max_tokens_a=500, top_p_a=1.0, 
                          frequency_penalty_a=0.0, presence_penalty_a=0.0,
                          temperature_b=0.9, max_tokens_b=500, top_p_b=1.0,
                          frequency_penalty_b=0.0, presence_penalty_b=0.0):
    response_a = generate_llm_response(
        prompt, model_name, temperature_a, max_tokens_a, 
        top_p_a, frequency_penalty_a, presence_penalty_a
    )
    
    response_b = generate_llm_response(
        prompt, model_name, temperature_b, max_tokens_b,
        top_p_b, frequency_penalty_b, presence_penalty_b
    )
    
    return response_a, response_b
