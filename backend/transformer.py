from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import faiss

# Read CSV file
df = pd.read_csv("uniprot_extracted_data.csv")

# Load a pre-trained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Converts DataFrame rows into formatted strings combining protein information into a list
texts = df.apply(lambda x: f"Protein: {x['protein_name']} | Gene names: {x['gene_names']} | Organism: {x['organism_name']} | Accessions: {x['accessions']} | Proteome: {x['proteome']} | | Function: {x['function']}", axis=1).tolist()

# Generate embeddings locally
embeddings = model.encode(texts, show_progress_bar=True)

# Store the embeddings in FAISS

# Convert embeddings to a NumPy array
embeddings_array = np.array(embeddings)
# Create FAISS index
dimension = embeddings_array.shape[1]

index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(embeddings_array)

# Save the FAISS index for fast retrieval
faiss.write_index(index, "uniprot_vector_store.index")

# Save metadata
df.to_csv("uniprot_metadata.csv", index=False)
