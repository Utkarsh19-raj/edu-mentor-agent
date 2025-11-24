# config.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Support both GEMINI_API_KEY and GOOGLE_API_KEY names
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "❌ No API key found. Please create a .env file with GEMINI_API_KEY=your_key_here"
    )

# Configure Gemini client
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"


def get_model():
    """
    Returns a configured GenerativeModel instance.
    """
    return genai.GenerativeModel(MODEL_NAME)
