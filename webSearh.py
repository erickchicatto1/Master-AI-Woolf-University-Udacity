import os
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from tavily import TavilyClient

from lib.agents import Agent
from lib.messages import BaseMessage
from lib.tooling import tool

load_dotenv()

@tool
def web_search(query: str, search_depth: str = "advanced") -> Dict:
    """
    Search the web using Tavily API
    args:
        query (str): Search query
        search_depth (str): Type of search - 'basic' or 'advanced' (default: advanced)
    """
    api_key = os.getenv("TAVILY_API_KEY")
    client = TavilyClient(api_key=api_key)
    
    # Perform the search
    search_result = client.search(
        query=query,
        search_depth=search_depth,
        include_answer=True,
        include_raw_content=False,
        include_images=False
    )
    
    # Format the results
    formatted_results = {
        "answer": search_result.get("answer", ""),
        "results": search_result.get("results", []),
        "search_metadata": {
            "timestamp": datetime.now().isoformat(),
            "query": query
        }
    }
    
    return formatted_results
