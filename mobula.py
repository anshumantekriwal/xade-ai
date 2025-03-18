from typing import Optional, Dict, Any, List, Union
import requests

class MobulaAPIError(Exception):
    pass

class Mobula:
    BASE_URL = "https://api.mobula.io/api/1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key})

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MobulaAPIError(f"API request failed: {str(e)}")
        
    

    # Market endpoints
    def get_all_assets(self, fields: str = "") -> List[Dict[str, Any]]:
        """
        Get data for all assets.

        Args:
            fields (str, optional): Comma-separated list of fields to include

        Returns:
            list: List of assets with their data including:
                - id (int): Unique asset ID
                - name (str): Asset name
                - symbol (str): Trading symbol
                - logo (str, nullable): Logo URL
                - price (float, nullable): Current price in USD
                - price_change_1h (float): 1-hour price change
                - price_change_24h (float): 24-hour price change
                - price_change_7d (float): 7-day price change
                - price_change_1m (float): 1-month price change
                - price_change_1y (float): 1-year price change
                - market_cap (float): Market capitalization
                - liquidity (float): Liquidity pool size
                - volume (float): 24h trading volume
                - blockchains (list): Supported blockchains
                - contracts (list): Contract addresses
                - decimals (list): Decimals per contract
                - website (str, nullable): Official website
                - twitter (str, nullable): Twitter handle
                - chat (str, nullable): Community chat link

        Raises:
            MobulaAPIError: If the API request fails
        """
        return self._get("/all", {"fields": fields})

    def get_blockchains(self) -> List[Dict[str, Any]]:
        """
        Get information about all supported blockchains.

        Returns:
            list: Blockchain objects containing:
                - name (str): Full blockchain name
                - shortName (str): Short identifier (e.g., "ETH")
                - rpcs (list): Public RPC endpoints
                - privateRpcs (list): Private RPC endpoints
                - chainId (str): Native chain ID
                - evmChainId (int): EVM-compatible chain ID
                - cosmosChainId (str, nullable): Cosmos chain ID
                - testnet (bool): Testnet status
                - explorer (str): Block explorer URL
                - eth (dict): Native currency details:
                    - name (str): Currency name
                    - symbol (str): Currency symbol
                    - address (str): Contract address
                    - type (str): One of: ["eth", "stable", "other"]
                    - decimals (int): Token decimals
                    - denom (str, nullable): Cosmos denomination
                    - logo (str): Logo URL
                    - id (int): Currency ID
                - stable (dict): Stablecoin details (same structure as eth)
                - multicall_contract (str): Multicall contract address
                - uniswapV3Factory (list): Factory addresses
                - routers (list): DEX routers:
                    - address (str): Contract address
                    - name (str): Router name
                - tokens (list): Native tokens:
                    - address (str): Contract address
                    - name (str): Token name
                - supportedProtocols (list): Supported protocols
                - logo (str): Chain logo URL
                - color (str): Primary brand color
                - coingeckoChain (str): CoinGecko identifier
                - dexscreenerChain (str): DexScreener identifier
                - isLayer2 (bool): Layer 2 status

        Raises:
            MobulaAPIError: If the API request fails
        """
        return self._get("/blockchains")

    def get_market_blockchain_pairs(
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
        Get blockchain pairs data.

        Args:
            blockchain (str, optional): Single blockchain name
            blockchains (str, optional): Multiple comma-separated blockchain names
            sort_by (str, optional): Field to sort by (default: "latest_trade_date")
            sort_order (str, optional): Sort direction - "asc" or "desc" (default: "desc")
            factory (str, optional): Factory contract address
            limit (int, optional): Results per page (1-100, default: 100)
            offset (int, optional): Pagination offset (default: 0)
            filters (str, optional): Additional filter parameters

        Returns:
            dict: Contains:
                - data (list): Array of pairs data including:
                    - price and price change percentages (5min, 1h, 4h, 24h)
                    - volume data (1min through 24h)
                    - trade counts (1min through 24h)
                    - liquidity and holder metrics
                    - pair info (token0/token1) including:
                        - address, price, reserves, metadata
                        - exchange details
                        - blockchain/protocol specifics
                - factories (dict): Factory contract metadata
        """
        params = {
            "blockchain": blockchain,
            "blockchains": blockchains,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "factory": factory,
            "limit": min(limit, 100),
            "offset": offset,
            "filters": filters
        }
        return self._get("/market/blockchain/pairs", params)

    def get_market_blockchain_stats(
        self,
        blockchain: str,
        factory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get blockchain analytics.

        Returns:
            dict: Contains:
                - data (object):
                    - volume_history (list): [timestamp, volume] pairs
                    - volume_change_24h (float): 24h volume % change
                    - volume_change_total (float, nullable): All-time change
                    - liquidity_history (list): [timestamp, liquidity] pairs
                    - liquidity_change_24h (float)
                    - liquidity_change_total (float, nullable)
                    - tokens_history (list): [timestamp, token count] pairs
                    - tokens_change_24h (float)
                    - tokens_change_total (float, nullable)
        """
        return self._get("/market/blockchain/stats", {"blockchain": blockchain, "factory": factory})

    def get_cefi_funding_rate(
        self,
        symbol: str,
        quote: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get centralized exchange funding rates.

        Args:
            symbol (str): Trading pair symbol (e.g., "BTCUSDT") (required)
            quote (str, optional): Quote currency (e.g., "USDT")

        Returns:
            dict: Contains:
                - binanceFundingRate (dict):
                    - symbol (str)
                    - fundingTime (int): Next funding timestamp
                    - fundingRate (float): Rate percentage
                    - marketPrice (str): Current price
                    - epochDurationMs (int): Funding interval
                - deribitFundingRate (dict): Same structure as binance
                - queryDetails (dict):
                    - base (str): Base currency
                    - quote (str, nullable): Quote currency
        """
        return self._get("/market/cefi/funding-rate", {"symbol": symbol, "quote": quote})

    def get_feed_create(
        self,
        quote_id: Optional[int] = None,
        asset_id: Optional[int] = None
    ) -> Dict[str, bool]:
        """
        Create a feed configuration.

        Args:
            quote_id (int, optional): Quote asset ID
            asset_id (int, optional): Base asset ID

        Returns:
            dict: Contains:
                - success (bool): Creation status
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/feed/create", params)

    def get_market_history_pair(
        self,
        blockchain: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        address: Optional[str] = None,
        base_token: Optional[str] = None,
        from_timestamp: Optional[Union[int, str]] = None,
        to_timestamp: Optional[Union[int, str]] = None,
        period: Optional[str] = None,
        amount: Optional[float] = None,
        latest: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get market history for a trading pair.

        Args:
            blockchain (str, optional): Blockchain name
            asset (str, optional): Asset name
            symbol (str, optional): Trading symbol
            address (str, optional): Contract address
            base_token (str, optional): Base token address
            from_timestamp (Union[int, str], optional): Start timestamp
            to_timestamp (Union[int, str], optional): End timestamp  
            period (str, optional): Time period granularity
            amount (float, optional): Token amount
            latest (str, optional): Latest data flag

        Returns:
            dict: Contains:
                - data (list): Array of OHLCV candlesticks with:
                    - volume (float): Trading volume
                    - open (float): Opening price
                    - high (float): Highest price
                    - low (float): Lowest price
                    - close (float): Closing price
                    - time (int): Candle timestamp
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/history/pair", params)

    def get_market_history(
        self,
        blockchain: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        period: Optional[str] = None,
        id: Optional[int] = None,
        from_timestamp: int = 0,
        to_timestamp: int = 1740735669314
    ) -> Dict[str, Any]:
        """
        Retrieves historical market data for an asset.

        Args:
            asset (str, optional): Asset name (e.g., 'bitcoin')
            symbol (str, optional): Trading symbol (e.g., 'BTC')
            blockchain (str, optional): Blockchain name filter
            period (str, optional): Time granularity - 
                One of: '24h', '7d', '1m', '1y', 'all'
            id (int, optional): Asset ID
            from_timestamp (int, optional): Start timestamp (milliseconds)
            to_timestamp (int, optional): End timestamp (milliseconds)

        Returns:
            dict: Contains:
                - data (object):
                    - price_history (list): Array of [timestamp, price] pairs
                    - name (str): Asset name
                    - symbol (str): Trading symbol

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/history", params)

    def get_market_multi_data(
        self,
        ids: Optional[Union[str, List[str]]] = None,
        symbols: Optional[Union[str, List[str]]] = None,
        blockchains: Optional[Union[str, List[str]]] = None,
        assets: Optional[Union[str, List[Dict[str, str]]]] = None,
        should_fetch_price_change: Union[bool, str] = False
    ) -> Dict[str, Any]:
        """
        Returns:
            dict: Contains:
                - data (dict): Key-value pairs with asset identifiers as keys:
                    - key (str): Asset identifier
                    - id (int): Unique ID
                    - name (str): Asset name
                    - symbol (str): Trading symbol
                    - decimals (int, nullable): Token decimals
                    - logo (str): Logo URL
                    - rank (int, nullable): Market rank
                    - price (float): Current price
                    - market_cap (float): Market capitalization
                    - market_cap_diluted (float): Fully diluted market cap
                    - volume (float): 24h trading volume
                    - volume_change_24h (float): 24h volume change
                    - volume_7d (float): 7d trading volume
                    - liquidity (float): Total liquidity
                    - ath (float): All-time high
                    - atl (float): All-time low
                    - off_chain_volume (float): CEX volume
                    - is_listed (bool): CEX listing status
                    - price_change_1h/24h/7d/1m/1y (float): Price changes
                    - total_supply (float): Total tokens
                    - circulating_supply (float): Circulating tokens
                    - contracts (list):
                        - address (str): Contract address
                        - blockchainId (str): Chain ID
                        - blockchain (str): Chain name
                        - decimals (int): Token decimals
                - dataArray (list): Same data in array format
        """
        params = {
            "ids": ",".join(ids) if isinstance(ids, list) else ids,
            "symbols": ",".join(symbols) if isinstance(symbols, list) else symbols,
            "blockchains": ",".join(blockchains) if isinstance(blockchains, list) else blockchains,
            "assets": assets,
            "shouldFetchPriceChange": should_fetch_price_change
        }
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
        Returns:
            dict: Contains:
                - data (list): Array of historical data objects:
                    - price_history (list): Array of [timestamp, price] pairs
                    - name (str): Asset name
                    - symbol (str): Trading symbol
                    - address (str): Contract address

        Raises:
            MobulaAPIError: For failed API requests
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/multi-history", params)

    def get_market_nft(
        self,
        asset: str,
        chain: str
    ) -> Dict[str, Any]:
        """
        Get NFT market data.

        Args:
            asset (str): NFT contract address or identifier
            chain (str): Blockchain name (e.g., "ethereum")

        Returns:
            dict: Contains:
                - price (float): Current price in USD
                - priceETH (float): Current price in ETH

        Raises:
            MobulaAPIError: If the API request fails
            ValueError: If missing required parameters
        """
        return self._get("/market/nft", {"asset": asset, "chain": chain})

    def get_market_pair(
        self,
        blockchain: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        address: Optional[str] = None,
        base_token: Optional[str] = None,
        stats: Union[bool, str] = False
    ) -> Dict[str, Any]:
        """
        Retrieve recent trades for a liquidity pool.

        Returns:
            dict: Contains:
                - data (list): Trade objects:
                    - blockchain (str): Chain name
                    - hash (str): Transaction hash
                    - pair (str): Trading pair address
                    - date (int): Unix timestamp
                    - token_price_vs (float): Price in quote token
                    - token_price (float): Price in USD
                    - token_amount (float): Base token amount
                    - token_amount_vs (float): Quote token amount
                    - token_amount_usd (float): USD value
                    - type (str): Trade type (e.g., "swap")
                    - sender (str): Trader address
                    - token_amount_raw (str): Raw base token amount
                    - token_amount_raw_vs (str): Raw quote token amount
                    - operation (str): Trade action (e.g., "Buy"/"Sell")
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/pair", params)

    def get_market_pairs(
        self,
        limit: str = "25",
        offset: str = "0",
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
            limit (int, optional): Number of pairs to return (1-100, default: 25)
            offset (int, optional): Pagination offset (default: 0)
            id (int, optional): Filter by asset ID
            asset (str, optional): Filter by asset name
            symbol (str, optional): Filter by trading symbol
            blockchain (str, optional): Filter by blockchain
            tokens (str, optional): Comma-separated token addresses
            blockchains (str, optional): Comma-separated blockchain names

        Returns:
            dict: Contains 'pairs' array with:
                - token0 (dict):
                    - address (str): Contract address
                    - price (float): USD price
                    - priceToken (float): Price in paired token
                    - priceTokenString (str): Formatted token price
                    - approximateReserveUSD (float): USD liquidity
                    - approximateReserveTokenRaw (str): Raw reserve amount
                    - approximateReserveToken (float): Reserve amount
                    - symbol (str): Token symbol
                    - name (str): Token name
                    - id (int): Token ID
                    - decimals (int): Token decimals
                    - totalSupply (float): Total supply
                    - circulatingSupply (float): Circulating supply
                    - logo (str, nullable): Logo URL
                    - chainId (str): Blockchain ID
                - token1 (dict): Same structure as token0
                - volume24h (float): 24h trading volume
                - liquidity (float): Total liquidity
                - blockchain (str): Blockchain name
                - address (str): Pair contract address
                - createdAt (str): Creation timestamp
                - type (str): Pair type
                - baseToken (str): Base token symbol
                - exchange (dict):
                    - name (str): Exchange name
                    - logo (str): Exchange logo
                - factory (str, nullable): Factory contract
                - quoteToken (str): Quote token symbol
                - price (float): Current price
                - priceToken (float): Price in token terms
                - priceTokenString (str): Formatted price string

        Raises:
            MobulaAPIError: If the API request fails
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/pairs", params)

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
        Token-specific market query.

        Returns:
            list: Token objects with:
                - name (str)
                - logo (str, nullable)
                - symbol (str)
                - address (str)
                - blockchain (str)
                - decimals (int)
                - volume_24h (float)
                - listed_at (str, nullable)
                - circulating_supply (str)
                - total_supply (str)
                - coingecko_id (str, nullable)
                - pairs (list): Trading pair details
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/market/query/token", params)

    #region Wallet Endpoints
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
            wallet (str): Wallet address (required)
            blockchains (str, optional): Comma-separated blockchain names
            page (str, optional): Page number (default: "1")
            offset (str, optional): Pagination offset (default: "0")
            limit (str, optional): Results per page (1-100, default: "100")
            pagination (str, optional): Enable pagination metadata ("true"/"false")

        Returns:
            dict: Contains:
                - data (list): NFT items with:
                    - token_address (str): Contract address
                    - token_id (str): NFT ID
                    - token_uri (str): Metadata URI
                    - amount (str): Quantity owned
                    - owner_of (str): Current owner
                    - name (str): NFT collection name
                    - symbol (str): Collection symbol
                    - blockchain (str): Chain name
                    - chain_id (str): Chain ID
                - pagination (dict, nullable):
                    - total (int): Total results
                    - page (int): Current page
                    - offset (int): Results skipped
                    - limit (int): Results per page
        """
        params = {
            "wallet": wallet,
            "blockchains": blockchains,
            "page": page,
            "offset": offset,
            "limit": limit,
            "pagination": pagination
        }
        return self._get("/wallet/nfts", params)

    def get_wallet_transactions(
        self,
        wallet: Optional[str] = None,
        wallets: Optional[Union[str, List[str]]] = None,
        limit: Optional[str] = None,
        offset: Optional[str] = None,
        page: Optional[str] = None,
        order: Optional[str] = None,
        blockchains: Optional[Union[str, List[str]]] = None,
        asset: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get wallet transactions.

        Returns:
            dict: Contains:
                - data (object):
                    - transactions (list):
                        - id (str): Transaction ID
                        - timestamp (int): Unix timestamp
                        - from (str, nullable): Sender address
                        - to (str, nullable): Receiver address
                        - contract (str, nullable): Contract address
                        - hash (str): Transaction hash
                        - amount_usd (float): USD value
                        - amount (float): Token amount
                        - block_number (int): Block number
                        - type (str): Transaction type
                        - blockchain (str): Chain name
                        - tx_cost (float): Transaction fee in USD
                        - transaction (object):
                            - hash (str)
                            - chainId (str)
                            - fees (str): Fee amount
                            - feesUSD (float): Fee USD value
                            - date (str): ISO timestamp
                        - asset (object):
                            - id (int, nullable)
                            - name (str)
                            - symbol (str)
                            - totalSupply (float)
                            - circulatingSupply (float)
                            - price (float)
                            - liquidity (float)
                            - priceChange24hPercent (float)
                            - marketCapUSD (float)
                            - logo (str, nullable)
                            - nativeChainId (str, nullable)
                            - contract (str, nullable)
                    - wallets (list): Queried addresses
                - pagination (dict, nullable):
                    - total (int): Total results
                    - page (int): Current page
                    - offset (int): Results skipped
                    - limit (int): Results per page
        """
        params = {
            "wallet": wallet,
            "wallets": ",".join(wallets) if isinstance(wallets, list) else wallets,
            "limit": limit,
            "offset": offset,
            "page": page,
            "order": order,
            "blockchains": ",".join(blockchains) if isinstance(blockchains, list) else blockchains,
            "asset": asset
        }
        return self._get("/wallet/transactions", params)

    def get_wallet_history(
        self,
        wallet: Optional[str] = None,
        wallets: Optional[Union[str, List[str]]] = None,
        blockchains: Optional[Union[str, List[str]]] = None,
        asset: Optional[str] = None,
        from_timestamp: Optional[str] = None,
        to_timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get historical wallet balance.

        Args:
            wallet (str, optional): Single wallet address
            wallets (str, optional): Comma-separated wallet addresses
            portfolio (str, optional): Portfolio ID
            blockchains (str, optional): Comma-separated blockchain names
            asset (str, optional): Filter by asset
            pnl (str, optional): Include PNL data ("true"/"false")
            cache (str, optional): Bypass cache ("true"/"false")
            stale (int, optional): Max staleness duration (seconds)
            recheck_contract (str, optional): Revalidate contracts ("true"/"false")
            from (str, optional): Start timestamp (ISO or UNIX)
            to (str, optional): End timestamp (ISO or UNIX)
            portfolio_settings (str, optional): Settings JSON
            unlisted_assets (str, optional): Include unlisted ("true"/"false")
            period (str, optional): Timeframe (e.g., "7d")
            accuracy (str, optional): Data resolution ("low"/"high")
            testnet (str, optional): Include testnets ("true"/"false")
            liqmin (str, optional): Minimum liquidity filter

        Returns:
            dict: Contains:
                - data (object):
                    - wallets (list): Wallet addresses
                    - balance_usd (float): Current balance
                    - balance_history (list): [timestamp, balance] pairs
        """
        params = {
            "wallet": wallet,
            "wallets": ",".join(wallets) if isinstance(wallets, list) else wallets,
            "blockchains": ",".join(blockchains) if isinstance(blockchains, list) else blockchains,
            "asset": asset,
            "from": from_timestamp,
            "to": to_timestamp
        }
        return self._get("/wallet/history", params)

    def get_wallet_multi_portfolio(
        self,
        wallets: Union[str, List[str]],
        blockchains: Optional[Union[str, List[str]]] = None,
        period: Optional[str] = None,
        accuracy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get portfolio data for multiple wallets.

        Returns:
            dict: Same structure as `get_wallet_portfolio()`, but with:
                - total_wallet_balance (float): Combined balance
                - pnl_history (dict): Includes "1y", "7d", "24h", "30d" timeframes
                - total_realized_pnl (float): Aggregate realized gains
                - total_unrealized_pnl (float): Aggregate unrealized gains
        """
        params = {
            "wallets": ",".join(wallets) if isinstance(wallets, list) else wallets,
            "blockchains": ",".join(blockchains) if isinstance(blockchains, list) else blockchains,
            "period": period,
            "accuracy": accuracy
        }
        return self._get("/wallet/multi-portfolio", params)
    #endregion

    #region Metadata Endpoints
    def get_metadata(
        self,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        id: Optional[str] = None,
        blockchain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns:
            dict: Contains:
                - id (int, nullable)
                - name (str)
                - symbol (str)
                - contracts (list)
                - blockchains (list)
                - decimals (list)
                - twitter (str, nullable)
                - website (str, nullable)
                - logo (str, nullable)
                - price (float, nullable)
                - market_cap (float)
                - liquidity (float)
                - volume (float)
                - description (str, nullable)
                - kyc (str, nullable)
                - audit (str, nullable)
                - total_supply (float)
                - circulating_supply (float)
                - max_supply (float, nullable)
                - discord (str, nullable)
                - tags (list)
                - investors (list):
                    - lead (bool)
                    - name (str)
                    - type (str)
                    - image (str)
                    - country_name (str)
                    - description (str)
                - distribution (list):
                    - percentage (float)
                    - name (str)
                - release_schedule (list):
                    - allocation_details (dict)
                    - tokens_to_unlock (float)
                    - unlock_date (int)
                - cexs (list):
                    - logo (str, nullable)
                    - name (str, nullable)
                    - id (str)
                - listed_at (str, nullable)
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._get("/metadata", params)

    def get_multi_metadata(
        self,
        ids: Optional[str] = None,
        assets: Optional[str] = None,
        blockchains: Optional[str] = None,
        symbols: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get metadata for multiple assets in bulk.

        Args:
            ids (str, optional): Comma-separated asset IDs
            assets (str, optional): Comma-separated asset names
            blockchains (str, optional): Comma-separated blockchain names
            symbols (str, optional): Comma-separated trading symbols

        Returns:
            list: Array of metadata objects (same structure as `get_metadata()`)
        """
        params = {
            "ids": ids,
            "assets": assets,
            "blockchains": blockchains,
            "symbols": symbols
        }
        return self._get("/multi-metadata", params)

    def get_metadata_categories(self) -> List[Dict[str, Any]]:
        """
        Get cryptocurrency category metrics.

        Returns:
            list: Categories with:
                - name (str): Category name
                - market_cap (float): Total market cap
                - market_cap_change_24h (float): 24h % change
                - market_cap_change_7d (float): 7d % change
        """
        return self._get("/metadata/categories")

    def get_metadata_news(
        self,
        symbols: str
    ) -> Dict[str, Any]:
        """
        Get asset-related news.
        Args:
            symbols (str): Comma-separated asset symbols (e.g., "BTC,ETH")

        Returns:
            dict: Contains:
                - data (list): News articles with:
                    - news_url (str)
                    - image_url (str)
                    - title (str)
                    - text (str)
                    - source_name (str)
                    - date (str)
                    - topics (list)
                    - sentiment (str)
                    - type (str)
                    - tickers (list)
        """
        return self._get("/metadata/news", {"symbols": symbols})

    def get_metadata_trendings(
        self,
        platform: Optional[str] = None,
        blockchain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get trending assets across platforms.

        Args:
            platform (str, optional): Filter by platform (e.g., "uniswap")
            blockchain (str, optional): Filter by blockchain

        Returns:
            list: Trending assets with:
                - platforms (list): Platforms where trending:
                    - name (str): Platform name
                    - rank (int): Trend rank
                    - weight (float): Trend score weight
                - contracts (list): Contract addresses per blockchain
                - trending_score (float): Aggregate trend score

        """
        params = {
            "platform": platform,
            "blockchain": blockchain
        }
        return self._get("/metadata/trendings", params)
    #endregion

    #region Market Endpoints
    def get_market_query(
        self,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        filters: Optional[str] = None,
        blockchain: Optional[str] = None,
        blockchains: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Query assets with filters/sorting.

        Returns:
            list: Asset objects with:
                - name (str)
                - logo (str, nullable)
                - symbol (str)
                - liquidity (float)
                - market_cap (float)
                - volume (float)
                - off_chain_volume (float)
                - price (float)
                - price_change_1h/24h/7d (float)
                - contracts (list): Contract details per blockchain
                - id (int)
                - rank (int, nullable)
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
        return self._get("/market/query", params)

    def get_market_sparkline(
        self,
        asset: Optional[str] = None,
        blockchain: Optional[str] = None,
        symbol: Optional[str] = None,
        id: Optional[str] = None,
        time_frame: str = "24h",
        png: str = "false"
    ) -> Dict[str, Any]:
        """
        Get price sparkline data.

        Args:
            asset (str, optional): Asset name
            blockchain (str, optional): Chain name
            symbol (str, optional): Trading symbol
            id (str, optional): Asset ID
            time_frame (str, optional): Range - 
                "24h", "7d", "1m", "1y", "all" (default: "24h")
            png (str, optional): Return PNG URL ("true"/"false")

        Returns:
            dict: Contains:
                - url (str): PNG image URL if png=true
                (If png=false, returns array of [timestamp, price] pairs)
        """
        params = {
            "asset": asset,
            "blockchain": blockchain,
            "symbol": symbol,
            "id": id,
            "timeFrame": time_frame,
            "png": png
        }
        return self._get("/market/sparkline", params)

    def get_market_token_holders(
        self,
        blockchain: Optional[str] = None,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get token holder distribution.

        Args:
            blockchain (str, optional): Chain name
            asset (str, optional): Asset name
            symbol (str, optional): Trading symbol
            limit (int, optional): Results per page (1-100, default: 20)
            offset (int, optional): Pagination offset (default: 0)

        Returns:
            dict: Contains:
                - data (list): Holders with:
                    - address (str): Wallet address
                    - amountRaw (str): Raw balance
                    - amount (float): Normalized balance
                    - chainId (str): Blockchain ID
                    - totalSupplyShare (float): Ownership percentage
                    - amountUSD (float): USD value
                - total_count (int): Total holders
        """
        params = {
            "blockchain": blockchain,
            "asset": asset,
            "symbol": symbol,
            "limit": min(limit, 100),
            "offset": offset
        }
        return self._get("/market/token/holders", params)

    def get_market_token_vs_market(
        self,
        tag: str
    ) -> Dict[str, Any]:
        """
        Compare token performance against market segments.

        Args:
            tag (str): Market segment (e.g., "defi", "gaming")

        Returns:
            dict: Contains mixed data types:
                - For tokens:
                    - marketCapUSD (float)
                    - priceUSD (float, nullable)
                    - priceChange[...]Percent (float)
                - For market segments:
                    - marketCapChange[...]Percent (float)
                    - volumeUSD (float)

        """
        return self._get("/market/token-vs-market", {"tag": tag})

    def get_market_total(self) -> Dict[str, Any]:
        """
        Get aggregated market statistics.

        Returns:
            dict: Contains:
                - market_cap_history (list): Array of [timestamp, market cap] pairs
                - market_cap_change_24h (str): 24h change percentage
                - btc_dominance_history (list): Array of [timestamp, dominance] pairs

        Raises:
            MobulaAPIError: If the API request fails
        """        
        return self._get("/market/total")

    def search(
        self,
        input: str,
        filters: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for assets/tokens/pairs.

        Returns:
            list: Results may include:
                - For tokens:
                    - type: 'token'
                    - logo (str, nullable)
                    - name (str)
                    - symbol (str)
                    - decimals (list)
                    - blockchains (list)
                    - contracts (list)
                    - price (float)
                    - total_supply (str)
                    - pairs (list): Trading pairs
                - For assets:
                    - type: 'asset'
                    - id (int)
                    - contracts (list)
                    - blockchains (list)
                    - decimals (list)
                    - twitter (str)
                    - website (str)
                    - logo (str, nullable)
                    - price (float)
                    - market_cap (float)
                    - liquidity (float)
                    - volume (float)
                    - pairs (list): Trading pairs
        """
        return self._get("/search", {"input": input, "filters": filters})
    #endregion

    def get_market_data(
        self,
        asset: Optional[str] = None,
        symbol: Optional[str] = None,
        blockchain: Optional[str] = None,
        id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive market data for a specific asset.

        Args:
            asset: Name of the asset (e.g., "bitcoin")
            symbol: Trading symbol (e.g., "BTC")
            blockchain: Blockchain name (e.g., "ethereum")
            id: Mobula asset ID

        Returns:
            Dict containing:
            - id (int): Unique asset identifier
            - name (str): Asset name
            - symbol (str): Trading symbol
            - contracts (List[str]): Contract addresses across blockchains
            - blockchains (List[str]): Supported blockchains
            - decimals (List[int]): Decimals for each contract
            - twitter (str, nullable): Twitter handle
            - website (str, nullable): Project website
            - logo (str, nullable): Logo URL
            - price (float, nullable): Current price in USD
            - market_cap (float): Market capitalization
            - liquidity (float): Total liquidity
            - volume (float): 24h trading volume
            - description (str, nullable): Project description
            - kyc (str, nullable): KYC status
            - audit (str, nullable): Audit information
            - total_supply (float): Total token supply
            - circulating_supply (float): Circulating supply
            - max_supply (float, nullable): Maximum supply
            - discord (str, nullable): Discord invite link
            - tags (List[str]): Associated categories/tags
            - investors (List[Dict]): Investment details:
                - lead (bool): Lead investor status
                - name (str): Investor name
                - type (str): Investor type (VC, Angel, etc.)
                - image (str): Investor logo
                - country_name (str): Headquarters location
                - description (str): Investment details
            - distribution (List[Dict]): Token allocation:
                - percentage (float): Allocation percentage
                - name (str): Allocation category
            - release_schedule (List[Dict]): Vesting schedule:
                - allocation_details (Dict): Breakdown by category
                - tokens_to_unlock (float): Number of tokens
                - unlock_date (int): UNIX timestamp
            - cexs (List[Dict]): Exchange listings:
                - logo (str, nullable): Exchange logo
                - name (str, nullable): Exchange name
                - id (str): Exchange identifier
            - listed_at (str, nullable): Initial listing date (ISO 8601)
        """
        params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        if not params:
            raise ValueError("At least one identifier required")
        return self._get("/market/data", params)

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
        Get comprehensive portfolio data for a wallet.

        Args:
            wallet: Single wallet address
            wallets: Multiple wallet addresses (comma-separated or list)
            portfolio: Portfolio identifier
            blockchains: Filter by blockchains
            asset: Filter by specific asset
            pnl: Include profit/loss data
            cache: Use cached data
            stale: Accept stale data up to X seconds
            recheck_contract: Force contract recheck
            from_timestamp: Start time (ISO 8601 or UNIX timestamp)
            to_timestamp: End time (ISO 8601 or UNIX timestamp)
            portfolio_settings: Custom settings JSON
            unlisted_assets: Include unlisted assets
            period: Time period for historical data
            accuracy: Data resolution (high/low)
            testnet: Include testnet assets

        Returns:
            Dict containing:
            - total_wallet_balance (float): Total USD value
            - wallets (List[str]): Wallet addresses analyzed
            - assets (List[Dict]): Asset holdings details:
                - contracts_balances (List[Dict]):
                    - address (str): Contract address
                    - balance (float): Normalized balance
                    - balanceRaw (str): Raw on-chain balance
                    - chainId (str): Blockchain ID
                    - decimals (int): Token decimals
                - cross_chain_balances (Dict): Balances per blockchain
                - price_change_24h (float): 24h price change
                - estimated_balance (float): USD value
                - price (float): Current price
                - token_balance (float): Total tokens held
                - allocation (float): Portfolio percentage
                - asset (Dict): Asset metadata
                - realized_pnl (float): Realized gains/losses
                - unrealized_pnl (float): Unrealized gains/losses
                - price_bought (float): Average buy price
            - pnl_history (Dict): Historical PNL for 1y/7d/24h/30d
            - total_realized_pnl (float): Total realized PNL
            - total_unrealized_pnl (float): Total unrealized PNL
            - total_pnl_history (Dict): Aggregated PNL history
            - balances_length (int): Number of balance records
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
        return self._get("/wallet/portfolio", {k: v for k, v in params.items() if v is not None})

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
        Get trading pairs from specific blockchain(s).

        Args:
            blockchain: Single blockchain name
            blockchains: Multiple blockchains (comma-separated)
            sort_by: Sorting field (latest_trade_date, liquidity, volume24h)
            sort_order: Sorting direction (asc/desc)
            factory: Factory contract address
            limit: Results per page (1-100)
            offset: Pagination offset
            filters: Additional filters (JSON string)

        Returns:
            Dict containing:
            - data (List[Dict]): Trading pairs:
                - token0 (Dict):
                    - address (str)
                    - price (float)
                    - priceToken (float)
                    - priceTokenString (str)
                    - approximateReserveUSD (float)
                    - approximateReserveTokenRaw (str)
                    - approximateReserveToken (float)
                    - symbol (str)
                    - name (str)
                    - id (int)
                    - decimals (int)
                    - totalSupply (float)
                    - circulatingSupply (float)
                    - logo (str, nullable)
                    - chainId (str)
                - token1 (Dict): Same structure as token0
                - volume24h (float)
                - liquidity (float)
                - blockchain (str)
                - address (str)
                - createdAt (str)
                - type (str)
                - baseToken (str)
                - exchange (Dict):
                    - name (str)
                    - logo (str)
                - factory (str, nullable)
                - quoteToken (str)
                - price (float)
                - priceToken (float)
                - priceTokenString (str)
            - factories (Dict): Factory contract data
        """
        params = {
            "blockchain": blockchain,
            "blockchains": blockchains,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "factory": factory,
            "limit": min(limit, 100),
            "offset": offset,
            "filters": filters
        }
        return self._get("/market/blockchain/pairs", params)
