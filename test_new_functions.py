from mobula import Mobula
from new_data_functions import *
from social import LunarCrush
from typing import Dict, Any
import traceback

def run_test(test_name: str, test_func, *args) -> bool:
    global tests_passed, total_tests
    total_tests += 1
    try:
        result = test_func(*args)
        print(f"✓ {test_name} passed! Result:\n {result}")
        tests_passed += 1
        return True
    except Exception as e:
        print(f"✗ {test_name} failed!")
        print(f"Error: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return False

# Initialize API clients
mobula = Mobula("e26c7e73-d918-44d9-9de3-7cbe55b63b99")
lunar = LunarCrush("deb9mcyuk3wikmvo8lhlv1jsxnm6mfdf70lw4jqdk")
tests_passed = 0
total_tests = 0

print("\nTesting functions with raw API data...")

# Get social data from LunarCrush
btc_social = lunar.get_coins_list()

print(btc_social)

# Test functions that use social data
print("\nTesting social data functions...")
run_test("socialSentimentScore", socialSentimentScore, btc_social)
run_test("altRank", altRank, btc_social)
run_test("galaxyScore", galaxyScore, btc_social)
run_test("socialEngagementRate", socialEngagementRate, btc_social)

# Get market data from Mobula
# btc_market = mobula.get_market_data(symbol="BTC")
# btc_market_history = mobula.get_market_history(symbol="BTC", period="1y")

# # Test market sentiment index
# print("\nTesting market sentiment index...")
# run_test("marketSentimentIndex", marketSentimentIndex, btc_market_history, btc_social["sentiment"])

# # Test composite risk score
# print("\nTesting composite risk score...")
# # Get market volatility from price history
# price_history = btc_market_history["data"]["price_history"]
# price_changes = [(b[4] - a[4])/a[4] for a, b in zip(price_history[:-1], price_history[1:])]
# market_volatility = (max(price_changes) - min(price_changes)) / 2

# # Use social sentiment volatility
# social_volatility = btc_social.get("volatility", 0.5)  # Default if not available
# run_test("compositeRiskScore", compositeRiskScore, market_volatility, social_volatility)

# # Test liquidity adjusted price
# print("\nTesting liquidity adjusted price...")
# btc_pair = mobula.get_market_pairs(symbol="BTC", limit=1)
# run_test("liquidityAdjustedPrice", liquidityAdjustedPrice, btc_market, btc_pair["pairs"][0])

# # Test decentralization score
# print("\nTesting decentralization score...")
# btc_holders = mobula.get_market_token_holders(symbol="BTC")
# run_test("decentralizationScore", decentralizationScore, btc_holders)

# # Test social volatility index
# print("\nTesting social volatility index...")
# # Get historical sentiment from last 30 days of data
# sentiment_history = [0.6, 0.7, 0.5, 0.8, 0.7, 0.6, 0.9]  # Example values
# run_test("socialVolatilityIndex", socialVolatilityIndex, sentiment_history)

# # Test market momentum score
# print("\nTesting market momentum score...")
# run_test("marketMomentumScore", marketMomentumScore, btc_market_history, 7, 30)  # 7-day vs 30-day

