import math
import statistics
from typing import List, Dict, Any
import numpy as np

def calculateSMA(raw_market_history_output: Dict[str, Any], period: int) -> float:
    """
    Function Name: calculateSMA
    Description: Computes the Simple Moving Average (SMA) using historical price data.
                 The raw API output is expected to have a "data" field containing "price_history",
                 which is a list of price data. If "price_history" is a list of lists, each sublist is assumed to be 
                 structured as [timestamp, price] and the price is extracted from index 1.
    Inputs:
        - raw_market_history_output: Raw API output from Mobula.get_market_history.
        - period: Number of most recent data points to average.
    Processing:
        - Extract "price_history" from the "data" field.
        - Convert the price history into a flat list of floats by extracting the price from each entry.
        - Extract the last 'period' prices and compute their arithmetic mean.
    Output:
        - A float representing the SMA.
    """
    price_history = raw_market_history_output.get("data", {}).get("price_history", [])
    if not price_history:
        raise ValueError("price_history not found in raw market history output.")
    # If elements are lists, extract the second element from each sublist (index 1).
    if isinstance(price_history[0], list):
        prices = [entry[1] for entry in price_history if entry and len(entry) > 1]
    else:
        prices = price_history
    if len(prices) < period:
        raise ValueError("Not enough data points to compute SMA.")
    return sum(prices[-period:]) / period


def calculateEMA(raw_market_history_output: Dict[str, Any], period: int) -> float:
    """
    Function Name: calculateEMA
    Description: Computes the Exponential Moving Average (EMA) where more weight is given to recent prices.
                 The raw API output is expected to have a "data" field containing "price_history",
                 which is a list of price data. If "price_history" is a list of lists, each sublist is assumed to be 
                 structured as [timestamp, price] and the price is extracted from index 1.
    Inputs:
        - raw_market_history_output: Raw API output from Mobula.get_market_history.
        - period: The EMA period.
    Processing:
        - Extract "price_history" and convert it to a flat list of floats.
        - Initialize EMA with the SMA of the first 'period' values.
        - Update the EMA iteratively using the smoothing factor k = 2/(period+1).
    Output:
        - A float representing the final EMA.
    """
    price_history = raw_market_history_output.get("data", {}).get("price_history", [])
    if not price_history:
        raise ValueError("price_history not found in raw market history output.")
    if isinstance(price_history[0], list):
        prices = [entry[1] for entry in price_history if entry and len(entry) > 1]
    else:
        prices = price_history
    if len(prices) < period:
        raise ValueError("Not enough data points to compute EMA.")
    ema = sum(prices[:period]) / period
    k = 2 / (period + 1)
    for price in prices[period:]:
        ema = price * k + ema * (1 - k)
    return ema

def calculateRSI(raw_market_history_output: Dict[str, Any], period: int = 14) -> float:
    """
    Function Name: calculateRSI
    Description: Computes the Relative Strength Index (RSI) to indicate momentum and identify overbought or oversold conditions.
                 The raw API output is expected to have a "data" field containing "price_history",
                 which is a list of price data. If "price_history" is a list of lists, each sublist is assumed to be 
                 structured as [timestamp, price] and the price is extracted from index 1.
    Inputs:
        - raw_market_history_output: Raw API output from Mobula.get_market_history.
        - period: RSI period (default is 14).
    Processing:
        - Extract "price_history" and convert it to a flat list of floats.
        - Compute consecutive price changes; separate gains and losses.
        - Calculate the average gain and average loss over the period.
        - Compute RS = (average gain) / (average loss) and then RSI = 100 - (100 / (1 + RS)).
    Output:
        - A float (0 to 100) representing the RSI.
    """
    price_history = raw_market_history_output.get("data", {}).get("price_history", [])
    if not price_history:
        raise ValueError("price_history not found in raw market history output.")
    if isinstance(price_history[0], list):
        prices = [entry[1] for entry in price_history if entry and len(entry) > 1]
    else:
        prices = price_history
    if len(prices) <= period:
        raise ValueError("Not enough data points to compute RSI.")
    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change >= 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculateMACD(raw_market_history_output: Dict[str, Any], fast_period: int, slow_period: int, signal_period: int) -> Dict[str, float]:
    """
    Function Name: calculateMACD
    Description: Calculates the Moving Average Convergence Divergence (MACD) indicator.
                 The raw API output is expected to have a "data" field containing "price_history",
                 which is a list of price data. If "price_history" is a list of lists, each sublist is assumed to be 
                 structured as [timestamp, price] and the price is extracted from index 1.
    Inputs:
        - raw_market_history_output: Raw API output from Mobula.get_market_history.
        - fast_period: Period for the fast EMA.
        - slow_period: Period for the slow EMA.
        - signal_period: Period for the signal line EMA.
    Processing:
        - Extract "price_history" and convert it to a flat list of floats.
        - Compute fast and slow EMAs.
        - Derive MACD_line = fast EMA - slow EMA.
        - Compute the signal line as the EMA of the MACD_line over the signal_period.
        - Calculate the histogram as MACD_line minus the signal line.
    Output:
        - A dictionary with keys "macd_line", "signal_line", and "histogram" representing the respective values.
    """
    price_history = raw_market_history_output.get("data", {}).get("price_history", [])
    if not price_history:
        raise ValueError("price_history not found in raw market history output.")
    if isinstance(price_history[0], list):
        prices = [entry[1] for entry in price_history if entry and len(entry) > 1]
    else:
        prices = price_history
    if len(prices) < slow_period:
        raise ValueError("Not enough data points to compute MACD.")
    
    # Fast EMA
    fast_ema = sum(prices[:fast_period]) / fast_period
    k_fast = 2 / (fast_period + 1)
    fast_ema_values = [fast_ema]
    for price in prices[fast_period:]:
        fast_ema = price * k_fast + fast_ema * (1 - k_fast)
        fast_ema_values.append(fast_ema)
    
    # Slow EMA
    slow_ema = sum(prices[:slow_period]) / slow_period
    k_slow = 2 / (slow_period + 1)
    slow_ema_values = [slow_ema]
    for price in prices[slow_period:]:
        slow_ema = price * k_slow + slow_ema * (1 - k_slow)
        slow_ema_values.append(slow_ema)
    
    # Align fast EMA to slow EMA length
    aligned_fast = fast_ema_values[-len(slow_ema_values):]
    macd_line = [f - s for f, s in zip(aligned_fast, slow_ema_values)]
    if len(macd_line) < signal_period:
        raise ValueError("Not enough MACD data to compute signal line.")
    
    # Signal line calculation
    signal = sum(macd_line[:signal_period]) / signal_period
    k_signal = 2 / (signal_period + 1)
    signal_line_values = [signal]
    for value in macd_line[signal_period:]:
        signal = value * k_signal + signal * (1 - k_signal)
        signal_line_values.append(signal)
    
    # Align signal line with MACD line length (pad if necessary)
    signal_line = [None] * (len(macd_line) - len(signal_line_values)) + signal_line_values
    histogram = [m - s if s is not None else 0 for m, s in zip(macd_line, signal_line)]
    return {
        "macd_line": macd_line[-1],
        "signal_line": signal_line[-1] if signal_line[-1] is not None else 0,
        "histogram": histogram[-1]
    }


