from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).parent

CONTEXT_FILE = BASE_DIR / "context.txt"
PROMPT_FILE = BASE_DIR / "prompt.txt"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
