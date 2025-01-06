"""
Search1API MCP Server implementation
"""
import os
import logging
import json
import requests
from typing import Optional, Dict, Any, List
from mcp import Server, Tool, Resource

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='search1api_server.log'
)
logger = logging.getLogger(__name__)

class Search1APIServer(Server):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('SEARCH1API_KEY')
        if not self.api_key:
            raise ValueError("SEARCH1API_KEY environment variable is required")
        
        self.base_url = "https://www.search1api.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make request to Search1API with error handling"""
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise RuntimeError(f"Search1API request failed: {str(e)}")

    @Tool()
    def search(self, query: str, max_results: int = 10, search_service: str = "google") -> Dict[str, Any]:
        """
        Search the web using Search1API
        
        Args:
            query: Search query
            max_results: Number of results to return (default: 10)
            search_service: Search service to use (default: "google")
        """
        params = {
            "q": query,
            "num": max_results,
            "engine": search_service
        }
        return self._make_request("search", params)

    @Tool()
    def news(self, query: str, max_results: int = 10, search_service: str = "google") -> Dict[str, Any]:
        """
        Search for news articles using Search1API
        
        Args:
            query: Search query
            max_results: Number of results to return (default: 10)
            search_service: Search service to use (default: "google")
        """
        params = {
            "q": query,
            "num": max_results,
            "engine": search_service,
            "type": "news"
        }
        return self._make_request("news", params)

    @Tool()
    def crawl(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a URL using Search1API
        
        Args:
            url: URL to crawl
        """
        params = {"url": url}
        return self._make_request("crawl", params)

    @Tool()
    def sitemap(self, url: str) -> Dict[str, Any]:
        """
        Get all related links from a URL
        
        Args:
            url: URL to get sitemap
        """
        params = {"url": url}
        return self._make_request("sitemap", params)

def main():
    """Run the Search1API MCP server"""
    try:
        server = Search1APIServer()
        server.run()
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")
        raise