def calculateVolatility(raw_market_history_output: Dict[str, Any], time_frame: str = "24h") -> float:
    """
    Function Name: calculateVolatility
    Description: Computes market volatility as the standard deviation of percentage returns.
                 The raw API output is expected to have a "data" field containing "price_history",
                 which is a list of price data. If "price_history" is a list of lists, each sublist is assumed to be 
                 structured as [timestamp, price] and the price is extracted from index 1.
    Inputs:
        - raw_market_history_output: Raw API output from Mobula.get_market_history.
        - time_frame: A string indicating the time frame (e.g., "24h"); used for contextual purposes.
    Processing:
        - Extract "price_history" and convert it to a flat list of floats.
        - Compute percentage returns between consecutive prices.
        - Calculate the standard deviation of these returns.
    Output:
        - A float representing the volatility.
    """
    price_history = raw_market_history_output.get("data", {}).get("price_history", [])
    if not price_history:
        raise ValueError("price_history not found in raw market history output.")
    if isinstance(price_history[0], list):
        prices = [entry[1] for entry in price_history if entry and len(entry) > 1]
    else:
        prices = price_history
    if len(prices) < 2:
        raise ValueError("Not enough data to compute volatility.")
    returns = [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]
    return statistics.stdev(returns)


def determineTrend(raw_market_history_output: Dict[str, Any], short_period: int, long_period: int) -> str:
    """
    Function Name: determineTrend
    Description: Determines the current trend (up, down, or sideways) by comparing short-term and long-term simple moving averages.
                 The raw API output is expected to have a "data" field containing "price_history",
                 which is a list of price data. If "price_history" is a list of lists, each sublist is assumed to be 
                 structured as [timestamp, price] and the price is extracted from index 1.
    Inputs:
        - raw_market_history_output: Raw API output from Mobula.get_market_history.
        - short_period: Number of recent data points for the short-term SMA.
        - long_period: Number of recent data points for the long-term SMA.
    Processing:
        - Extract "price_history" and convert it to a flat list of floats.
        - Compute the short-term SMA and the long-term SMA.
        - Compare the two averages: if short-term SMA > long-term SMA then trend is "up", if less then "down", else "sideways".
    Output:
        - A string indicating the trend ("up", "down", or "sideways").
    """
    price_history = raw_market_history_output.get("data", {}).get("price_history", [])
    if not price_history:
        raise ValueError("price_history not found in raw market history output.")
    if isinstance(price_history[0], list):
        prices = [entry[1] for entry in price_history if entry and len(entry) > 1]
    else:
        prices = price_history
    if len(prices) < long_period:
        raise ValueError("Not enough data to determine trend.")
    short_sma = sum(prices[-short_period:]) / short_period
    long_sma = sum(prices[-long_period:]) / long_period
    if short_sma > long_sma:
        return "up"
    elif short_sma < long_sma:
        return "down"
    else:
        return "sideways"

def marketCapToVolumeRatio(asset_data: Dict[str, Any]) -> float:
    """
    Function Name: marketCapToVolumeRatio
    Description:
        Computes market_cap / volume for a single asset dictionary that includes
        'market_cap' and 'volume' fields, which can come from endpoints like:
          - /market/query
          - /all
          - /market/multi-data (one item in the dataArray)
        etc.

    Raw snippet of one asset might be:
    {
      "market_cap": 1234567,
      "volume": 89012,
      ...
    }

    Processing:
      - ratio = market_cap / volume

    Output:
      - Float
    """
    market_cap = asset_data.get("market_cap")
    volume_val = asset_data.get("volume")
    if market_cap is None or volume_val is None or volume_val == 0:
        raise ValueError("Invalid or missing market_cap or volume in asset_data.")
    return market_cap / volume_val


def riskAdjustedReturn(market_history_output: Dict[str, Any]) -> float:
    """
    Function Name: riskAdjustedReturn
    Description:
        Computes a simplified Sharpe-like ratio from consecutive close prices
        from the /market/history endpoint. Risk-free rate = 0 for simplicity.

    Raw structure:
    {
      "data": {
        "price_history": [[timestamp, price]]
      }
    }

    Processing:
      - Extract prices from price history.
      - Compute daily (or per-interval) returns.
      - Average return / standard deviation (volatility).

    Output:
      - Float representing the ratio.
    """
    if "data" not in market_history_output:
        raise ValueError("No 'data' in market_history_output.")
    if "price_history" not in market_history_output["data"]:
        raise ValueError("No 'price_history' found.")

    ph = market_history_output["data"]["price_history"]
    if len(ph) < 2:
        raise ValueError("Not enough data to compute returns.")

    # Price history is [[timestamp, price]]
    prices = [row[1] for row in ph]

    returns = []
    for i in range(1, len(prices)):
        prev_price = prices[i - 1]
        curr_price = prices[i]
        if prev_price != 0:
            returns.append((curr_price - prev_price) / prev_price)

    if len(returns) < 2:
        raise ValueError("Not enough consecutive returns to compute stdev.")

    avg_return = sum(returns) / len(returns)
    vol = statistics.stdev(returns)
    if vol == 0:
        return float("inf")
    return avg_return / vol

