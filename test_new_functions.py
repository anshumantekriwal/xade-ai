from mobula import Mobula
from new_data_functions import *
from typing import Dict, Any
import traceback

# Initialize Mobula client
mobula = Mobula("e26c7e73-d918-44d9-9de3-7cbe55b63b99")
tests_passed = 0
total_tests = 0

print("Testing all data functions with Mobula API data...")

# # Get current market data and history for all time periods
# market_data = mobula.get_market_data(asset="bitcoin")
# history_24h = mobula.get_market_history(asset="bitcoin", period="24h")
# history_1h = mobula.get_market_history(asset="bitcoin", period="1h")
history_7d = mobula.get_market_history(asset="bitcoin", period="1h")
# history_30d = mobula.get_market_history(asset="bitcoin", period="30d")
# history_1y = mobula.get_market_history(asset="bitcoin", period="1y")

# Get pair data
# pairs = mobula.get_market_pairs(asset="bitcoin", limit="1")

# Get multi data for volume metrics
# multi_data = mobula.get_market_multi_data(symbols="BTC")

print(history_7d)
# prev_multi_data = mobula.get_market_multi_data(symbols="BTC")  # For comparison


