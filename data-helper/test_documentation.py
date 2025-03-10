import json
import os

def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_endpoint_docs():
    endpoints_path = os.path.join(get_root_dir(), 'mobula_endpoints.json')
    with open(endpoints_path, 'r') as f:
        return json.load(f)

def search_endpoints(docs, query):
    """Simulates a basic RAG-like search through the endpoints"""
    results = []
    query = query.lower()
    
    for endpoint, info in docs.items():
        # Search in description and use case
        relevance = 0
        if query in info['description'].lower():
            relevance += 2
        if query in info['use_case'].lower():
            relevance += 1
            
        # Search in input/output descriptions
        for param in info['inputs'].values():
            if query in param['description'].lower():
                relevance += 1
        
        if 'outputs' in info:
            for output in info['outputs'].values():
                if isinstance(output, dict) and 'description' in output:
                    if query in output['description'].lower():
                        relevance += 1
        
        if relevance > 0:
            results.append({
                'endpoint': endpoint,
                'relevance': relevance,
                'description': info['description'],
                'use_case': info['use_case']
            })
    
    # Sort by relevance
    return sorted(results, key=lambda x: x['relevance'], reverse=True)

# Load the documentation
docs = load_endpoint_docs()

# Example 1: Search for NFT-related endpoints
print("\nSearching for NFT-related endpoints:")
print("-" * 50)
nft_results = search_endpoints(docs, "nft")
for result in nft_results:
    print(f"\nEndpoint: {result['endpoint']}")
    print(f"Description: {result['description']}")
    print(f"Use Case: {result['use_case']}")

# Example 2: Search for portfolio tracking
print("\nSearching for portfolio-related endpoints:")
print("-" * 50)
portfolio_results = search_endpoints(docs, "portfolio")
for result in portfolio_results:
    print(f"\nEndpoint: {result['endpoint']}")
    print(f"Description: {result['description']}")
    print(f"Use Case: {result['use_case']}")

# Example 3: Get detailed input requirements for a specific endpoint
print("\nDetailed inputs for get_market_data:")
print("-" * 50)
market_data = docs['get_market_data']['inputs']
for param, details in market_data.items():
    print(f"\nParameter: {param}")
    print(f"Type: {details['type']}")
    print(f"Description: {details['description']}")
    print(f"Required: {details['required']}")