def priceStabilityScore(market_history_output: Dict[str, Any], period: int = 20) -> float:
    """
    Function Name: priceStabilityScore
    Description:
        Computes a stability metric over the last `period` prices (e.g. 20)
        from the /market/history endpoint. Higher => more stable.

    Raw data:
    {
      "data": {
        "price_history": [[timestamp, price]]
      }
    }

    Processing:
      - Extract prices from the tail of the array.
      - Compute SMA of these prices.
      - Compute average absolute deviation from SMA.
      - normalized_dev = avg_dev / SMA.
      - return 1 / (1 + normalized_dev).

    Output:
      - Float (score).
    """
    if "data" not in market_history_output:
        raise ValueError("No 'data' in market_history_output.")
    if "price_history" not in market_history_output["data"]:
        raise ValueError("No 'price_history' found.")

    ph = market_history_output["data"]["price_history"]
    if len(ph) < period:
        raise ValueError("Not enough price data for the requested period.")

    prices = [row[1] for row in ph[-period:]]
    sma = sum(prices) / period

    deviations = [abs(p - sma) for p in prices]
    avg_dev = sum(deviations) / period

    if sma == 0:
        return 0.0

    normalized_deviation = avg_dev / sma
    return 1 / (1 + normalized_deviation)


def tradeActivityIntensity(trades_output: Dict[str, Any]) -> float:
    """
    Function Name: tradeActivityIntensity
    Description:
        Quantifies trade activity by counting the trades in
        the raw output from /market/trades/pair.

    Raw structure:
    {
      "data": [
        { "hash": "...", "date": 123456, "token_price": 1.23, ... },
        ...
      ]
    }

    Processing:
      - Return len(data).

    Output:
      - Float count of trades.
    """
    trades_list = trades_output.get("data", [])
    return float(len(trades_list))

def marketBreadthIndex(assets_data_output: Dict[str, Any]) -> float:
    """
    Function Name: marketBreadthIndex
    Description:
        Computes the proportion of assets with a positive 24h price change
        from the raw JSON returned by /all or /market/query.

    Raw structure (e.g. from /all):
    {
      "data": [
        {
          "price_change_24h": 3.2,
          ...
        },
        ...
      ]
    }

    Processing:
      - Count how many assets have price_change_24h > 0
      - Divide by total number of assets in the data array.

    Output:
      - Float between 0 and 1.
    """
    if "data" not in assets_data_output:
        raise ValueError("No 'data' in assets_data_output.")

    assets_list = assets_data_output["data"]
    if not assets_list:
        raise ValueError("Empty list of assets in 'data'.")

    positive_count = sum(1 for asset in assets_list if asset.get("price_change_24h", 0) > 0)
    return positive_count / len(assets_list)


def priceCorrelationMatrix(multi_history_output: Dict[str, Any]) -> np.ndarray:
    """
    Function Name: priceCorrelationMatrix
    Description:
        Computes pairwise Pearson correlation between price histories
        of multiple assets from /market/multi-history.

    Raw structure:
    {
      "data": [
        {
          "price_history": [[timestamp, price]],
          "symbol": "...",
          ...
        },
        ...
      ]
    }

    Processing:
      - For each asset in data, extract a list of prices.
      - Use numpy.corrcoef to form correlation matrix.

    Output:
      - np.ndarray (2D)
    """
    if "data" not in multi_history_output:
        raise ValueError("No 'data' in multi_history_output.")

    assets_data = multi_history_output["data"]
    if not assets_data:
        raise ValueError("Empty 'data' array.")

    # Extract price time series for each asset
    series_list = []
    for asset in assets_data:
        ph = asset.get("price_history", [])
        prices = [row[1] for row in ph] if ph else []
        series_list.append(prices)

    n = len(series_list)
    corr_matrix = np.zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(n):
            if i == j:
                corr_matrix[i, j] = 1.0
            else:
                try:
                    corr = np.corrcoef(series_list[i], series_list[j])[0, 1]
                    corr_matrix[i, j] = corr
                except:
                    corr_matrix[i, j] = 0.0

    return corr_matrix


def assetUtilizationRate(asset_data: Dict[str, Any]) -> float:
    """
    Function Name: assetUtilizationRate
    Description:
        Measures how actively an asset is traded relative to its circulating supply,
        usually volume / circulating_supply. Both typically appear in a single asset
        record from /all or /market/query or /market/multi-data.

    Example:
    {
      "volume": 1234567,
      "circulating_supply": 999999,
      ...
    }

    Output:
      - Float
    """
    volume_val = asset_data.get("volume")
    circ_supply = asset_data.get("circulating_supply")

    if volume_val is None or circ_supply is None or circ_supply == 0:
        raise ValueError("Invalid or missing 'volume' or 'circulating_supply'.")
    return volume_val / circ_supply

# ------------------------------------------------------------------------------
# 31. socialSentimentScore
# ------------------------------------------------------------------------------
# def socialSentimentScore(social_coin_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: socialSentimentScore
#     Description: Computes an overall social sentiment score for an asset.
#                  Data should be obtained from LunarCrush.get_coin_data (expected to have a "sentiment" field).
#     Inputs:
#         - social_coin_data_output: Dictionary containing social metrics.
#     Processing:
#         - Extract and return the "sentiment" field as a float.
#     Output:
#         - A float representing the social sentiment score.
#     """
#     sentiment = social_coin_data_output.get("sentiment")
#     if sentiment is None:
#         raise ValueError("Social sentiment data not provided.")
#     return float(sentiment)

