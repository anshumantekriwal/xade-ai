from mobula import Mobula
import json

# Initialize with provided API key
client = Mobula("e26c7e73-d918-44d9-9de3-7cbe55b63b99")

try:
    # Get market data for Bitcoin
    btc_data = client.get_market_data(symbol="BTC")
    
    # Pretty print the results
    print("Bitcoin Market Data:")
    print("-" * 50)
    print(f"Price: ${btc_data['price']:,.2f}")
    print(f"Market Cap: ${btc_data['market_cap']:,.2f}")
    print(f"24h Volume: ${btc_data['volume']:,.2f}")
    print(f"24h Price Change: {btc_data['price_change_24h']}%")
    print(f"Liquidity: ${btc_data['liquidity']:,.2f}")
    
except Exception as e:
    print(f"Error: {str(e)}")
