# proteomics-chatbot-application
# Protein Search Assistant

A conversational AI system that helps users search protein information using natural language queries.

## Description

This application combines protein search capabilities with a conversational interface. Users can search for proteins, filter results, and sort data using natural language commands when explicitly mentioned in the query. The system uses FAISS for efficient vector search and the LLaMA language model for generating human-like responses.

## Getting Started

### Dependencies

* Python 3.8 or higher
* Flask
* FAISS
* Flask cors
* Sentence Transformers
* Ollama
* React.js
* Node.js
* npm

### Prerequisites

* Ollama application

### Installing

1. Clone the repository
```bash
git clone https://github.com/your-username/protein-search.git
cd protein-search
```

2. Set up backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up frontend
```bash
cd frontend
npm install
```

### Configuration

1. Make sure you have the required data files in the backend directory:
   * uniprot_vector_store.index
   * uniprot_metadata.csv

2. Install Ollama and download the LLaMA model:
```bash
# Install Ollama from https://ollama.ai/
ollama pull llama3.2:1b
```

## Running the Application

1. Start the backend server:
```bash
cd backend
python qyery_db.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at `http://localhost:3000`

## Usage Examples

Here are some example queries you can use:

1. Basic protein search:
```
Function of clarin-2
```

2. Sorted results:
```
List proteins sort protein_name desc
```

3. Combined operations:
```
Show organism name of Clarin-2 and Clarin-3
```


## Project Structure

```
protein-search/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── uniprot_vector_store.index
│   └── uniprot_metadata.csv
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── Message.jsx
│   │   │   ├── MessageList.jsx
│   │   │   └── InputArea.jsx
│   │   └── App.js
│   └── package.json
└── README.md
```

## API Reference

### POST /chatbot
Process user queries and return protein information.

Request body:
```json
{
  "query": "string"
}
```

Response:
```json
{
  "response": {
    "content": "string"
  }
}
```

## Common Issues & Solutions

1. **FAISS Index Error**
   * Make sure the index file is in the correct location
   * Verify the file permissions

2. **LLaMA Model Issues**
   * Ensure Ollama is running
   * Verify the model is downloaded correctly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Authors

* Your Name
* Contact: your.email@example.com

## Version History

* 1.0.0
    * Initial Release
    * Basic search functionality
* 1.1.0
    * Added filtering and sorting
    * Improved response formatting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

* UniProt database
* FAISS by Facebook Research
* Meta AI for LLaMA model