# # ------------------------------------------------------------------------------
# # 32. altRank
# # ------------------------------------------------------------------------------
# def altRank(social_coin_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: altRank
#     Description: Returns the alternative rank score for an asset.
#                  Data should be obtained from LunarCrush.get_coin_data (expected to have an "alt_rank" field).
#     Inputs:
#         - social_coin_data_output: Dictionary containing social metrics.
#     Processing:
#         - Extract and return the "alt_rank" value.
#     Output:
#         - A float representing the alternative rank.
#     """
#     rank = social_coin_data_output.get("alt_rank")
#     if rank is None:
#         raise ValueError("altRank data not provided.")
#     return float(rank)

# # ------------------------------------------------------------------------------
# # 33. galaxyScore
# # ------------------------------------------------------------------------------
# def galaxyScore(social_coin_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: galaxyScore
#     Description: Retrieves the LunarCrush Galaxy Score for an asset.
#                  Data should be obtained from LunarCrush.get_coin_data (expected to have a "galaxy_score" field).
#     Inputs:
#         - social_coin_data_output: Dictionary containing social metrics.
#     Processing:
#         - Extract and return the "galaxy_score" value.
#     Output:
#         - A float representing the Galaxy Score.
#     """
#     score = social_coin_data_output.get("galaxy_score")
#     if score is None:
#         raise ValueError("Galaxy Score not provided.")
#     return float(score)

# # ------------------------------------------------------------------------------
# # 34. marketSentimentIndex
# # ------------------------------------------------------------------------------
# def marketSentimentIndex(market_data_output: Dict[str, Any], social_sentiment_score: float) -> float:
#     """
#     Function Name: marketSentimentIndex
#     Description: Computes a composite market sentiment index by integrating technical market data and social sentiment.
#                  Market data should be obtained from Mobula.get_market_data, and social sentiment from LunarCrush.get_coin_data.
#     Inputs:
#         - market_data_output: Dictionary containing technical metrics (e.g., "price", "volume").
#         - social_sentiment_score: A float representing the social sentiment score.
#     Processing:
#         - Calculate market volatility from a provided "price_history" field if available (or assume a constant).
#           For demonstration, we compute an inverse volatility factor using a placeholder volatility value.
#         - Combine the inverse volatility factor with the social sentiment score (e.g., via averaging).
#     Output:
#         - A float representing the composite market sentiment index.
#     """
#     # For demonstration, we'll assume a constant volatility factor if no price history is provided.
#     volatility_factor = 0.5  # Placeholder value; in practice, compute from price history.
#     technical_index = 1 / volatility_factor if volatility_factor != 0 else 0
#     return (technical_index + social_sentiment_score) / 2

# # ------------------------------------------------------------------------------
# # 35. socialEngagementRate
# # ------------------------------------------------------------------------------
# def socialEngagementRate(social_coin_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: socialEngagementRate
#     Description: Calculates the average social engagement per post.
#                  Data should be obtained from LunarCrush.get_coin_data (fields "interactions_24h" and "num_posts" are expected).
#     Inputs:
#         - social_coin_data_output: Dictionary containing social metrics.
#     Processing:
#         - Compute engagement_rate = interactions_24h / num_posts.
#     Output:
#         - A float representing the average social engagement rate.
#     """
#     interactions = social_coin_data_output.get("interactions_24h")
#     num_posts = social_coin_data_output.get("num_posts")
#     if interactions is None or num_posts is None or num_posts == 0:
#         raise ValueError("Insufficient social engagement data.")
#     return interactions / num_posts

# # ------------------------------------------------------------------------------
# # 36. compositeRiskScore
# # ------------------------------------------------------------------------------
# def compositeRiskScore(market_volatility: float, social_volatility: float) -> float:
#     """
#     Function Name: compositeRiskScore
#     Description: Computes a composite risk score by averaging market volatility and social sentiment volatility.
#                  Market volatility may be computed from Mobula.get_market_history and social volatility from historical social sentiment data.
#     Inputs:
#         - market_volatility: A float representing market volatility.
#         - social_volatility: A float representing social sentiment volatility.
#     Processing:
#         - Compute the average of the two volatility measures.
#     Output:
#         - A float representing the composite risk score.
#     """
#     return (market_volatility + social_volatility) / 2

# # ------------------------------------------------------------------------------
# # 37. liquidityAdjustedPrice
# # ------------------------------------------------------------------------------
# def liquidityAdjustedPrice(market_data_output: Dict[str, Any], pair_output: Dict[str, Any]) -> float:
#     """
#     Function Name: liquidityAdjustedPrice
#     Description: Adjusts the current price based on liquidity conditions.
#                  Data should be obtained from Mobula.get_market_data (for "price") and a single trading pair object from Mobula.get_market_pairs (for "liquidity").
#     Inputs:
#         - market_data_output: Dictionary containing the current "price".
#         - pair_output: Dictionary representing a trading pair, expected to contain a "liquidity" field.
#     Processing:
#         - Compute a liquidity factor as liquidity divided by an arbitrary normalization constant (e.g., 1000).
#         - Adjust the price: adjusted_price = price * (1 + liquidity_factor).
#     Output:
#         - A float representing the liquidity-adjusted price.
#     """
#     price_val = market_data_output.get("price")
#     liq = pair_output.get("liquidity")
#     if price_val is None or liq is None:
#         raise ValueError("Required data missing for liquidity adjustment.")
#     normalization_constant = 1000.0  # This constant may be tuned as needed.
#     liquidity_factor = liq / normalization_constant
#     return price_val * (1 + liquidity_factor)

# # ------------------------------------------------------------------------------
# # 38. decentralizationScore
# # ------------------------------------------------------------------------------
# def decentralizationScore(token_holders_output: Dict[str, Any]) -> float:
#     """
#     Function Name: decentralizationScore
#     Description: Evaluates the decentralization of an asset by measuring token holder concentration.
#                  Data should be obtained from Mobula.get_market_token_holders.
#     Inputs:
#         - token_holders_output: Dictionary containing token holder data (expected to have a "data" list and "total_count").
#     Processing:
#         - Sort the holders by their "holding" amount.
#         - Sum the holdings of the top 10 holders and divide by the total holdings.
#     Output:
#         - A float representing the decentralization score (a higher score indicates greater concentration).
#     """
#     holders = token_holders_output.get("data", [])
#     if not holders:
#         raise ValueError("No token holder data provided.")
#     sorted_holders = sorted(holders, key=lambda x: x.get("holding", 0), reverse=True)
#     top_holdings = sum(holder.get("holding", 0) for holder in sorted_holders[:10])
#     total_holdings = sum(holder.get("holding", 0) for holder in holders)
#     if total_holdings == 0:
#         raise ValueError("Total holdings is zero; cannot compute decentralization.")
#     return top_holdings / total_holdings

