from typing import Optional, Dict, Any, List, Union
import requests
from datetime import datetime

class SocialAPIError(Exception):
    """Custom exception for Social API errors"""
    pass

class LunarCrush:
    """LunarCrush API client for social and market data"""
    
    BASE_URL = "https://lunarcrush.com/api4/public"
    
    def __init__(self, api_key: str):
        """
        Initialize LunarCrush API client.
        
        Args:
            api_key (str): Your LunarCrush API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the LunarCrush API.
        
        Args:
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            
        Returns:
            dict: API response data
            
        Raises:
            SocialAPIError: If the API request fails
        """
        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SocialAPIError(f"LunarCrush API request failed: {str(e)}")

    def get_coin_data(self, coin: str) -> Dict[str, Any]:
        """
        Get market data for a specific coin.

        Args:
            coin (str): Numeric ID or symbol of the coin

        Returns:
            dict: Market data including:
                - id (int): Unique identifier of the coin
                - name (str): Name of the coin
                - symbol (str): Trading symbol
                - price (float): Current price in USD
                - price_btc (float): Price in BTC
                - market_cap (float): Market capitalization in USD
                And other market metrics

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/coins/{coin}/v1")["data"]

    def get_coin_metadata(self, coin: str) -> Dict[str, Any]:
        """
        Get meta information for a cryptocurrency project.

        Args:
            coin (str): Numeric ID or symbol of the coin

        Returns:
            dict: Project metadata including:
                - id (int): Unique identifier of the coin
                - name (str): Name of the coin
                - symbol (str): Trading symbol
                - market_categories (str): Market category classifications
                - blockchain (list): List of blockchain networks where the asset exists
                - description (str): Detailed project description
                - social links and other metadata

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/coins/{coin}/meta/v1")["data"]

    def get_nft_data(self, nft: str) -> Dict[str, Any]:
        """
        Get market data for an NFT collection.

        Args:
            nft (str): Numeric ID or slug of the NFT collection

        Returns:
            dict: NFT market data including:
                - id (int): Unique identifier of the NFT collection
                - name (str): Name of the NFT collection
                - floor_price (float): Current floor price in ETH
                - market_cap (float): Market capitalization
                - percent_change_24h (float): 24-hour price change percentage
                - volume_24h (float): 24-hour trading volume

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/nfts/{nft}/v1")["data"]

    def get_topic_news(self, topic: str) -> Dict[str, Any]:
        """
        Get the top news posts for a social topic.

        Args:
            topic (str): Topic identifier (can include letters, numbers, spaces, #, and $)

        Returns:
            dict: List of news articles including:
                - id (str): LunarCrush internal ID
                - post_type (str): Type of social post
                - post_title (str): Article title
                - post_link (str): URL to article
                - post_sentiment (float): Sentiment score (1-5)
                And other article metadata

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/topic/{topic}/news/v1")["data"]

    def get_coins_list(self) -> List[Dict[str, Any]]:
        """
        Get a list of all tracked coins with their market data.

        Returns:
            list: List of coins including:
                - id (int): LunarCrush internal ID
                - symbol (str): Trading symbol
                - name (str): Full name of the asset
                - price (float): Current price in USD
                - price_btc (float): Price in BTC
                - volume_24h (float): 24-hour volume
                - market_cap (float): Market capitalization
                - galaxy_score (int): LunarCrush Galaxy Score™
                And other market and social metrics

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get("/coins/list/v1")["data"]

    def get_topic_summary(self, topic: str) -> Dict[str, Any]:
        """
        Get summary information for a social topic.

        Args:
            topic (str): Topic identifier to get summary for

        Returns:
            dict: Topic summary including:
                - topic (str): Topic identifier
                - title (str): Display title
                - topic_rank (int): Topic ranking
                - related_topics (list): Related topic identifiers
                - interactions_24h (int): Total interactions last 24h
                - num_contributors (int): Number of unique contributors
                And detailed engagement metrics by content type

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/topic/{topic}/v1")["data"]


class CryptoPanic:
    """CryptoPanic API client for crypto news and media monitoring"""
    
    BASE_URL = "https://cryptopanic.com/api/v1"
    
    def __init__(self, auth_token: str):
        """
        Initialize CryptoPanic API client.
        
        Args:
            auth_token (str): Your CryptoPanic API authentication token
        """
        self.auth_token = auth_token
        self.session = requests.Session()

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the CryptoPanic API.
        
        Args:
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            
        Returns:
            dict: API response data
            
        Raises:
            SocialAPIError: If the API request fails
        """
        # Add auth token to params
        if params is None:
            params = {}
        params['auth_token'] = self.auth_token

        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SocialAPIError(f"CryptoPanic API request failed: {str(e)}")

    def get_posts(
        self,
        public: bool = False,
        filter: Optional[str] = None,
        currencies: Optional[str] = None,
        regions: Optional[str] = None,
        kind: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get news and media posts with various filtering options.

        Args:
            public (bool, optional): Filter by public posts only (default: False)
            filter (str, optional): Post filter type (rising|hot|bullish|bearish|important|saved|lol)
            currencies (str, optional): Comma-separated list of currency codes (max 50, e.g., 'BTC,ETH')
            regions (str, optional): Comma-separated list of region codes 
                (en,de,nl,es,fr,it,pt,ru,tr,ar,cn,jp,ko) (default: en)
            kind (str, optional): Content type filter (news|media)

        Returns:
            dict: Response containing:
                - count (int): Total number of results
                - next (str): URL for next page
                - previous (str): URL for previous page
                - results (list): Array of posts with:
                    - kind (str): Post type (news/media)
                    - title (str): Post title
                    - published_at (str): Publication timestamp
                    - url (str): Source URL
                    - currencies (list): Related cryptocurrencies
                    - votes (dict): User voting data
                    - metadata (dict): Additional post metadata

        Raises:
            SocialAPIError: If the API request fails
        """
        params = {
            'public': 'true' if public else 'false',
            'filter': filter,
            'currencies': currencies,
            'regions': regions,
            'kind': kind
        }
        params = {k: v for k, v in params.items() if v is not None}
        
        return self._get("/posts/", params)
