import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai(prompt, model="gpt-4", max_tokens=2000):
    """
    Call OpenAI API using the new v1.0.0+ format.
    
    Args:
        prompt (str): The prompt to send to the model
        model (str): The model to use (default: "gpt-4")
        max_tokens (int): The maximum number of tokens to generate (default: 2000)
    
    Returns:
        str: The model's response
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"