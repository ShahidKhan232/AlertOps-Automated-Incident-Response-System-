FROM python:3.9-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create .env file if it doesn't exist
RUN touch .env

EXPOSE 8080

# Use a more robust command to run the application
CMD ["python", "-u", "app.py"] 