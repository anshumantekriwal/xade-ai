import inspect
import json
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mobula import Mobula

def get_function_params(func):
    """Extract function parameters and their types from the function signature"""
    signature = inspect.signature(func)
    params = {}
    for name, param in signature.parameters.items():
        if name != 'self':
            params[name] = {
                "type": str(param.annotation) if param.annotation != inspect._empty else "Any",
                "required": param.default == inspect._empty
            }
    return params

def verify_documentation():
    """Verify documentation against actual implementation"""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    endpoints_path = os.path.join(root_dir, 'mobula_endpoints.json')
    with open(endpoints_path, 'r') as f:
        docs = json.load(f)
    
    issues = []
    print("Documentation Verification Report:")
    print("-" * 50)

    # Get all methods from Mobula class
    mobula_methods = {name: func for name, func in inspect.getmembers(Mobula, predicate=inspect.isfunction)
                     if not name.startswith('_')}

    # Verify each documented endpoint
    for endpoint_name, endpoint_doc in docs.items():
        print(f"\nChecking endpoint: {endpoint_name}")
        
        # Check if method exists in implementation
        if endpoint_name not in mobula_methods:
            issues.append(f"❌ {endpoint_name}: Method not found in implementation")
            continue

        # Get actual method parameters
        actual_params = get_function_params(mobula_methods[endpoint_name])
        doc_params = endpoint_doc.get('inputs', {})

        # Compare parameters
        for param_name, param_info in actual_params.items():
            if param_name not in doc_params:
                issues.append(f"❌ {endpoint_name}: Missing parameter '{param_name}' in documentation")
            else:
                # Check if required status matches
                if doc_params[param_name].get('required', False) != param_info['required']:
                    issues.append(
                        f"❌ {endpoint_name}: Parameter '{param_name}' required status mismatch. "
                        f"Doc: {doc_params[param_name].get('required', False)}, "
                        f"Actual: {param_info['required']}"
                    )

        # Check for extra documented parameters
        for param_name in doc_params:
            if param_name not in actual_params:
                issues.append(f"❌ {endpoint_name}: Extra parameter '{param_name}' in documentation")

        print(f"✓ Parameters checked")

    # Print summary
    print("\nVerification Summary:")
    print("-" * 50)
    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(issue)
    else:
        print("✅ All documentation matches implementation!")

    return len(issues) == 0

if __name__ == "__main__":
    verify_documentation()
