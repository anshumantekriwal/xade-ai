from langchain_openai import ChatOpenAI
import faiss
import numpy as np
from typing import List, Dict
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()

def process_rag_query(
    rag_instructions: str,
    function_names: List[str],
    function_descriptions: List[str]
) -> Dict[str, Dict[str, str]]:
    """
    Process RAG instructions to find relevant functions using embeddings and FAISS.
    
    Args:
        rag_instructions (str): The instructions to process
        function_names (List[str]): List of available function names
        function_descriptions (List[str]): List of function descriptions corresponding to function_names
        
    Returns:
        Dict[str, Dict[str, str]]: Dictionary mapping function names to their descriptions and code
    """
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o-mini")
    client = OpenAI()
    
    # Create optimized RAG query using the LLM
    messages = [
        {"role": "system", "content": "You are a DeFi data specialist that converts instructions into clear, concise search queries focused on finding relevant data functions."},
        {"role": "user", "content": f"Convert these instructions into a focused search query optimized for finding relevant DeFi data functions: {rag_instructions}"}
    ]
    completion = llm.invoke(messages)
    rag_query = completion.content
    
    # Create embeddings
    query_embedding = client.embeddings.create(
        model="text-embedding-ada-002",
        input=rag_query
    ).data[0].embedding
    

    description_embeddings = []
    for desc in function_descriptions:
        print(desc) 
        embedding = client.embeddings.create(
            model="text-embedding-ada-002",
            input=desc
        ).data[0].embedding
        description_embeddings.append(embedding)
    
    # Convert embeddings to numpy arrays for FAISS
    query_embedding = np.array(query_embedding).reshape(1, -1).astype('float32')
    description_embeddings = np.array(description_embeddings).astype('float32')
    
    # Create FAISS index
    dimension = len(query_embedding[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(description_embeddings)
    
    # Search for most similar functions
    k = min(3, len(function_descriptions))  # Get top 3 or less if fewer functions exist
    distances, indices = index.search(query_embedding, k)
    
    # Get the matching functions and build result dictionary
    results = {}
    for idx in indices[0]:
        func_name = function_names[idx]
        results[func_name] = {
            "description": function_descriptions[idx],
            "code": ""  # Code can be added if needed, similar to the existing implementation
        }
    
    return results
