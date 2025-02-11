FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . .

# Default command: you can override this in docker-compose.yml
CMD ["python", "scanner/integrated_scanner.py", "-d", "example.com"]
