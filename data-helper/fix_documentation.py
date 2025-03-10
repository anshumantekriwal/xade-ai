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
            annotation = str(param.annotation) if param.annotation != inspect._empty else "Any"
            default = None if param.default == inspect._empty else param.default
            params[name] = {
                "type": annotation.replace("typing.", "").replace("Optional[", "").replace("]", ""),
                "description": f"Parameter {name}",
                "required": param.default == inspect._empty
            }
            if default is not None:
                params[name]["default"] = default
    return params

def fix_documentation():
    """Update documentation to match implementation"""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    endpoints_path = os.path.join(root_dir, 'mobula_endpoints.json')
    
    with open(endpoints_path, 'r') as f:
        docs = json.load(f)

    # Get all methods from Mobula class
    mobula_methods = {name: func for name, func in inspect.getmembers(Mobula, predicate=inspect.isfunction)
                     if not name.startswith('_')}

    # Update each endpoint's documentation
    for endpoint_name, endpoint_doc in docs.items():
        if endpoint_name in mobula_methods:
            method = mobula_methods[endpoint_name]
            actual_params = get_function_params(method)
            
            # Keep existing descriptions but update parameter list
            updated_inputs = {}
            for param_name, param_info in actual_params.items():
                if param_name in endpoint_doc.get('inputs', {}):
                    # Keep existing description and add/update other fields
                    existing = endpoint_doc['inputs'][param_name]
                    updated_inputs[param_name] = {
                        "type": param_info['type'],
                        "description": existing.get('description', param_info['description']),
                        "required": param_info['required']
                    }
                    if 'default' in param_info:
                        updated_inputs[param_name]['default'] = param_info['default']
                else:
                    # Add new parameter
                    updated_inputs[param_name] = param_info

            endpoint_doc['inputs'] = updated_inputs

    # Write updated documentation
    with open(endpoints_path, 'w') as f:
        json.dump(docs, f, indent=4)

    print("Documentation has been updated to match implementation.")

if __name__ == "__main__":
    fix_documentation()
    print("\nRunning verification after fix:")
    from verify_docs import verify_documentation
    verify_documentation()
