import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
