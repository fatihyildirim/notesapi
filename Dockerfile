# Use a slim image based on Python 3.11
FROM python:3.11-slim

# Set the working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies (required for the PostgreSQL driver)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy and load dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project code
COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]