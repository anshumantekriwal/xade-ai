import requests
import json
from jsonschema import Draft7Validator
from genson import SchemaBuilder

# Sample API request using Mobula's get_market_data endpoint
response = requests.get("https://api.mobula.io/api/1/market/data?asset=bitcoin")
data = response.json()

# Generate schema using genson
builder = SchemaBuilder()
builder.add_object(data)

# Get schema
schema = builder.to_schema()
print("\nGenerated Schema:")
print(json.dumps(schema, indent=2))

# Validate response
validator = Draft7Validator(schema)
errors = sorted(validator.iter_errors(data), key=str)
print("\nValidation Errors:")
for error in errors:
    print(error.message)
