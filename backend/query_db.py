from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np
import ollama
import re
from typing import List, Dict, Any, Tuple

app = Flask(__name__)
CORS(app, resources={r"/chatbot": {"origins": "http://localhost:3000"}})

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index for faster retrieval
index = faiss.read_index("uniprot_vector_store.index")

# Load metadata
metadata = pd.read_csv("uniprot_metadata.csv")

def parse_query(query: str) -> Tuple[str, Dict[str, str], Dict[str, str]]:
    """Parse query to extract filter and sort conditions if present."""
    base_query = query.lower()
    filters = {}
    sort_config = {}
    
    # Check if query contains filter command
    if "filter" in base_query:
        # Extract filter conditions
        filter_match = re.search(r'filter\s+(\w+)\s*=\s*(\w+)', base_query)
        if filter_match:
            field, value = filter_match.groups()
            filters[field] = value
            # Remove filter part from base query
            base_query = re.sub(r'filter\s+\w+\s*=\s*\w+', '', base_query).strip()
    
    # Check if query contains sort command
    if "sort" in base_query:
        # Extract sort conditions
        sort_match = re.search(r'sort\s+(\w+)\s*(asc|desc)?', base_query)
        if sort_match:
            field = sort_match.group(1)
            order = sort_match.group(2) if sort_match.group(2) else "asc"
            sort_config = {"field": field, "order": order}
            # Remove sort part from base query
            base_query = re.sub(r'sort\s+\w+\s*(asc|desc)?', '', base_query).strip()
    
    return base_query, filters, sort_config

def apply_filter(results: List[Dict], filters: Dict[str, str]) -> List[Dict]:
    """Apply filters to results if specified."""
    if not filters:
        return results
    
    filtered_results = results.copy()
    for field, value in filters.items():
        filtered_results = [
            result for result in filtered_results
            if str(value).lower() in str(result.get(field, '')).lower()
        ]
    return filtered_results

def apply_sort(results: List[Dict], sort_config: Dict[str, str]) -> List[Dict]:
    """Apply sorting to results if specified."""
    if not sort_config or 'field' not in sort_config:
        return results
    
    field = sort_config['field']
    reverse = sort_config.get('order', 'asc').lower() == 'desc'
    
    return sorted(
        results,
        key=lambda x: str(x.get(field, '')).lower(),
        reverse=reverse
    )

def query_faiss(query: str, top_k: int = 5) -> List[Dict]:
    """Query FAISS for the most relevant proteins."""
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), top_k)
    results = [metadata.iloc[i].to_dict() for i in indices[0]]
    return results

def generate_response_with_llama(query: str, context: List[Dict], 
                               filters: Dict[str, str] = None,
                               sort_config: Dict[str, str] = None) -> str:
    """Generate response using Llama."""
    # Create context text from results
    context_text = "\n".join(
        [f"Protein: {entry['protein_name']}, organism_name: {entry['organism_name']}, function: {entry['function']}, gene_names: {entry['gene_names']}, accessions: {entry['accessions']}, proteome: {entry['proteome']}" for entry in context]
    )
    
    # Add filter and sort information to prompt if present
    analysis_info = ""
    if filters:
        analysis_info += f"\nResults are filtered by {', '.join([f'{k}={v}' for k, v in filters.items()])}."
    if sort_config:
        analysis_info += f"\nResults are sorted by {sort_config['field']} in {sort_config['order']} order."
    
    prompt = f"""Context: {context_text}{analysis_info}
    Question: {query}
    Provide exact information of the exact proteins based on user queries. Present data in a html code for tabular format only when there is a word 'table' or 'tabular' in the user query. Keep the answer concise and to the point.
    Answer:"""
    
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "assistant", "content": prompt}]
    )
    return response["message"]

@app.route("/chatbot", methods=["POST"])
def chatbot():
    """Main chatbot endpoint handling queries with optional filtering and sorting."""
    data = request.json
    query = data.get("query", "")
    
    # Parse query for filter and sort commands
    base_query, filters, sort_config = parse_query(query)
    
    # Get initial results
    context = query_faiss(base_query)
    if not context:
        return jsonify({"response": {"content": "No relevant proteins found."}})
    
    # Apply filters if present in query
    if filters:
        context = apply_filter(context, filters)
    
    # Apply sorting if present in query
    if sort_config:
        context = apply_sort(context, sort_config)
    
    # Generate response using Llama
    response = generate_response_with_llama(base_query, context, filters, sort_config)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)