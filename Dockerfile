FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a directory for credentials
RUN mkdir -p /app/credentials

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/credentials.json

# Expose the port
EXPOSE 8080

CMD ["python", "main.py"] 