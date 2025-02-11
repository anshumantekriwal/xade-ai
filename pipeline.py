import os
from os import getenv
from dotenv import load_dotenv
import json
import re
import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

class CryptoAnalysisPipeline:
    def __init__(self):
        load_dotenv()
        
        # Initialize API configurations
        self.lunarcrush_base_url = "https://lunarcrush.com/api4"
        self.mobula_base_url = "https://production-api.mobula.io/api/1"
        self.lunarcrush_headers = {
            'Authorization': 'Bearer deb9mcyuk3wikmvo8lhlv1jsxnm6mfdf70lw4jqdk'
        }
        self.mobula_headers = {
            "Authorization": "e26c7e73-d918-44d9-9de3-7cbe55b63b99"
        }
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=getenv("OPENAI_API_KEY"),
            model_name="gpt-4o",
            verbose=True,
            temperature=0
        )
        
        # Load endpoint configurations
        self.load_endpoint_configs()

    def load_endpoint_configs(self):
        """Load API endpoint configurations from file"""
        try:
            with open('lunarcrush.json', 'r') as file:
                self.lunarcrush_endpoints = json.load(file)
            
            self.mobula_endpoints = [{
                "endpoint": "/market/data?symbol=LINK",
                "description": "Get market data for given coin.",
                "parameters": [{
                    "name": "symbol",
                    "description": "Provide the symbol to get details for.",
                    "type": "string",
                    "example": "BTC",
                    "required": "true"
                }]
            }]
            
            self.example = [{
                "provider": "mobula",
                "endpoint": "/market/data?symbol=BTC",
                "description": "Get market data on bitcoin."
            }, {
                "provider": "lunarcrush",
                "endpoint": "/public/topic/bitcoin/v1",
                "description": "Get summary information including social sentiment for Bitcoin."
            }]
        except FileNotFoundError as e:
            raise Exception(f"Configuration file not found: {e}")

    def create_system_prompt(self):
        """Create system prompt template for API endpoint selection"""
        return SystemMessagePromptTemplate.from_template('''
            You are an AI agent specialized in determining the appropriate cryptocurrency API calls based on user queries. 
            
            Your primary function is to analyze user queries and determine which API endpoints from Lunarcrush and Mobula would be most suitable to fulfill the request.
            
            Use Mobula for more market related data and Lunarcrush for social metrics.
            
            AVAILABLE ENDPOINTS:
            
            LunarCrush API Endpoints (given in JSON format):
            {lunarcrush_endpoints}
            
            Mobula API Endpoints (given in JSON format):
            {mobula_endpoints}
            
            For each user query:
            1. Analyze the query to identify:
               - Required data points (price, volume, social metrics etc)
               - Time frame (current vs historical)
               - Specific assets or topics
            
            2. Determine the most appropriate API endpoint(s) based on:
               - Data requirements
               - Rate limits and data freshness
               - Query complexity
            
            3. Format the API call(s) with:
               - Required parameters
               - Appropriate filters
               - Sorting options if applicable
            
            4. YOU MUST OUTPUT ONLY JSON IN THE EXACT FORMAT SHOWN BELOW. DO NOT INCLUDE ANY OTHER TEXT OR EXPLANATIONS:
            {example}
            
            YOUR RESPONSE MUST BE VALID JSON AND NOTHING ELSE. DO NOT EXPLAIN YOUR THOUGHT PROCESS.
        ''').format(
            lunarcrush_endpoints=self.lunarcrush_endpoints,
            mobula_endpoints=self.mobula_endpoints,
            example=self.example
        )

    def clean_llm_response(self, response_content):
        """Clean and parse LLM response"""
        try:
            # First try to parse directly
            return json.loads(response_content)
        except json.JSONDecodeError:
            # If that fails, try to clean and parse
            try:
                # Remove markdown code blocks
                clean_output = re.sub(r"```(?:json)?\s*|\s*```", "", response_content.strip())
                # Convert single quotes to double quotes, but only for strings
                clean_output = re.sub(r"(?<!\w)'(.*?)'(?!\w)", r'"\1"', clean_output)
                # Remove any leading/trailing whitespace
                clean_output = clean_output.strip()
                return json.loads(clean_output)
            except json.JSONDecodeError as e:
                raise Exception(f"Failed to parse LLM response: {response_content}\nError: {str(e)}")

    def fetch_api_data(self, api_info):
        """Fetch data from specified APIs"""
        api_responses = []
        
        for api in api_info:
            endpoint = api.get("endpoint")
            base_url = self.lunarcrush_base_url if api['provider'] == "lunarcrush" else self.mobula_base_url
            headers = self.lunarcrush_headers if api['provider'] == "lunarcrush" else self.mobula_headers
            
            try:
                response = requests.get(f"{base_url}{endpoint}", headers=headers)
                response.raise_for_status()
                api_responses.append({
                    "endpoint": endpoint,
                    "response": response.json()
                })
            except requests.RequestException as e:
                api_responses.append({
                    "endpoint": endpoint,
                    "error": str(e)
                })
        
        return api_responses

    def create_tweet(self, api_responses, query):
        """Generate tweet based on API responses"""
        system_template = '''
        Use the given data to create a tweet that utilizes the provided context to answer the user query.
        Don't include any hashtags or call to actions in the tweet. You are free to use emojis.
        Format the output properly and make sure it is as informative as possible.
        
        Context:
        {api_responses}
        '''
        
        system_prompt = SystemMessagePromptTemplate.from_template(system_template).format(
            api_responses=api_responses
        )
        human_prompt = HumanMessagePromptTemplate.from_template("Query: {input}").format(
            input=query
        )
        
        response = self.llm.invoke([system_prompt, human_prompt])
        return response.content

    def run_pipeline(self, query):
        """Execute the complete analysis pipeline"""
        try:
            # 1. Get API endpoint recommendations
            system_prompt = self.create_system_prompt()
            human_prompt = HumanMessagePromptTemplate.from_template("Query: {input}").format(input=query)
            endpoint_response = self.llm.invoke([system_prompt, human_prompt])
            
            # 2. Parse and clean the response
            api_info = self.clean_llm_response(endpoint_response.content)
            
            # 3. Fetch data from APIs
            api_responses = self.fetch_api_data(api_info)
            
            # 4. Generate tweet
            tweet = self.create_tweet(api_responses, query)
            
            return {
                "api_info": api_info,
                "api_responses": api_responses,
                "tweet": tweet
            }
            
        except Exception as e:
            return {"error": f"Pipeline execution failed: {str(e)}"}

def main():
    # Example usage
    pipeline = CryptoAnalysisPipeline()
    result = pipeline.run_pipeline("Market data and social metrics for AIXBT")
    
    if "error" in result:
        print("Error:", result["error"])
    else:
        print("\nAPI Info:", json.dumps(result["api_info"], indent=2))
        print("\nGenerated Tweet:", result["tweet"])

if __name__ == "__main__":
    main()
