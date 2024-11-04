FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Set the environment variables
ENV CONFIGURATION_FILE_PATH ./src/config/halal_config.json

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the 'src' directory
COPY . .

# Expose the FastAPI port
EXPOSE 8080

# Start the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
