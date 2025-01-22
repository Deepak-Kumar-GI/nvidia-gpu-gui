FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy application files into the container
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the Flask application port
EXPOSE 5000

# Command to run the application
CMD ["python", "1.py", "--host=0.0.0.0", "--port=5000"]
