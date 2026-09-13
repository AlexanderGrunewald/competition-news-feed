import json
import os
from tavily import TavilyClient
from time import time


class CompetitorSearchEngine(TavilyClient):
    VALID_SEARCH_PARAMS = {
        "search_depth",
        "topic",
        "time_range",
        "start_date",
        "end_date",
        "max_results",
        "include_images",
        "include_answer",
        "include_raw_content",
        "include_domains",
        "exclude_domains",
        "exact_match",
    }

    def __init__(self, api_key: str | None = None):
        resolved_key = api_key or os.environ.get("TAVILY_API_KEY")
        if not resolved_key:
            raise ValueError(
                "API key must be provided or set as TAVILY_API_KEY in the environment."
            )
        super().__init__(api_key=resolved_key)

    def monitor_competitor(
            self,
            competitor: str,
            category: str = "accessories",
            custom_query: str | None = None,
            **kwargs,
        ) -> dict:
            query = custom_query or f'"{competitor}" new power tool {category}'

            search_payload = {
                "query": query,
                "exact_match": True,
                "time_range": "y",
                "search_depth": "advanced",
                "max_results": 10,
            }

            filtered_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k in self.VALID_SEARCH_PARAMS and v is not None
            }
            # If start date or end date is specified, the client does not take time_range as an argument
            if "stat_date" in filtered_kwargs or "end_date" in filtered_kwargs:
                del search_payload["time_range"]

            search_payload.update(filtered_kwargs)

            return self.search(**search_payload)
    
    def save_results(self, data: dict, filename: str = "competitor_intel.json"):
        """Utility to write search results cleanly to disk."""
        todays_date = time.now().strftime("%Y-%m-%d %H:%M")
        with open(f"{filename}_{todays_date}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# Usage:
engine = CompetitorSearchEngine()
results = engine.monitor_competitor("Makita", category="accessories")

print(f"Results found: {len(results.get('results', []))}")
engine.save_results(results, "makita_accessories.json")
