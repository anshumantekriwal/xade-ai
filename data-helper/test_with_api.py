import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_functions import getTokensDataOnBlockchain
from mobula import Mobula

def test_with_real_api():
    # Get API key from environment
    api_key = "e26c7e73-d918-44d9-9de3-7cbe55b63b99"
    
    # Initialize Mobula client
    client = Mobula(api_key)
    
    try:
        # Get real blockchain pairs data (limiting to 10 pairs for test)
        pairs_data = client.get_market_blockchain_pairs(
            blockchain="ethereum",
            limit=10
        )
        
        # Extract tokens using our function
        tokens = getTokensDataOnBlockchain(pairs_data)
        
        # Print results
        print(f"\nFound {len(tokens)} unique tokens:")
        for symbol, data in tokens.items():
            print(f"\n{symbol}:")
            print(f"  Address: {data.get('address')}")
            print(f"  Price: ${data.get('price', 0):.2f}")
            print(f"  Name: {data.get('name')}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_with_real_api()
