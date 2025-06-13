import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def google_search(query):
    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERP_API_KEY, "engine": "google"}
    response = requests.get(url, params=params)
    return response.json()