# # ------------------------------------------------------------------------------
# # 39. socialVolatilityIndex
# # ------------------------------------------------------------------------------
# def socialVolatilityIndex(social_sentiment_history: List[float]) -> float:
#     """
#     Function Name: socialVolatilityIndex
#     Description: Measures the volatility of social sentiment over time.
#                  Social sentiment history should be a list of sentiment scores collected over multiple time periods (from LunarCrush.get_topic_summary or similar).
#     Inputs:
#         - social_sentiment_history: List of social sentiment scores (floats).
#     Processing:
#         - Compute the standard deviation of the sentiment scores.
#     Output:
#         - A float representing the social volatility index.
#     """
#     if len(social_sentiment_history) < 2:
#         raise ValueError("Insufficient social sentiment data to compute volatility.")
#     return statistics.stdev(social_sentiment_history)

# # ------------------------------------------------------------------------------
# # 40. marketMomentumScore
# # ------------------------------------------------------------------------------
# def marketMomentumScore(market_history_output: List[float], short_period: int, long_period: int) -> float:
#     """
#     Function Name: marketMomentumScore
#     Description: Quantifies market momentum by comparing short-term and long-term moving averages.
#                  Data should be extracted from the "price_history" field of Mobula.get_market_history.
#     Inputs:
#         - market_history_output: List of historical price values.
#         - short_period: Period for computing the short-term SMA.
#         - long_period: Period for computing the long-term SMA.
#     Processing:
#         - Compute the short-term SMA and the long-term SMA.
#         - Calculate the momentum score = (short_SMA - long_SMA) / long_SMA.
#     Output:
#         - A float representing the market momentum score.
#     """
#     if len(market_history_output) < long_period:
#         raise ValueError("Not enough data to compute momentum.")
#     short_sma = sum(market_history_output[-short_period:]) / short_period
#     long_sma = sum(market_history_output[-long_period:]) / long_period
#     if long_sma == 0:
#         raise ValueError("Long-term SMA is zero; cannot compute momentum.")
#     return (short_sma - long_sma) / long_sma

# # ------------------------------------------------------------------------------
# # End of Batch 2 (Functions 21-40)
# # ------------------------------------------------------------------------------

# # ----- Composite / Social-Hybrid Functions (Functions 41-52) -----

# def yieldEfficiencyScore(yield_platform_output: Dict[str, Any], market_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: yieldEfficiencyScore
#     Description: Assesses yield efficiency by comparing the yield rate from a yield platform
#                  with the asset's current price. Data should be obtained from a yield platform API 
#                  and Mobula.get_market_data.
#     Inputs:
#         - yield_platform_output: Dictionary containing yield-related data (expected field: "yield_rate").
#         - market_data_output: Dictionary from Mobula.get_market_data containing "price".
#     Processing:
#         - Compute yield efficiency = yield_rate / price.
#     Output:
#         - A float representing the yield efficiency score.
#     """
#     yield_rate = yield_platform_output.get("yield_rate")
#     price_val = market_data_output.get("price")
#     if yield_rate is None or price_val is None or price_val == 0:
#         raise ValueError("Required yield or price data missing.")
#     return yield_rate / price_val

# def socialMarketDivergence(market_history_output: List[float], social_sentiment_trend: List[float]) -> float:
#     """
#     Function Name: socialMarketDivergence
#     Description: Quantifies the divergence between market price trends and social sentiment trends.
#                  Price data is from Mobula.get_market_history ("price_history") and social sentiment trend 
#                  should be collected over time from LunarCrush.get_topic_summary.
#     Inputs:
#         - market_history_output: List of historical price values.
#         - social_sentiment_trend: List of historical social sentiment scores.
#     Processing:
#         - Normalize both series and compute the average absolute difference.
#     Output:
#         - A float representing the divergence (higher value indicates greater divergence).
#     """
#     if not market_history_output or not social_sentiment_trend:
#         raise ValueError("Both price and social sentiment data are required.")
#     # Normalize by dividing by their respective max values (avoid division by zero)
#     max_price = max(market_history_output) if max(market_history_output) != 0 else 1
#     max_sent = max(social_sentiment_trend) if max(social_sentiment_trend) != 0 else 1
#     norm_prices = [p / max_price for p in market_history_output]
#     norm_sentiments = [s / max_sent for s in social_sentiment_trend]
#     n = min(len(norm_prices), len(norm_sentiments))
#     divergence = sum(abs(norm_prices[i] - norm_sentiments[i]) for i in range(n)) / n
#     return divergence

# def onChainActivityScore(wallet_transactions_output: List[Dict[str, Any]]) -> float:
#     """
#     Function Name: onChainActivityScore
#     Description: Gauges on-chain activity by measuring the frequency of transactions.
#                  Data should be obtained from Mobula.get_wallet_transactions.
#     Inputs:
#         - wallet_transactions_output: List of transaction records.
#     Processing:
#         - Count the number of transactions (as a simple proxy for activity).
#     Output:
#         - A float representing the on-chain activity score.
#     """
#     if not wallet_transactions_output:
#         return 0.0
#     return float(len(wallet_transactions_output))

# def socialMediaInfluenceScore(social_coin_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: socialMediaInfluenceScore
#     Description: Quantifies social media influence by combining engagement and reach metrics.
#                  Data should be obtained from LunarCrush.get_coin_data (fields like "social_volume_24h" and "interactions_24h").
#     Inputs:
#         - social_coin_data_output: Dictionary containing social engagement metrics.
#     Processing:
#         - For example, compute influence = (social_volume_24h + interactions_24h) / 2.
#     Output:
#         - A float representing the social media influence score.
#     """
#     social_volume = social_coin_data_output.get("social_volume_24h")
#     interactions = social_coin_data_output.get("interactions_24h")
#     if social_volume is None or interactions is None:
#         raise ValueError("Required social engagement data missing.")
#     return (social_volume + interactions) / 2

