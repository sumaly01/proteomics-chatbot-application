# FROM python:3.9-slim

# # Set the working directory
# WORKDIR /app

# # Copy requirements file and install dependencies
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the backend code
# COPY . .

# # Expose the Flask server port
# EXPOSE 5000

# # Command to run the Flask app
# CMD ["python", "query_db.py"]


FROM python:3.9-slim

# Install curl for Ollama installation
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set the working directory
WORKDIR /app/src

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create start script in a different location
RUN echo '#!/bin/bash\n\
ollama serve & \n\
sleep 10\n\
if ! ollama list | grep -q "llama3.2:1b"; then\n\
    echo "Pulling llama3.2:1b model..."\n\
    ollama pull llama3.2:1b\n\
fi\n\
cd /app/src && python query_db.py\n\
' > /start.sh

# Make the script executable
RUN chmod +x /start.sh

# Copy the rest of the backend code
COPY . .

# Expose both Flask and Ollama ports
EXPOSE 5000 11434

# Use the startup script as the entry point
CMD ["/start.sh"]