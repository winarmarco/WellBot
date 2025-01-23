import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please set MISTRAL_API_KEY in your .env file.")
