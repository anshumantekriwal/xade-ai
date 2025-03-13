# file: analytics_functions.py
"""
This file contains a set of functions that parse raw Mobula API outputs (and in one case, LunarCrush)
in order to compute various analytics metrics. Each function has been updated to match the data
shapes specified in mobula.yaml (the 'raw' API responses), rather than relying on simplified or
pre-processed data.
"""

import statistics
import numpy as np
from typing import Any, Dict, List
import json

def socialSentimentScore(social_coin_data_output: Dict[str, Any]) -> float:
    """
    Function Name: socialSentimentScore
    Description:
        Computes an overall social sentiment score for an asset.
        Data should come from a social API (e.g. LunarCrush.get_coin_data),
        expected to have "sentiment" as a float field.

    Example Input:
    {
      "sentiment": 3.4,
      ...
    }

    Output: float
    """
    sentiment = social_coin_data_output.get("data")
    print(sentiment)
    if sentiment is None:
        raise ValueError("Social sentiment data ('sentiment') not provided.")
    return float(sentiment)

# ------------------------------------------------------------------------------
# 32. altRank
# ------------------------------------------------------------------------------
def altRank(social_coin_data_output: Dict[str, Any]) -> float:
    """
    Function Name: altRank
    Description:
        Returns the altRank from a social API (e.g. LunarCrush).
        Expects "alt_rank" in the dictionary.

    Example Input:
    {
      "alt_rank": 57,
      ...
    }

    Output: float
    """
    rank = social_coin_data_output.get("alt_rank")
    if rank is None:
        raise ValueError("altRank data not provided.")
    return float(rank)

# ------------------------------------------------------------------------------
# 33. galaxyScore
# ------------------------------------------------------------------------------
def galaxyScore(social_coin_data_output: Dict[str, Any]) -> float:
    """
    Function Name: galaxyScore
    Description:
        Retrieves the Galaxy Score from a social API (e.g. LunarCrush).
        Expects "galaxy_score" in the dictionary.

    Example Input:
    {
      "galaxy_score": 64.23,
      ...
    }

    Output: float
    """
    score = social_coin_data_output.get("galaxy_score")
    if score is None:
        raise ValueError("Galaxy Score not provided.")
    return float(score)

# ------------------------------------------------------------------------------
# 34. marketSentimentIndex
# ------------------------------------------------------------------------------
def marketSentimentIndex(market_data_output: Dict[str, Any], social_sentiment_score: float) -> float:
    """
    Function Name: marketSentimentIndex
    Description:
        Combines technical market volatility (e.g. from Mobula /market/history)
        with a social sentiment score (from a LunarCrush-like API) to create
        a composite index.

    Processing:
      - Attempt to parse close prices from market_data_output["data"]["price_history"].
      - Compute a volatility measure, invert it for a 'technical_index'.
      - Average that with social_sentiment_score.

    Output: float
    """
    import statistics

    # Default fallback if no valid price history
    technical_index = 1.0

    if ("data" in market_data_output
        and isinstance(market_data_output["data"], dict)
        and "price_history" in market_data_output["data"]):
        ph = market_data_output["data"]["price_history"]
        if len(ph) > 1:
            closes = [row[4] for row in ph]
            returns = []
            for i in range(1, len(closes)):
                prev_close = closes[i - 1]
                if prev_close != 0:
                    returns.append((closes[i] - prev_close) / prev_close)
            if len(returns) > 1:
                vol = statistics.stdev(returns)
                if vol != 0:
                    technical_index = 1 / vol
                else:
                    technical_index = 999999.0

    return (technical_index + social_sentiment_score) / 2.0

# ------------------------------------------------------------------------------
# 35. socialEngagementRate
# ------------------------------------------------------------------------------
def socialEngagementRate(social_coin_data_output: Dict[str, Any]) -> float:
    """
    Function Name: socialEngagementRate
    Description:
        Calculates average social engagement per post from a social API
        (e.g. "interactions_24h" / "num_posts").

    Example Input:
    {
      "interactions_24h": 24000,
      "num_posts": 80,
      ...
    }

    Output: float
    """
    interactions = social_coin_data_output.get("interactions_24h")
    num_posts = social_coin_data_output.get("num_posts")
    if interactions is None or num_posts is None or num_posts == 0:
        raise ValueError("Insufficient social engagement data.")
    return interactions / num_posts

