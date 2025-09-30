import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List models
models = genai.list_models()

for m in models:
    print(f"Name: {m.name}")
    print("-" * 30)
