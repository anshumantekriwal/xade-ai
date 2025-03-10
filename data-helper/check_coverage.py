import inspect
import json
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mobula import Mobula

def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_api_methods():
    """Get all API methods from Mobula class"""
    methods = []
    for name, obj in inspect.getmembers(Mobula):
        # Filter only public methods that are not internal/special methods
        if inspect.isfunction(obj) and not name.startswith('_'):
            methods.append(name)
    return sorted(methods)

def get_documented_endpoints():
    """Get all documented endpoints from JSON"""
    with open(os.path.join(get_root_dir(), 'mobula_endpoints.json'), 'r') as f:
        docs = json.load(f)
    return sorted(list(docs.keys()))

def compare_coverage():
    """Compare API methods against documentation"""
    api_methods = get_api_methods()
    documented_endpoints = get_documented_endpoints()
    
    print("API Coverage Analysis:")
    print("-" * 50)
    
    print("\n1. Methods in API but not documented:")
    missing_docs = set(api_methods) - set(documented_endpoints)
    if missing_docs:
        for method in sorted(missing_docs):
            print(f"❌ {method}")
    else:
        print("✅ All API methods are documented!")
    
    print("\n2. Documented endpoints not in API:")
    extra_docs = set(documented_endpoints) - set(api_methods)
    if extra_docs:
        for endpoint in sorted(extra_docs):
            print(f"❓ {endpoint}")
    else:
        print("✅ All documented endpoints exist in API!")
    
    print("\n3. Coverage Statistics:")
    total_methods = len(api_methods)
    documented_count = len(set(api_methods) & set(documented_endpoints))
    coverage_percent = (documented_count / total_methods) * 100 if total_methods > 0 else 0
    
    print(f"Total API Methods: {total_methods}")
    print(f"Documented Methods: {documented_count}")
    print(f"Coverage: {coverage_percent:.1f}%")

if __name__ == "__main__":
    compare_coverage()
