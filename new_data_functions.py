from typing import Any, Dict, List

# ------------------------------------------------------------------------------
# 11. liquidity
# ------------------------------------------------------------------------------
def liquidity(pair_output: Dict[str, Any]) -> float:
    """
    Function Name: liquidity
    Description: Extracts the liquidity metric from a trading pair object.
                 The raw API output is expected to be a dictionary representing a single trading pair
                 from Mobula.get_market_pairs, containing a "liquidity" field.
    Inputs:
        - pair_output: Dictionary representing a single trading pair.
    Processing:
        - Extract and return the liquidity value.
    Output:
        - A float representing the liquidity of the trading pair.
    """
    liq = pair_output.get('data').get('pairs')[0].get('liquidity')
    if liq is None:
        raise ValueError("Liquidity not found in pair_output.")
    return liq

# ------------------------------------------------------------------------------
# 13. offChainVolume
# ------------------------------------------------------------------------------
def offChainVolume(multi_data_output: Dict[str, Any], symbol) -> float:
    """
    Function Name: offChainVolume
    Description: Retrieves the off-chain trading volume.
                 The raw API output is expected to have a "data" field (or be a direct asset object)
                 containing the "off_chain_volume" field, as returned by Mobula.get_market_multi_data.
    Inputs:
        - multi_data_output: Dictionary containing market data for an asset.
    Processing:
        - Extract and return the off-chain volume value.
    Output:
        - A float representing the off-chain trading volume.
    """
    data = multi_data_output.get("data").get(symbol)
    off_volume = data.get("off_chain_volume")
    if off_volume is None:
        raise ValueError("Off-chain volume not found in multi_data_output.")
    return off_volume

# ------------------------------------------------------------------------------
# 14. volume7d
# ------------------------------------------------------------------------------
def volume7d(daily_volumes_output: List[float]) -> float:
    """
    Function Name: volume7d
    Description: Aggregates trading volume over the last 7 days.
                 The input is a list of daily trading volume figures.
    Inputs:
        - daily_volumes_output: List of daily trading volume numbers.
    Processing:
        - Sum the volumes for the last 7 days.
    Output:
        - A float representing the total 7-day trading volume.
    """
    if len(daily_volumes_output) < 7:
        raise ValueError("Insufficient daily volume data for 7-day aggregation.")
    return sum(daily_volumes_output[-7:])

# ------------------------------------------------------------------------------
# 15. volumeChange24h
# ------------------------------------------------------------------------------
def volumeChange24h(current_market_data_output: Dict[str, Any], previous_market_data_output: Dict[str, Any]) -> float:
    """
    Function Name: volumeChange24h
    Description: Calculates the percentage change in trading volume over the past 24 hours.
                 The raw API outputs are expected to have a "data" field containing a dictionary with a "volume" field.
    Inputs:
        - current_market_data_output: Dictionary containing current market data.
        - previous_market_data_output: Dictionary containing market data from 24 hours ago.
    Processing:
        - Extract the "volume" from each output and compute percentage change: ((current - previous) / previous) * 100.
    Output:
        - A float representing the 24-hour volume change percentage.
    """
    current_data = current_market_data_output.get("data", current_market_data_output)
    previous_data = previous_market_data_output.get("data", previous_market_data_output)
    current_vol = current_data.get("volume")
    previous_vol = previous_data.get("volume")
    if current_vol is None or previous_vol is None:
        raise ValueError("Required volume data missing for computation.")
    if previous_vol == 0:
        raise ValueError("Previous volume is zero; cannot compute change.")
    return ((current_vol - previous_vol) / previous_vol) * 100

# ------------------------------------------------------------------------------
# 16. priceChange24h
# ------------------------------------------------------------------------------
def priceChange24h(current_market_data_output: Dict[str, Any], history_24h_output: Dict[str, Any]) -> float:
    """
    Function Name: priceChange24h
    Description: Calculates the percentage change in price over the past 24 hours.
                 The raw API outputs are expected to have a "data" field containing a dictionary with a "price" field.
                 Current price is from Mobula.get_market_data and the 24h-old price is from Mobula.get_market_history.
    Inputs:
        - current_market_data_output: Dictionary containing current market data.
        - history_24h_output: Dictionary containing market history data from 24 hours ago.
    Processing:
        - Extract the "price" from each output and compute percentage change: ((current - old) / old) * 100.
    Output:
        - A float representing the 24-hour price change percentage.
    """
    current_data = current_market_data_output.get("data", current_market_data_output)
    history_data = history_24h_output.get("data", history_24h_output)
    current_price = current_data.get("price")
    old_price = history_data.get("price")
    if current_price is None or old_price is None:
        raise ValueError("Required price data missing for computation.")
    if old_price == 0:
        raise ValueError("Old price is zero; cannot compute change.")
    return ((current_price - old_price) / old_price) * 100