# def aggregateAssetScore(market_data_output: Dict[str, Any], social_coin_data_output: Dict[str, Any], wallet_portfolio_output: Dict[str, Any]) -> float:
#     """
#     Function Name: aggregateAssetScore
#     Description: Produces a comprehensive score summarizing overall asset performance by integrating market data,
#                  social metrics, and wallet portfolio data.
#                  Data should be obtained from Mobula.get_market_data, LunarCrush.get_coin_data, and Mobula.get_wallet_portfolio.
#     Inputs:
#         - market_data_output: Dictionary with key market metrics such as "price" and "market_cap".
#         - social_coin_data_output: Dictionary with social metrics (e.g., "galaxy_score").
#         - wallet_portfolio_output: Dictionary containing portfolio data (e.g., "total_wallet_balance").
#     Processing:
#         - Compute a weighted average of normalized metrics from each source.
#     Output:
#         - A float representing the aggregate asset score.
#     """
#     price_val = market_data_output.get("price", 0)
#     market_cap = market_data_output.get("market_cap", 0)
#     galaxy = float(social_coin_data_output.get("galaxy_score", 0))
#     portfolio_balance = wallet_portfolio_output.get("total_wallet_balance", 0)
#     # Example weighted sum (weights are adjustable)
#     score = (0.4 * (price_val / (market_cap + 1e-6)) + 0.4 * galaxy + 0.2 * portfolio_balance)
#     return score

# def tokenHolderConcentration(token_holders_output: Dict[str, Any]) -> float:
#     """
#     Function Name: tokenHolderConcentration
#     Description: Measures token holder concentration by computing the proportion held by the top holders.
#                  Data should be obtained from Mobula.get_market_token_holders.
#     Inputs:
#         - token_holders_output: Dictionary with a "data" list of token holder records and "total_count".
#     Processing:
#         - Sort holders by "holding" amount and compute the sum for the top 10 holders.
#         - Divide the top 10 sum by the total holdings.
#     Output:
#         - A float representing the concentration ratio (higher value indicates greater concentration).
#     """
#     holders = token_holders_output.get("data", [])
#     if not holders:
#         raise ValueError("No token holder data provided.")
#     sorted_holders = sorted(holders, key=lambda x: x.get("holding", 0), reverse=True)
#     top_total = sum(holder.get("holding", 0) for holder in sorted_holders[:10])
#     total_total = sum(holder.get("holding", 0) for holder in holders)
#     if total_total == 0:
#         raise ValueError("Total holdings is zero; cannot compute concentration.")
#     return top_total / total_total

# def priceReactionTime(market_trades_output: List[Dict[str, Any]], event_timestamp: float) -> float:
#     """
#     Function Name: priceReactionTime
#     Description: Determines the reaction time between a significant event and the subsequent price change.
#                  Trade data should be obtained from Mobula.get_market_trades_pair.
#     Inputs:
#         - market_trades_output: List of trade records, each expected to include a "timestamp" field.
#         - event_timestamp: Timestamp of the event (in seconds or milliseconds, as provided).
#     Processing:
#         - Identify the first trade with a timestamp greater than the event timestamp and compute the time difference.
#     Output:
#         - A float representing the reaction time (in the same time units as provided).
#     """
#     if not market_trades_output:
#         raise ValueError("No trade data provided.")
#     for trade in market_trades_output:
#         trade_ts = trade.get("timestamp")
#         if trade_ts and trade_ts > event_timestamp:
#             return trade_ts - event_timestamp
#     return float('inf')  # No reaction found

# def newsImpactScore(news_article_output: Dict[str, Any], subsequent_market_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: newsImpactScore
#     Description: Quantifies the market impact of a news event.
#                  Data should be obtained from LunarCrush.get_topic_news for the news article and Mobula.get_market_data for subsequent price data.
#     Inputs:
#         - news_article_output: Dictionary containing news metadata (expected to include "post_sentiment").
#         - subsequent_market_data_output: Dictionary containing market data post-event (expected field: "price_change_24h").
#     Processing:
#         - Multiply the news "post_sentiment" by the 24h price change percentage.
#     Output:
#         - A float representing the news impact score.
#     """
#     sentiment = news_article_output.get("post_sentiment")
#     price_change = subsequent_market_data_output.get("price_change_24h", 0)
#     if sentiment is None:
#         raise ValueError("News sentiment not provided.")
#     return float(sentiment) * price_change

# def volatilityBreakoutIndicator(market_history_output: List[float], current_market_data_output: Dict[str, Any], threshold: float = 0.05) -> bool:
#     """
#     Function Name: volatilityBreakoutIndicator
#     Description: Flags potential breakout opportunities when market volatility and volume exceed defined thresholds.
#                  Data should be obtained from Mobula.get_market_history and Mobula.get_market_data.
#     Inputs:
#         - market_history_output: List of historical price values.
#         - current_market_data_output: Dictionary containing current market data (expected field: "volume").
#         - threshold: A float threshold for volatility (default is 0.05).
#     Processing:
#         - Calculate volatility using calculateVolatility.
#         - Check if volatility exceeds the threshold and if current volume is above an arbitrary high value.
#     Output:
#         - A boolean indicating whether a breakout is signaled.
#     """
#     vol = calculateVolatility(market_history_output)
#     volume_val = current_market_data_output.get("volume", 0)
#     # For demonstration, define high volume arbitrarily as > 1000.
#     return vol > threshold and volume_val > 1000

