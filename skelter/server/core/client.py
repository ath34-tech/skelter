import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_groq import ChatGroq

def get_client():
    env_path = Path(".env")
    if not env_path.exists():
        parent_env = Path(__file__).parent.parent.parent / ".env"
        if parent_env.exists():
            env_path = parent_env
    
    load_dotenv(env_path)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Don't raise error immediately on import, allow 'config' command to run
        return None

    return ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

# Lazy client initialization
_client = None

def invoke_client(prompt):
    global _client
    if _client is None:
        _client = get_client()
    if _client is None:
        raise ValueError("GROQ_API_KEY is not set. Run 'skelter config --key YOUR_KEY' first.")
    return _client.invoke(prompt)