# ------------------------------------------------------------------------------
# 36. compositeRiskScore
# ------------------------------------------------------------------------------
def compositeRiskScore(market_volatility: float, social_volatility: float) -> float:
    """
    Function Name: compositeRiskScore
    Description:
        Averages market volatility and social sentiment volatility into a single
        risk score.

    Output: float
    """
    return (market_volatility + social_volatility) / 2.0

# ------------------------------------------------------------------------------
# 37. liquidityAdjustedPrice
# ------------------------------------------------------------------------------
def liquidityAdjustedPrice(market_data_output: Dict[str, Any], pair_output: Dict[str, Any]) -> float:
    """
    Function Name: liquidityAdjustedPrice
    Description:
        Adjusts the current price (from 'market_data_output') by a liquidity factor
        (from 'pair_output').

    Example:
      - market_data_output = {"price": 1.23}
      - pair_output = {"liquidity": 4500}

    Output: float
    """
    price_val = market_data_output.get("price")
    if price_val is None:
        raise ValueError("market_data_output missing 'price'.")
    liq = pair_output.get("liquidity")
    if liq is None:
        raise ValueError("pair_output missing 'liquidity'.")

    normalization_constant = 1000.0
    liquidity_factor = liq / normalization_constant
    return price_val * (1 + liquidity_factor)

# ------------------------------------------------------------------------------
# 38. decentralizationScore
# ------------------------------------------------------------------------------
def decentralizationScore(token_holders_output: Dict[str, Any]) -> float:
    """
    Function Name: decentralizationScore
    Description:
        Evaluates decentralization by summing the top 10 holders' amounts
        and comparing to total. Data from Mobula's /market/token/holders.

    Raw example:
    {
      "data": [
        {
          "address": "...",
          "amount": 1234,
          ...
        },
        ...
      ],
      "total_count": ...
    }

    Output: float
    """
    holders = token_holders_output.get("data", [])
    if not isinstance(holders, list) or not holders:
        raise ValueError("No token holder data provided.")
    sorted_holders = sorted(holders, key=lambda h: h.get("amount", 0), reverse=True)
    top_10_amount = sum(h.get("amount", 0) for h in sorted_holders[:10])
    total_amount = sum(h.get("amount", 0) for h in sorted_holders)
    if total_amount == 0:
        raise ValueError("Total holdings is zero; cannot compute ratio.")
    return top_10_amount / total_amount

# ------------------------------------------------------------------------------
# 39. socialVolatilityIndex
# ------------------------------------------------------------------------------
def socialVolatilityIndex(social_sentiment_history: List[float]) -> float:
    """
    Function Name: socialVolatilityIndex
    Description:
        Measures the volatility (std. dev.) of social sentiment scores.

    Input: e.g. [3.0, 3.4, 2.8, 4.1, ...]

    Output: float
    """
    if len(social_sentiment_history) < 2:
        raise ValueError("Need at least 2 sentiment points to compute volatility.")
    return statistics.stdev(social_sentiment_history)

# ------------------------------------------------------------------------------
# 40. marketMomentumScore
# ------------------------------------------------------------------------------
def marketMomentumScore(market_history_output: Dict[str, Any], short_period: int, long_period: int) -> float:
    """
    Function Name: marketMomentumScore
    Description:
        Calculates a momentum indicator by comparing short-term vs. long-term
        SMAs of the close price from Mobula's /market/history.

    Raw /market/history example:
    {
      "data": {
        "price_history": [
          [time, open, high, low, close, volume],
          ...
        ]
      }
    }

    Output: float (momentum score).
    """
    if "data" not in market_history_output or not isinstance(market_history_output["data"], dict):
        raise ValueError("market_history_output missing 'data'.")
    if "price_history" not in market_history_output["data"]:
        raise ValueError("No 'price_history' found in market_history_output['data'].")

    ph = market_history_output["data"]["price_history"]
    closes = [row[4] for row in ph]
    if len(closes) < long_period:
        raise ValueError("Not enough close data to compute momentum.")

    short_sma = sum(closes[-short_period:]) / short_period
    long_sma = sum(closes[-long_period:]) / long_period
    if long_sma == 0:
        raise ValueError("Long-term SMA is zero; cannot compute momentum.")
    return (short_sma - long_sma) / long_sma