# def onChainSentimentComposite(social_sentiment_history: List[float], wallet_transactions_output: List[Dict[str, Any]]) -> float:
#     """
#     Function Name: onChainSentimentComposite
#     Description: Merges off-chain social sentiment with on-chain activity metrics to produce a composite sentiment measure.
#                  Social sentiment history should be obtained from LunarCrush.get_topic_summary (or similar),
#                  and transaction data from Mobula.get_wallet_transactions.
#     Inputs:
#         - social_sentiment_history: List of social sentiment scores over time.
#         - wallet_transactions_output: List of wallet transaction records.
#     Processing:
#         - Compute the average social sentiment.
#         - Compute an on-chain activity metric (e.g., normalized transaction count).
#         - Return the average of these two normalized values.
#     Output:
#         - A float representing the composite on-chain sentiment score.
#     """
#     if not social_sentiment_history:
#         raise ValueError("Social sentiment history is required.")
#     avg_sentiment = sum(social_sentiment_history) / len(social_sentiment_history)
#     tx_count = len(wallet_transactions_output) if wallet_transactions_output else 0
#     normalized_tx = tx_count / 100.0  # Arbitrary normalization factor
#     return (avg_sentiment + normalized_tx) / 2

# def socialEngagementVolatility(engagement_history: List[float]) -> float:
#     """
#     Function Name: socialEngagementVolatility
#     Description: Measures the volatility of social engagement over time.
#                  Engagement data should be a list of engagement metrics (e.g., interactions per post) collected over time.
#     Inputs:
#         - engagement_history: List of social engagement values.
#     Processing:
#         - Compute the standard deviation of the engagement values.
#     Output:
#         - A float representing the volatility of social engagement.
#     """
#     if len(engagement_history) < 2:
#         raise ValueError("Insufficient engagement data to compute volatility.")
#     return statistics.stdev(engagement_history)

# def projectCredibilityScore(asset_metadata_output: Dict[str, Any], social_coin_data_output: Dict[str, Any]) -> float:
#     """
#     Function Name: projectCredibilityScore
#     Description: Evaluates the credibility and long-term potential of a project by combining asset metadata and social indicators.
#                  Data should be obtained from Mobula.get_metadata and LunarCrush.get_coin_data.
#     Inputs:
#         - asset_metadata_output: Dictionary containing asset metadata (e.g., "website", "description").
#         - social_coin_data_output: Dictionary containing social metrics (e.g., "galaxy_score").
#     Processing:
#         - Award points for having a website and a detailed description.
#         - Combine these with the social "galaxy_score" to produce a composite credibility score.
#     Output:
#         - A float representing the project credibility score.
#     """
#     website = asset_metadata_output.get("website")
#     description = asset_metadata_output.get("description", "")
#     social_score = float(social_coin_data_output.get("galaxy_score", 0))
#     meta_score = (1 if website else 0) + (len(description) / 1000.0)
#     return meta_score + social_score

# # ----- Additional Mobula-Specific Functions (Functions 53-62) -----

# def blockchainLiquiditySpread(blockchain_pairs_output: Dict[str, Any]) -> float:
#     """
#     Function Name: blockchainLiquiditySpread
#     Description: Measures the dispersion of liquidity across trading pairs on a specific blockchain.
#                  Data should be obtained from Mobula.get_blockchain_pairs, which returns a "data" list of pair objects.
#     Inputs:
#         - blockchain_pairs_output: Dictionary containing a "data" list of trading pairs. Each pair should have a "pair" object with token details and a "liquidity" field.
#     Processing:
#         - Iterate through the list, extract liquidity values, and compute the coefficient of variation (std. dev. / mean).
#     Output:
#         - A float representing the liquidity spread.
#     """
#     pairs = blockchain_pairs_output.get("data", [])
#     if not pairs:
#         raise ValueError("No trading pair data available.")
#     liquidities = [pair.get("liquidity", 0) for pair in pairs if pair.get("liquidity") is not None]
#     if not liquidities or sum(liquidities) == 0:
#         raise ValueError("Liquidity values missing or zero.")
#     mean_liq = sum(liquidities) / len(liquidities)
#     stdev_liq = statistics.stdev(liquidities)
#     return stdev_liq / mean_liq

# def blockchainVolumeChange(blockchain_stats_output: Dict[str, Any]) -> float:
#     """
#     Function Name: blockchainVolumeChange
#     Description: Retrieves the 24-hour volume change for a specific blockchain.
#                  Data should be obtained from Mobula.get_blockchain_stats.
#     Inputs:
#         - blockchain_stats_output: Dictionary containing a "volume_change_24h" field.
#     Processing:
#         - Extract and return the "volume_change_24h" value.
#     Output:
#         - A float representing the 24-hour volume change percentage.
#     """
#     vol_change = blockchain_stats_output.get("volume_change_24h")
#     if vol_change is None:
#         raise ValueError("Volume change data not provided.")
#     return float(vol_change)

# def cefiFundingRate(cefi_output: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Function Name: cefiFundingRate
#     Description: Retrieves funding rate data from centralized exchanges.
#                  Data should be obtained from Mobula.get_cefi_funding_rate.
#     Inputs:
#         - cefi_output: Dictionary containing funding rate details (e.g., "binanceFundingRate", "deribitFundingRate", and "queryDetails").
#     Processing:
#         - Return the funding rate information as provided.
#     Output:
#         - A dictionary with funding rate details.
#     """
#     if not cefi_output:
#         raise ValueError("Cefi funding rate data not provided.")
#     return cefi_output

# def tokenPerformanceComparison(market_token_vs_market_output: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Function Name: tokenPerformanceComparison
#     Description: Compares a token's performance against overall market metrics.
#                  Data should be obtained from Mobula.get_market_token_vs_market.
#     Inputs:
#         - market_token_vs_market_output: Dictionary containing comparative token market data.
#     Processing:
#         - Return the provided comparative data.
#     Output:
#         - A dictionary with token performance comparison metrics.
#     """
#     if not market_token_vs_market_output:
#         raise ValueError("Token vs market data not provided.")
#     return market_token_vs_market_output

# def customMarketQueryData(query_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#     """
#     Function Name: customMarketQueryData
#     Description: Executes a custom market query based on provided filtering and sorting parameters.
#                  This function serves as a wrapper for Mobula.get_market_query.
#     Inputs:
#         - query_params: Dictionary containing query parameters (e.g., "sortBy", "sortOrder", "filters", "blockchain", "blockchains", "limit", "offset").
#     Processing:
#         - Return the list of market data entries matching the query.
#     Output:
#         - A list of dictionaries representing market data.
#     """
#     # In practice, you would call Mobula.get_market_query(query_params) and return its result.
#     return query_params.get("results", [])