# ------------------------------------------------------------------------------
# 17. priceChange1h
# ------------------------------------------------------------------------------
def priceChange1h(current_market_data_output: Dict[str, Any], history_1h_output: Dict[str, Any]) -> float:
    """
    Function Name: priceChange1h
    Description: Calculates the percentage change in price over the past 1 hour.
                 The raw API outputs are expected to have a "data" field containing a dictionary with a "price" field.
                 Current price is from Mobula.get_market_data and the 1h-old price is from Mobula.get_market_history.
    Inputs:
        - current_market_data_output: Dictionary containing current market data.
        - history_1h_output: Dictionary containing market history data from 1 hour ago.
    Processing:
        - Extract the "price" from each output and compute percentage change.
    Output:
        - A float representing the 1-hour price change percentage.
    """
    current_data = current_market_data_output.get("data", current_market_data_output)
    history_data = history_1h_output.get("data", history_1h_output)
    current_price = current_data.get("price")
    old_price = history_data.get("price")
    if current_price is None or old_price is None:
        raise ValueError("Required price data missing for computation.")
    if old_price == 0:
        raise ValueError("Old price is zero; cannot compute change.")
    return ((current_price - old_price) / old_price) * 100

# ------------------------------------------------------------------------------
# 18. priceChange7d
# ------------------------------------------------------------------------------
def priceChange7d(current_market_data_output: Dict[str, Any], history_7d_output: Dict[str, Any]) -> float:
    """
    Function Name: priceChange7d
    Description: Calculates the percentage change in price over the past 7 days.
                 The raw API outputs are expected to have a "data" field containing a dictionary with a "price" field.
                 Current price is from Mobula.get_market_data and the 7d-old price is from Mobula.get_market_history.
    Inputs:
        - current_market_data_output: Dictionary containing current market data.
        - history_7d_output: Dictionary containing market history data from 7 days ago.
    Processing:
        - Extract the "price" from each output and compute percentage change.
    Output:
        - A float representing the 7-day price change percentage.
    """
    current_data = current_market_data_output.get("data", current_market_data_output)
    history_data = history_7d_output.get("data", history_7d_output)
    current_price = current_data.get("price")
    old_price = history_data.get("price")
    if current_price is None or old_price is None:
        raise ValueError("Required price data missing for computation.")
    if old_price == 0:
        raise ValueError("Old price is zero; cannot compute change.")
    return ((current_price - old_price) / old_price) * 100

# ------------------------------------------------------------------------------
# 19. priceChange30d
# ------------------------------------------------------------------------------
def priceChange30d(current_market_data_output: Dict[str, Any], history_30d_output: Dict[str, Any]) -> float:
    """
    Function Name: priceChange30d
    Description: Calculates the percentage change in price over the past 30 days.
                 The raw API outputs are expected to have a "data" field containing a dictionary with a "price" field.
                 Current price is from Mobula.get_market_data and the 30d-old price is from Mobula.get_market_history.
    Inputs:
        - current_market_data_output: Dictionary containing current market data.
        - history_30d_output: Dictionary containing market history data from 30 days ago.
    Processing:
        - Extract the "price" from each output and compute percentage change.
    Output:
        - A float representing the 30-day price change percentage.
    """
    current_data = current_market_data_output.get("data", current_market_data_output)
    history_data = history_30d_output.get("data", history_30d_output)
    current_price = current_data.get("price")
    old_price = history_data.get("price")
    if current_price is None or old_price is None:
        raise ValueError("Required price data missing for computation.")
    if old_price == 0:
        raise ValueError("Old price is zero; cannot compute change.")
    return ((current_price - old_price) / old_price) * 100

# ------------------------------------------------------------------------------
# 20. priceChange1y
# ------------------------------------------------------------------------------
def priceChange1y(current_market_data_output: Dict[str, Any], history_1y_output: Dict[str, Any]) -> float:
    """
    Function Name: priceChange1y
    Description: Calculates the percentage change in price over the past 1 year.
                 The raw API outputs are expected to have a "data" field containing a dictionary with a "price" field.
                 Current price is from Mobula.get_market_data and the 1y-old price is from Mobula.get_market_history.
    Inputs:
        - current_market_data_output: Dictionary containing current market data.
        - history_1y_output: Dictionary containing market history data from 1 year ago.
    Processing:
        - Extract the "price" from each output and compute percentage change.
    Output:
        - A float representing the 1-year price change percentage.
    """
    current_data = current_market_data_output.get("data", current_market_data_output)
    history_data = history_1y_output.get("data", history_1y_output)
    current_price = current_data.get("price")
    old_price = history_data.get("price")
    if current_price is None or old_price is None:
        raise ValueError("Required price data missing for computation.")
    if old_price == 0:
        raise ValueError("Old price is zero; cannot compute change.")
    return ((current_price - old_price) / old_price) * 100