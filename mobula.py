from typing import Optional, Dict, Any, List, Union
import requests
from datetime import datetime

class MobulaAPIError(Exception):
    """Custom exception for Mobula API errors"""
    pass

class Mobula:
    """Mobula API client"""
    
    BASE_URL = "https://api.mobula.io/api/1"
    
    def __init__(self, api_key: str):
        """
        Initialize Mobula API client.
        
        Args:
            api_key (str): Your Mobula API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": api_key
        })

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the Mobula API.
        
        Args:
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            
        Returns:
            dict: API response data
            
        Raises:
            MobulaAPIError: If the API request fails
        """
        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MobulaAPIError(f"API request failed: {str(e)}")

    # Market Data Functions
    def get_market_data(
        self,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        blockchain: Optional[str] = None,
        id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Fetches comprehensive market data for a specific cryptocurrency or token. Used to get current market metrics, price data, and trading information.

        Args:
            asset (str, optional): Asset name (e.g., 'bitcoin')
            symbol (str, optional): Trading symbol (e.g., 'BTC')
            blockchain (str, optional): Blockchain name (e.g., 'ethereum')
            id (int, optional): Unique asset identifier

        Returns:
            dict: Market data containing:
                - data (object):
                    - price (float): Current price in USD
                    - market_cap (float): Market capitalization in USD
                    - volume (float): 24-hour trading volume
                    And other market metrics as defined in the API schema

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If no identifier is provided
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        if not any(params.values()):
            raise ValueError("At least one of asset, symbol, blockchain, or id must be provided")
        
        return self._get("/market/data", params)["data"]

    def get_all_assets(self, fields: Optional[str] = "") -> List[Dict[str, Any]]:
        """
        Get data for all assets.

        Args:
            fields (str, optional): Comma-separated list of fields to include

        Returns:
            list: List of assets with their data including:
                - id (int): Asset ID
                - name (str): Asset name
                - symbol (str): Asset symbol
                - logo (str): Logo URL
                - price (float): Current price
                - market_cap (float): Market capitalization
                And other fields as specified in the API schema

        Raises:
            MobulaAPIError: If the API request fails
        """
        return self._get("/all", {"fields": fields})["data"]

    def get_market_pairs(
        self,
        limit: int = 25,
        offset: int = 0,
        id: Optional[int] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        blockchain: Optional[str] = None,
        tokens: Optional[str] = None,
        blockchains: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves trading pair information including liquidity, volume, and price data.

        Args:
            limit (int, optional): Number of pairs to return (default: 25)
            offset (int, optional): Number of pairs to skip (default: 0)
            id (int, optional): Asset ID filter
            asset (str, optional): Filter by asset name
            symbol (str, optional): Asset symbol filter
            blockchain (str, optional): Blockchain filter
            tokens (str, optional): Filter by token addresses
            blockchains (str, optional): Multiple blockchain filters

        Returns:
            dict: Market pairs data containing:
                - pairs (list): Array of trading pairs, each containing:
                    - token0/token1 (object): Details of both tokens including:
                        - address (str): Contract address
                        - price (float): Token price
                        - priceToken (float): Price in token terms
                        - approximateReserveUSD (float): USD reserve value
                        - symbol (str): Token symbol
                        - name (str): Token name
                        - decimals (int): Token decimals
                        - logo (str, nullable): Token logo URL
                    - volume24h (float): 24-hour trading volume
                    - liquidity (float): Pair liquidity
                    - blockchain (str): Blockchain name
                    - address (str): Pair contract address
                    - createdAt (str): Pair creation date
                    - exchange (object): Exchange details
                    - factory (str, nullable): Factory contract
                    - price (float): Trading price
                    And other pair-specific metrics

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/pairs", params)["data"]

    def get_market_history(
        self,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        blockchain: Optional[str] = None,
        period: Optional[str] = None,
        id: Optional[int] = None,
        from_timestamp: Optional[int] = 0,
        to_timestamp: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Retrieves historical market data for an asset over a specified time period.

        Args:
            asset (str, optional): Asset name (e.g., 'bitcoin')
            symbol (str, optional): Trading symbol (e.g., 'BTC')
            blockchain (str, optional): Blockchain name
            period (str, optional): Time period granularity
                                  Values: '1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w'
            id (int, optional): Asset ID
            from_timestamp (int, optional): Start timestamp in milliseconds (default: 0)
            to_timestamp (int, optional): End timestamp in milliseconds (default: current time)

        Returns:
            dict: Historical market data containing:
                - times (list): Timestamps for each data point
                - prices (list): Price values in USD
                - volumes (list): Trading volumes
                - liquidities (list): Liquidity values
                - market_caps (list): Market capitalizations
                - metadata (object): Additional data including:
                    - asset_id (int): Asset identifier
                    - period (str): Time period used
                    - data_points (int): Number of data points
                    - start_time (int): First data point timestamp
                    - end_time (int): Last data point timestamp

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If no identifier is provided
        """
        params = {
            k: v for k, v in {
                "asset": asset,
                "symbol": symbol,
                "blockchain": blockchain,
                "period": period,
                "id": id,
                "from": from_timestamp,
                "to": to_timestamp or int(datetime.now().timestamp() * 1000)
            }.items() if v is not None
        }
        return self._get("/market/history", params)["data"]

    # Wallet Functions
    def get_wallet_portfolio(
        self,
        wallet: Optional[str] = None,
        wallets: Optional[Union[str, List[str]]] = None,
        portfolio: Optional[str] = None,
        blockchains: Optional[Union[str, List[str]]] = None,
        asset: Optional[str] = None,
        pnl: bool = False,
        cache: bool = False,
        stale: Optional[int] = None,
        recheck_contract: bool = False,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        portfolio_settings: Optional[str] = None,
        unlisted_assets: bool = False,
        period: Optional[str] = None,
        accuracy: Optional[str] = None,
        testnet: bool = False
    ) -> Dict[str, Any]:
        """
        Get wallet portfolio data.

        Args:
            wallet (str, optional): Single wallet address
            wallets (Union[str, List[str]], optional): Multiple wallet addresses
            portfolio (str, optional): Portfolio identifier
            blockchains (Union[str, List[str]], optional): Blockchain(s) to include
            asset (str, optional): Filter by specific asset
            pnl (bool, optional): Include profit/loss data
            cache (bool, optional): Use cached data
            stale (int, optional): Stale data threshold
            recheck_contract (bool, optional): Recheck contract data
            from_timestamp (str, optional): Start timestamp
            to_timestamp (str, optional): End timestamp
            portfolio_settings (str, optional): Portfolio settings
            unlisted_assets (bool, optional): Include unlisted assets
            period (str, optional): Time period
            accuracy (str, optional): Data accuracy level
            testnet (bool, optional): Use testnet

        Returns:
            dict: Portfolio data including:
                - total_wallet_balance (float)
                - wallets (list): List of wallet addresses
                - assets (list): List of asset holdings
                - balances_length (int)
                And other portfolio metrics

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {
            "wallet": wallet,
            "wallets": ",".join(wallets) if isinstance(wallets, list) else wallets,
            "portfolio": portfolio,
            "blockchains": ",".join(blockchains) if isinstance(blockchains, list) else blockchains,
            "asset": asset,
            "pnl": pnl,
            "cache": cache,
            "stale": stale,
            "recheck_contract": recheck_contract,
            "from": from_timestamp,
            "to": to_timestamp,
            "portfolio_settings": portfolio_settings,
            "unlistedAssets": unlisted_assets,
            "period": period,
            "accuracy": accuracy,
            "testnet": testnet
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/wallet/portfolio", params)["data"]

    def get_wallet_transactions(
        self,
        wallet: Optional[str] = None,
        wallets: Optional[Union[str, List[str]]] = None,
        limit: Optional[str] = None,
        offset: Optional[str] = None,
        page: Optional[str] = None,
        order: Optional[str] = None,
        cache: Optional[str] = None,
        stale: Optional[str] = None,
        recheck_contract: Optional[str] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        asset: Optional[str] = None,
        trades: Optional[str] = None,
        blockchains: Optional[Union[str, List[str]]] = None,
        unlisted_assets: Optional[str] = None,
        only_assets: Optional[str] = None,
        pagination: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get wallet transactions.

        Args:
            wallet (str, optional): Single wallet address
            wallets (Union[str, List[str]], optional): Multiple wallet addresses
            limit (str, optional): Results per page
            offset (str, optional): Pagination offset
            page (str, optional): Page number
            order (str, optional): Sort order
            cache (str, optional): Use cached data
            stale (str, optional): Stale data threshold
            recheck_contract (str, optional): Recheck contract data
            from_timestamp (str, optional): Start timestamp
            to_timestamp (str, optional): End timestamp
            asset (str, optional): Filter by asset
            trades (str, optional): Filter by trades
            blockchains (Union[str, List[str]], optional): Filter by blockchain(s)
            unlisted_assets (str, optional): Include unlisted assets
            only_assets (str, optional): Show only specific assets
            pagination (str, optional): Pagination format

        Returns:
            dict: Transaction data including:
                - data (dict): Transaction details
                - details (dict): Additional details
                - pagination (dict): Pagination information

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {
            "wallet": wallet,
            "wallets": ",".join(wallets) if isinstance(wallets, list) else wallets,
            "limit": limit,
            "offset": offset,
            "page": page,
            "order": order,
            "cache": cache,
            "stale": stale,
            "recheckContract": recheck_contract,
            "from": from_timestamp,
            "to": to_timestamp,
            "asset": asset,
            "trades": trades,
            "blockchains": ",".join(blockchains) if isinstance(blockchains, list) else blockchains,
            "unlistedAssets": unlisted_assets,
            "onlyAssets": only_assets,
            "pagination": pagination
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/wallet/transactions", params)

    # Search Functions
    def search(
        self,
        input: str,
        filters: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for assets, tokens, and pairs.

        Args:
            input (str): Search query
            filters (str, optional): Filter criteria

        Returns:
            list: List of matching items with their details

        Raises:
            MobulaAPIError: If the API request fails
        """
        return self._get("/search", {"input": input, "filters": filters})["data"]

    # Metadata Functions
    def get_metadata(
        self,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        id: Optional[str] = None,
        blockchain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves detailed metadata for an asset including social metrics and project details.

        Args:
            asset (str, optional): Asset name
            symbol (str, optional): Asset symbol
            id (str, optional): Asset ID
            blockchain (str, optional): Blockchain name

        Returns:
            dict: Comprehensive asset metadata including:
                - id (int, nullable): Asset ID
                - name (str): Asset name
                - symbol (str): Trading symbol
                - contracts (list): Contract addresses
                - blockchains (list): Associated blockchains
                - decimals (list): Decimal places for each contract
                - twitter (str, nullable): Twitter handle
                - website (str, nullable): Project website
                - logo (str, nullable): Logo URL
                - price (float, nullable): Current price
                - market_cap (float): Market capitalization
                - liquidity (float): Current liquidity
                - volume (float): Trading volume
                - description (str, nullable): Project description
                - kyc (str, nullable): KYC verification details
                - audit (str, nullable): Audit information
                - total_supply (float): Total token supply
                - circulating_supply (float): Circulating supply
                - max_supply (float, nullable): Maximum supply
                - discord (str, nullable): Discord link
                - tags (list): Project tags/categories
                - investors (list): List of project investors
                - distribution (list): Token distribution details
                - release_schedule (list): Token release schedule
                - cexs (list): Listed centralized exchanges
                - listed_at (str, nullable): Initial listing date

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/metadata", params)["data"]

    def get_blockchains(self) -> List[Dict[str, Any]]:
        """
        Get information about all supported blockchains.

        Returns:
            list: List of blockchain data including:
                - name (str): Blockchain name
                - shortName (str): Short name/symbol
                - rpcs (list): RPC endpoints
                - chainId (str): Chain ID
                And other blockchain-specific information

        Raises:
            MobulaAPIError: If the API request fails
        """
        return self._get("/blockchains")["data"]

    def get_market_total(self) -> Dict[str, Any]:
        """
        Get total market statistics.

        Returns:
            dict: Market statistics including:
                - market_cap_history
                - market_cap_change_24h
                - btc_dominance_history

        Raises:
            MobulaAPIError: If the API request fails
        """
        return self._get("/market/total")

    def get_market_nft(
        self,
        asset: str,
        chain: str
    ) -> Dict[str, Any]:
        """
        Get NFT market data.

        Args:
            asset (str): NFT asset identifier
            chain (str): Blockchain name

        Returns:
            dict: NFT market data including:
                - price (float): NFT price in USD
                - priceETH (float): NFT price in ETH

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If required parameters are missing
        """
        if not asset or not chain:
            raise ValueError("Both asset and chain parameters are required")
        
        return self._get("/market/nft", {"asset": asset, "chain": chain})["data"]

    def get_market_multi_data(
        self,
        ids: Optional[Union[str, List[str]]] = None,
        symbols: Optional[Union[str, List[str]]] = None,
        blockchains: Optional[Union[str, List[str]]] = None,
        assets: Optional[Union[str, List[Dict[str, str]]]] = None,
        should_fetch_price_change: Union[bool, str] = False
    ) -> Dict[str, Any]:
        """
        Fetches market data for multiple assets in a single request. Perfect for portfolio tracking and market analysis.

        Args:
            ids (Union[str, List[str]], optional): Asset IDs to fetch
            symbols (Union[str, List[str]], optional): Trading symbols (e.g., ['BTC', 'ETH'])
            blockchains (Union[str, List[str]], optional): Filter by blockchain networks
            assets (Union[str, List[Dict[str, str]]], optional): Detailed asset specifications
            should_fetch_price_change (Union[bool, str], optional): Include price change data (default: False)

        Returns:
            dict: Comprehensive market data containing:
                - data (dict): Key-value pairs where each key is an asset identifier and value contains:
                    - id (int): Asset ID
                    - name (str): Asset name
                    - symbol (str): Trading symbol
                    - decimals (int, nullable): Token decimals
                    - logo (str): Logo URL
                    - rank (int, nullable): Market rank
                    - price (float): Current price
                    - market_cap (float): Market capitalization
                    - market_cap_diluted (float): Diluted market cap
                    - volume (float): Trading volume
                    - liquidity (float): Current liquidity
                    - price_change_1h/24h/7d/1m/1y (float): Price changes over time
                    - total_supply (float): Total token supply
                    - circulating_supply (float): Circulating supply
                    - contracts (list): List of blockchain contracts
                - dataArray (list): Same data in array format
        
        Raises:
            MobulaAPIError: If the API request fails
        """
        def format_param(param):
            if isinstance(param, list):
                return ','.join(param) if isinstance(param[0], str) else str(param)
            return param

        params = {
            "ids": format_param(ids) if ids is not None else None,
            "symbols": format_param(symbols) if symbols is not None else None,
            "blockchains": format_param(blockchains) if blockchains is not None else None,
            "assets": format_param(assets) if assets is not None else None,
            "shouldFetchPriceChange": should_fetch_price_change
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/multi-data", params)

    def get_market_multi_history(
        self,
        assets: Optional[str] = None,
        period: Optional[str] = None,
        symbols: Optional[str] = None,
        blockchains: Optional[str] = None,
        ids: Optional[str] = None,
        from_timestamp: Optional[str] = None,
        froms: Optional[str] = None,
        to_timestamp: Optional[str] = None,
        tos: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves historical market data for multiple assets simultaneously, supporting various time periods and aggregations.

        Args:
            assets (str, optional): Comma-separated asset names (e.g., 'bitcoin,ethereum')
            period (str, optional): Time period granularity
                                  Values: '1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w'
            symbols (str, optional): Comma-separated trading symbols (e.g., 'BTC,ETH')
            blockchains (str, optional): Comma-separated blockchain names
            ids (str, optional): Comma-separated asset IDs
            from_timestamp (str, optional): Global start timestamp for all assets
            froms (str, optional): Comma-separated start timestamps for each asset
            to_timestamp (str, optional): Global end timestamp for all assets
            tos (str, optional): Comma-separated end timestamps for each asset

        Returns:
            dict: 
                - data (object): Key-value pairs where each key is an asset identifier and value contains:
                    - times (list): Array of timestamps
                    - prices (list): Corresponding price values in USD
                    - volumes (list): Trading volumes for each time point
                    - liquidities (list): Liquidity values
                    - market_caps (list): Market capitalizations
                - metadata (object): Query details including:
                    - assets (list): List of asset identifiers
                    - period (str): Time period used
                    - start_time (int): Global start timestamp
                    - end_time (int): Global end timestamp

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/multi-history", params)["data"]

    def get_metadata_news(
        self,
        symbols: str
    ) -> List[Dict[str, Any]]:
        """
        Get news metadata for specified assets.

        Args:
            symbols (str): Comma-separated list of asset symbols

        Returns:
            list: List of news items including:
                - news_url (str): News article URL
                - image_url (str): Article image URL
                - title (str): Article title
                - text (str): Article content
                - source_name (str): News source
                - date (str): Publication date
                - sentiment (str): News sentiment
                And other news metadata

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If symbols parameter is missing
        """
        if not symbols:
            raise ValueError("Symbols parameter is required")
        
        return self._get("/metadata/news", {"symbols": symbols})["data"]

    def get_metadata_trendings(
        self,
        platform: Optional[str] = None,
        blockchain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get trending assets metadata.

        Args:
            platform (str, optional): Platform filter
            blockchain (str, optional): Blockchain filter

        Returns:
            list: List of trending assets with their metadata:
                - name (str): Asset name
                - symbol (str): Asset symbol
                - contracts (list): Contract information
                - price_change_24h (float): 24h price change
                - price (float): Current price
                And other trending metrics

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/metadata/trendings", params)

    def get_wallet_nfts(
        self,
        wallet: str,
        blockchains: Optional[str] = None,
        page: str = "1",
        offset: str = "0",
        limit: str = "100",
        pagination: str = "false"
    ) -> Dict[str, Any]:
        """
        Get NFTs owned by a wallet.

        Args:
            wallet (str): Wallet address
            blockchains (str, optional): Comma-separated list of blockchains
            page (str, optional): Page number (default: "1")
            offset (str, optional): Pagination offset (default: "0")
            limit (str, optional): Results per page (default: "100")
            pagination (str, optional): Include pagination info (default: "false")

        Returns:
            dict: Wallet's NFT holdings including:
                - data (list): List of NFTs
                - pagination (dict): Pagination details if requested

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If wallet address is missing
        """
        if not wallet:
            raise ValueError("Wallet address is required")
        
        params = {
            "wallet": wallet,
            "blockchains": blockchains,
            "page": page,
            "offset": offset,
            "limit": limit,
            "pagination": pagination
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/wallet/nfts", params)

    def get_feed_create(
        self,
        quote_id: Optional[int] = None,
        asset_id: Optional[int] = None
    ) -> Dict[str, bool]:
        """
        Create a feed.

        Args:
            quote_id (int, optional): Quote asset ID
            asset_id (int, optional): Asset ID

        Returns:
            dict: Feed creation status
                - success (bool): Whether feed was created successfully

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/feed/create", params)

    def get_market_token_holders(
        self,
        blockchain: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get token holder information.

        Args:
            blockchain (str, optional): Blockchain name
            asset (str, optional): Asset name
            symbol (str, optional): Asset symbol
            limit (int, optional): Number of holders to return (max: 100, default: 20)
            offset (int, optional): Pagination offset (default: 0)

        Returns:
            dict: Token holder information including:
                - data (list): List of holders with their holdings
                - total_count (int): Total number of holders

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {
            "blockchain": blockchain,
            "asset": asset,
            "symbol": symbol,
            "limit": min(limit, 100),  # Enforce API limit
            "offset": offset
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/token/holders", params)

    def get_multi_metadata(
        self,
        ids: Optional[str] = None,
        assets: Optional[str] = None,
        blockchains: Optional[str] = None,
        symbols: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get metadata for multiple assets.

        Args:
            ids (str, optional): Comma-separated asset IDs
            assets (str, optional): Comma-separated asset names
            blockchains (str, optional): Comma-separated blockchain names
            symbols (str, optional): Comma-separated asset symbols

        Returns:
            list: List of asset metadata

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/multi-metadata", params)["data"]

    def get_metadata_categories(self) -> List[Dict[str, Any]]:
        """
        Get metadata for asset categories.

        Returns:
            list: List of category data including:
                - name (str): Category name
                - market_cap (float): Total market cap
                - market_cap_change_24h (float): 24h market cap change
                - market_cap_change_7d (float): 7d market cap change

        Raises:
            MobulaAPIError: If the API request fails
        """
        return self._get("/metadata/categories")

    def get_market_trades_pair(
        self,
        blockchain: Optional[str] = None,
        asset: Optional[str] = None,
        address: Optional[str] = None,
        symbol: Optional[str] = None,
        limit: Optional[int] = None,
        amount: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Retrieves detailed trading information for a specific trading pair including recent trades and liquidity data.

        Args:
            blockchain (str, optional): Blockchain name (e.g., 'ethereum')
            asset (str, optional): Asset name to filter trades
            address (str, optional): Contract address of the trading pair
            symbol (str, optional): Trading symbol
            limit (int, optional): Maximum number of trades to return
            amount (int, optional): Minimum trade amount filter
            sort_by (str, optional): Field to sort trades by
            sort_order (str, optional): Sort direction ('asc' or 'desc', default: 'desc')
            offset (int, optional): Number of trades to skip (default: 0)

        Returns:
            dict: Trading pair data containing:
                - trades (list): List of recent trades, each containing:
                    - txHash (str): Transaction hash
                    - timestamp (int): Trade timestamp
                    - amount0In (float): Amount of token0 in
                    - amount1In (float): Amount of token1 in
                    - amount0Out (float): Amount of token0 out
                    - amount1Out (float): Amount of token1 out
                    - price_usd (float): Trade price in USD
                    - total_usd (float): Total trade value in USD
                    - side (str): Trade side ('buy' or 'sell')
                - pair (object): Pair information including:
                    - token0 (object): Token0 details (address, symbol, decimals)
                    - token1 (object): Token1 details (address, symbol, decimals)
                    - address (str): Pair contract address
                    - blockchain (str): Blockchain name

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/trades/pair", params)["data"]

    def get_blockchain_pairs(
        self,
        blockchain: Optional[str] = None,
        blockchains: Optional[str] = None,
        sort_by: str = "latest_trade_date",
        sort_order: str = "desc",
        factory: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        filters: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get trading pairs from a specific blockchain.

        Args:
            blockchain (str, optional): Blockchain name to filter pairs
            blockchains (str, optional): Multiple blockchain names (comma-separated)
            sort_by (str, optional): Sort field (default: "latest_trade_date")
            sort_order (str, optional): Sort direction ('asc' or 'desc', default: 'desc')
            factory (str, optional): Factory contract address
            limit (int, optional): Number of pairs to return (max 100, default: 100)
            offset (int, optional): Number of pairs to skip (default: 0)
            filters (str, optional): Additional filter criteria

        Returns:
            dict: 
                - data (list): List of trading pairs with their details
                - factories (dict): Factory contract details

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {
            "blockchain": blockchain,
            "blockchains": blockchains,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "factory": factory,
            "limit": min(limit, 100),  # Enforce API limit
            "offset": offset,
            "filters": filters
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/blockchain/pairs", params)["data"]

    def get_blockchain_stats(
        self,
        blockchain: str,
        factory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get statistics for a specific blockchain.

        Args:
            blockchain (str): Blockchain name
            factory (str, optional): Factory contract address

        Returns:
            dict: Blockchain statistics including:
                - volume_history (list): Historical volume data
                - volume_change_24h (float): 24h volume change
                - liquidity_history (list): Historical liquidity data
                - tokens_history (list): Historical token data

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If blockchain is not provided
        """
        if not blockchain:
            raise ValueError("Blockchain parameter is required")
            
        params = {"blockchain": blockchain, "factory": factory}
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/blockchain/stats", params)["data"]

    def get_cefi_funding_rate(
        self,
        symbol: str,
        quote: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get funding rates from centralized exchanges.

        Args:
            symbol (str): Trading symbol
            quote (str, optional): Quote currency

        Returns:
            dict: Funding rate data including:
                - binanceFundingRate (dict): Binance funding rate details
                - deribitFundingRate (dict): Deribit funding rate details
                - queryDetails (dict): Query parameters used

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If symbol is not provided
        """
        if not symbol:
            raise ValueError("Symbol parameter is required")
            
        params = {"symbol": symbol, "quote": quote}
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/cefi/funding-rate", params)["data"]

    def get_market_query(
        self,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        filters: Optional[str] = None,
        blockchain: Optional[str] = None,
        blockchains: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Performs a market query with various filters and sorting options to search and filter market data with custom criteria.

        Args:
            sort_by (str, optional): Field to sort by
            sort_order (str, optional): Sort direction (default: 'desc')
            filters (str, optional): Filter criteria
            blockchain (str, optional): Blockchain filter
            blockchains (str, optional): Multiple blockchain filters (comma-separated)
            limit (int, optional): Results per page (default: 20)
            offset (int, optional): Pagination offset (default: 0)

        Returns:
            dict: 
                - data (list): Array of market data entries, each containing:
                    - name (str): Asset name
                    - logo (str, nullable): Asset logo URL
                    - symbol (str): Trading symbol
                    - liquidity (float): Asset liquidity
                    - market_cap (float): Market capitalization
                    - volume (float): Trading volume
                    - off_chain_volume (float): Off-chain trading volume
                    - price (float): Current price
                    - price_change_1h (float): 1-hour price change
                    - price_change_24h (float): 24-hour price change
                    - price_change_7d (float): 7-day price change
                    - contracts (list): Contract details for each blockchain
                    - id (int): Asset ID
                    - rank (int, nullable): Market rank

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "filters": filters,
            "blockchain": blockchain,
            "blockchains": blockchains,
            "limit": limit,
            "offset": offset
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/query", params)["data"]

    def get_market_query_token(
        self,
        sort_field: Optional[str] = None,
        sort_order: str = "desc",
        sort_by: Optional[str] = None,
        filters: Optional[str] = None,
        limit: int = 20,
        blockchain: Optional[str] = None,
        blockchains: Optional[str] = None,
        unlisted_assets: bool = False
    ) -> Dict[str, Any]:
        """
        Performs a token-specific market query with filtering and sorting options.

        Args:
            sort_field (str, optional): Field to sort by
            sort_order (str, optional): Sort direction (default: 'desc')
            sort_by (str, optional): Alternative sort field
            filters (str, optional): Filter criteria
            limit (int, optional): Results per page (default: 20)
            blockchain (str, optional): Blockchain filter
            blockchains (str, optional): Multiple blockchain filters
            unlisted_assets (bool, optional): Include unlisted assets (default: False)

        Returns:
            dict: Token market data containing:
                - data (list): Array of tokens, each containing:
                    - name (str): Token name
                    - logo (str, nullable): Token logo URL
                    - symbol (str): Trading symbol
                    - address (str): Contract address
                    - blockchain (str): Blockchain name
                    - decimals (int): Token decimals
                    - volume_24h (float): 24h trading volume
                    - listed_at (str, nullable): Initial listing date
                    - circulating_supply (str): Circulating supply
                    - total_supply (str): Total supply
                    - coingecko_id (str, nullable): CoinGecko identifier
                    - pairs (list): Trading pairs information

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {
            "sortField": sort_field,
            "sortOrder": sort_order,
            "sortBy": sort_by,
            "filters": filters,
            "limit": limit,
            "blockchain": blockchain,
            "blockchains": blockchains,
            "unlistedAssets": unlisted_assets
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/query/token", params)["data"]

    def get_market_token_vs_market(
        self,
        tag: str
    ) -> Dict[str, Any]:
        """
        Compare token/market segment performance against overall market metrics.

        Args:
            tag (str): Market segment or category to analyze (e.g., 'defi', 'gaming', etc.)

        Returns:
            dict: Comparative market data including:
                - market_cap (object): Market capitalization data containing:
                    - current (float): Current market cap
                    - change_1h (float): 1-hour market cap change
                    - change_24h (float): 24-hour market cap change
                    - change_7d (float): 7-day market cap change
                    - history (list): Historical market cap data
                - volume (object): Volume data containing:
                    - current (float): Current trading volume
                    - change_24h (float): 24-hour volume change
                    - history (list): Historical volume data
                - dominance (object): Market dominance metrics:
                    - current (float): Current market dominance
                    - change_24h (float): 24-hour dominance change
                    - history (list): Historical dominance data

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If tag parameter is missing
        """
        if not tag:
            raise ValueError("Tag parameter is required")
            
        return self._get("/market/token-vs-market", {"tag": tag})["data"]

    def get_market_sparkline(
        self,
        asset: Optional[str] = None,
        blockchain: Optional[str] = None,
        symbol: Optional[str] = None,
        id: Optional[str] = None,
        time_frame: str = "24h",
        png: str = "false"
    ) -> Dict[str, str]:
        """
        Retrieves sparkline chart data for visualizing price trends. Can return either raw data points or a PNG image URL.

        Args:
            asset (str, optional): Asset name (e.g., 'bitcoin')
            blockchain (str, optional): Blockchain name (e.g., 'ethereum')
            symbol (str, optional): Trading symbol (e.g., 'BTC')
            id (str, optional): Asset ID
            time_frame (str, optional): Time period for the sparkline (default: '24h')
                                     Values: '1h', '24h', '7d', '30d', '3m', '1y', 'all'
            png (str, optional): Return PNG image URL instead of data points (default: 'false')

        Returns:
            dict: Sparkline data containing:
                - data (list): List of price data points if png=false
                - url (str): PNG image URL if png=true
                - timeFrame (str): Time frame used for the data
                - success (bool): Request success status

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If no identifier is provided
        """
        params = {
            "asset": asset,
            "blockchain": blockchain,
            "symbol": symbol,
            "id": id,
            "timeFrame": time_frame,
            "png": png
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._get("/market/sparkline", params)["data"]
