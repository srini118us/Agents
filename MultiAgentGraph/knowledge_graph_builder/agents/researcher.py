from helpers.serpapi_tool import google_search
from helpers.wikipedia_tool import search_wikipedia

def research_topic(topic):
    """Fetches information about a topic from Google and Wikipedia."""
    try:
        google_data = google_search(topic)

        # Check if 'organic_results' exists and is non-empty
        organic_results = google_data.get('organic_results', [])
        if not organic_results:
            snippet = "No search results found on Google."
        else:
            snippet = organic_results[0].get('snippet', "No snippet available.")

        wiki_data = search_wikipedia(topic) or "No Wikipedia data found."

        return f"{snippet}\n\n{wiki_data}"

    except Exception as e:
        return f"An error occurred during research: {str(e)}"

