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
                - volume_24h (float): Volume in USD for 24 hours
                - volatility (float): Standard deviation of price
                - circulating_supply (float): Number of coins actively available
                - max_supply (float): Maximum supply of the coin
                - percent_change_24h (float): 24-hour price change percentage
                - percent_change_7d (float): 7-day price change percentage
                - percent_change_30d (float): 30-day price change percentage
                - market_cap (float): Total market capitalization in USD
                - market_cap_rank (int): Rank by market cap
                - galaxy_score (int): Technical and social indicator score
                - alt_rank (int): Performance score relative to other assets

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/coins/{coin}/v1")

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
                - blockchain (list): List of blockchain networks including:
                    - type (str): Type of blockchain implementation
                    - network (str): Blockchain network name
                    - address (str): Contract address on the network
                    - decimals (int): Token decimals
                - short_summary (str): Brief project description
                - description (str): Detailed project description
                - github_link (str): GitHub repository URL
                - website_link (str): Project website URL
                - whitepaper_link (str): Whitepaper URL
                - twitter_link (str): Twitter profile URL
                - reddit_link (str): Reddit community URL
                - header_image (str): Header image URL
                - header_text (str): Header text description
                - videos (str): Related video URLs
                - coingecko_link (str): CoinGecko profile URL
                - coinmarketcap_link (str): CoinMarketCap profile URL

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/coins/{coin}/meta/v1")

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
                - total_supply (int): Total number of NFTs in collection
                - num_owners (int): Number of unique owners
                - avg_price_24h (float): Average sale price in last 24h
                - highest_sale (float): Highest sale price ever
                - market_cap_rank (int): Rank by market cap
                - volume_rank (int): Rank by trading volume
                - social_volume_24h (int): Number of social mentions
                - twitter_followers (int): Number of Twitter followers
                - discord_members (int): Number of Discord members
                - website_link (str): Collection website URL
                - marketplace_links (list): NFT marketplace URLs

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/nfts/{nft}/v1")

    def get_topic_news(self, topic: str) -> Dict[str, Any]:
        """
        Get the top news posts for a social topic.

        Args:
            topic (str): Topic identifier (can include letters, numbers, spaces, #, and $)

        Returns:
            list: List of news articles including:
                - id (str): LunarCrush internal ID for the article
                - post_type (str): Type of social post
                - post_title (str): Article title
                - post_link (str): URL to view the article
                - post_image (str): URL to the primary image
                - post_created (int): Unix timestamp of creation
                - post_sentiment (float): Sentiment score (1-5)
                - creator_id (str): Unique identifier for creator
                - creator_name (str): Screen name of creator
                - creator_display_name (str): Display name of creator
                - creator_followers (int): Number of creator followers
                - creator_avatar (str): URL to creator's avatar
                - interactions_24h (int): Interactions in last 24 hours
                - interactions_total (int): Total number of interactions
                - source_domain (str): Domain of the news source
                - source_name (str): Name of the news source
                - topics (list): Related topic identifiers
                - assets (list): Related asset symbols

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/topic/{topic}/news/v1")

    def get_coins_list(self) -> List[Dict[str, Any]]:
        """
        Get a list of all tracked coins with their market data.

        Returns:
            list: List of dicts including:
                - id (int): LunarCrush internal ID
                - symbol (str): Trading symbol
                - name (str): Full name of the asset
                - price (float): Current price in USD
                - price_btc (float): Price in BTC
                - volume_24h (float): 24-hour volume in USD
                - market_cap (float): Market capitalization
                - galaxy_score (int): LunarCrush Galaxy Score™
                - alt_rank (int): Relative performance score
                - interactions_24h (int): Social interactions in last 24h
                - social_volume_24h (int): Total posts with interactions
                - social_dominance (float): Percentage of total social volume
                - market_dominance (float): Percentage of total market cap
                - market_cap_rank (int): Market cap ranking
                - percent_change_24h (float): 24h price change percentage
                - volatility (float): Price volatility metric
                - sentiment (float): Weighted sentiment score
                - categories (str): Asset categories
                - blockchains (list): Associated blockchain networks

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get("/coins/list/v1")

    def get_topic_summary(self, topic: str) -> Dict[str, Any]:
        """
        Get summary information for a social topic.

        Args:
            topic (str): Topic identifier to get summary for

        Returns:
            dict: Topic summary including:
                - topic (str): Topic identifier
                - title (str): Display title for the topic
                - topic_rank (int): Ranking of the topic
                - related_topics (list): List of related topic identifiers
                - interactions_24h (int): Total interactions in last 24 hours
                - num_contributors (int): Number of unique contributors
                - num_posts (int): Total number of posts
                - types_count (dict): Count of posts by content type:
                    - tweet (int): Number of tweets
                    - reddit-post (int): Number of Reddit posts
                    - youtube-video (int): Number of YouTube videos
                    - tiktok-video (int): Number of TikTok videos
                    - news (int): Number of news articles
                - types_interactions (dict): Interactions by content type
                - types_sentiment (dict): Sentiment scores by content type
                - types_sentiment_detail (dict): Detailed sentiment breakdown
                - trend (str): Current trend direction (up/down)

        Raises:
            SocialAPIError: If the API request fails
        """
        return self._get(f"/topic/{topic}/v1")


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
                    - votes (dict): User voting data including:
                        - positive (int): Number of positive votes
                        - negative (int): Number of negative votes
                        - important (int): Number of important votes
                        - liked (bool): Whether authenticated user liked
                        - disliked (bool): Whether authenticated user disliked
                    - metadata (dict): Additional metadata including:
                        - description (str): Full post description
                        - tags (list): Associated topic tags
                        - image (str): Featured image URL
                        - author (str): Original author name
                        - share_url (str): Social sharing URL

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
