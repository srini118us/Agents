import requests

def search_wikipedia(topic):
    response = requests.get(
        f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", f"No summary found for {topic}.")
    else:
        return f"No Wikipedia page found for {topic}."