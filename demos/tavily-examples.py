from tavily import TavilyClient
import os
from rich import print

tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
response = tavily_client.search("Who is Leo Messi?")

print(response)

