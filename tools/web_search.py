import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient
load_dotenv()  # reads keys from .env file

@tool
def web_search(query: str) -> str:
    """Search the web for current information about any topic.
    Input: a plain search query string.
    """
    try:
        client = TavilyClient(api_key="your_tavily_key_here")
        response = client.search(query, max_results=4)
        results = []
        for r in response["results"]:
            results.append(f"Title: {r['title']}\nURL: {r['url']}\nSummary: {r['content']}\n")
        return "\n---\n".join(results)
    except Exception as e:
        return f"Search failed: {str(e)}"
