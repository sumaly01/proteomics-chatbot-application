import requests
import pandas as pd

def fetch_uniprot_data_entries():
    #API endpoint for proteins data
    url = "https://rest.uniprot.org/uniprotkb/search?query=*&format=json&size=500"
    response = requests.get(url)
    response.raise_for_status()  # Ensures request as successful
    data = response.json()

    proteins = []
    for entry in data.get("results", []):
        proteins.append({
            "id": entry.get("primaryAccession", ""),
            "protein_name": entry.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", ""),
            "gene_names": ", ".join(gene["geneName"]["value"] for gene in entry.get("genes", [])),
            "organism_name": entry.get("organism", {}).get("scientificName", ""),
            "accessions": ", ".join(entry.get("secondaryAccessions", [])),
            "proteome": ", ".join(proteome["id"] for proteome in entry.get("uniProtKBCrossReferences", []) if proteome["database"] == "Proteomes"),
            "function": next(
                (comment["texts"][0]["value"] for comment in entry.get("comments", []) if comment["commentType"] == "FUNCTION"), ""
            )
        })
    return pd.DataFrame(proteins)

def main():
    try:
        # Fetch UniProt data
        df = fetch_uniprot_data_entries()
        
        # Save in CSV file format
        output_file = "uniprot_extracted_data.csv"
        df.to_csv(output_file, index=False)
        
        # Display the results
        print(f"Data has been fetched successfully! Saved to {output_file}")
        print(df.head())  

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