# def customTokenQueryData(query_params: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Function Name: customTokenQueryData
#     Description: Retrieves token-specific market data based on custom query parameters.
#                  This function serves as a wrapper for Mobula.get_market_query_token.
#     Inputs:
#         - query_params: Dictionary containing token query parameters (e.g., "sortField", "sortOrder", "filters", "blockchain", "blockchains", "unlistedAssets").
#     Processing:
#         - Return the token market data as provided.
#     Output:
#         - A dictionary representing token market data.
#     """
#     # In practice, you would call Mobula.get_market_query_token(query_params).
#     return query_params  # Placeholder

# def marketNFTAnalysis(market_nft_output: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Function Name: marketNFTAnalysis
#     Description: Analyzes NFT market trends by extracting key metrics from NFT market data.
#                  Data should be obtained from Mobula.get_market_nft.
#     Inputs:
#         - market_nft_output: Dictionary containing NFT market data (expected fields: "price", "priceETH").
#     Processing:
#         - Extract key metrics such as NFT price in USD and ETH.
#     Output:
#         - A dictionary summarizing NFT market analysis.
#     """
#     if not market_nft_output:
#         raise ValueError("NFT market data not provided.")
#     return {
#         "price_usd": market_nft_output.get("price"),
#         "price_eth": market_nft_output.get("priceETH")
#     }

# def walletTransactionAnalysis(wallet_transactions_output: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Function Name: walletTransactionAnalysis
#     Description: Analyzes wallet transaction patterns to assess activity trends.
#                  Data should be obtained from Mobula.get_wallet_transactions.
#     Inputs:
#         - wallet_transactions_output: Dictionary containing wallet transaction data.
#     Processing:
#         - Compute metrics such as total number of transactions and average transaction value.
#     Output:
#         - A dictionary containing analysis results (e.g., "transaction_count", "average_transaction_value").
#     """
#     transactions = wallet_transactions_output.get("data", [])
#     count = len(transactions) if isinstance(transactions, list) else 0
#     values = [tx.get("value", 0) for tx in transactions] if isinstance(transactions, list) else []
#     avg_value = sum(values) / count if count > 0 else 0
#     return {
#         "transaction_count": count,
#         "average_transaction_value": avg_value
#     }

# def blockchainStatsComposite(blockchain_stats_output: Dict[str, Any]) -> float:
#     """
#     Function Name: blockchainStatsComposite
#     Description: Combines various blockchain statistics into a composite index.
#                  Data should be obtained from Mobula.get_blockchain_stats.
#     Inputs:
#         - blockchain_stats_output: Dictionary containing statistics (e.g., "volume_history", "volume_change_24h", "liquidity_history", "tokens_history").
#     Processing:
#         - Normalize key metrics and compute their average as a composite score.
#     Output:
#         - A float representing the composite blockchain statistics score.
#     """
#     vol_change = blockchain_stats_output.get("volume_change_24h", 0)
#     # For demonstration, we simply return the volume change as a proxy.
#     return float(vol_change)

# def assetMetadataComposite(asset_metadata_output: Dict[str, Any], social_coin_data_output: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Function Name: assetMetadataComposite
#     Description: Merges asset metadata with social data to produce an overall composite score.
#                  Data should be obtained from Mobula.get_metadata and LunarCrush.get_coin_data.
#     Inputs:
#         - asset_metadata_output: Dictionary containing asset metadata (e.g., "website", "description").
#         - social_coin_data_output: Dictionary containing social metrics (e.g., "galaxy_score").
#     Processing:
#         - Combine selected metadata (presence of website, length of description) with the galaxy score.
#     Output:
#         - A dictionary with the composite score and its components.
#     """
#     meta_score = 0
#     if asset_metadata_output.get("website"):
#         meta_score += 1
#     description = asset_metadata_output.get("description", "")
#     meta_score += len(description) / 1000.0  # Arbitrary normalization
#     social_score = float(social_coin_data_output.get("galaxy_score", 0))
#     composite = meta_score + social_score
#     return {"composite_score": composite, "meta_score": meta_score, "social_score": social_score}

# # ----- Additional Function: getTokensDataOnBlockchain (Function 63) -----

def getTokensDataOnBlockchain(blockchain_pairs_output: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Function Name: getTokensDataOnBlockchain
    Description: Extracts all unique token data and their aggregated statistics from the blockchain pairs output.
                 Data should be obtained from Mobula.get_blockchain_pairs. It iterates over each trading pair,
                 extracts token details from the "pair" object (specifically "token0" and "token1"),
                 and aggregates unique tokens based on a unique identifier (preferably "symbol", or "address" if missing).
    Inputs:
        - blockchain_pairs_output: Dictionary from Mobula.get_blockchain_pairs, expected to contain:
            {
              "data": [
                  {
                      "pair": {
                          "token0": { ... },
                          "token1": { ... }
                      },
                      ...
                  },
                  ...
              ],
              "factories": { ... }
            }
    Processing:
        - Initialize an empty dictionary.
        - Iterate over each pair in "data" and extract tokens from the "pair" object.
        - For each token, determine a unique identifier (using "symbol" or fallback to "address") and add to the dictionary if not already present.
    Output:
        - A dictionary mapping unique token identifiers to their token data.
          Example:
            {
              "ABC": { token data for ABC },
              "XYZ": { token data for XYZ },
              ...
            }
    """
    tokens_dict = {}
    pairs = blockchain_pairs_output.get("data", [])
    if not pairs:
        raise ValueError("No trading pair data found.")
    for pair_item in pairs:
        pair = pair_item.get("pair")
        if not pair:
            continue
        for token_key in ["token0", "token1"]:
            token = pair.get(token_key)
            if token and isinstance(token, dict):
                token_id = token.get("symbol") or token.get("address")
                if token_id and token_id not in tokens_dict:
                    tokens_dict[token_id] = token
    return tokens_dict