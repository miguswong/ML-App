# Unemployment Prediction Microservice

This microservice provides access to a BigQuery ML regression model for unemployment predictions.

## Setup

1. Ensure you have Google Cloud credentials set up correctly:
   - Create a service account with access to BigQuery
   - Download the service account key and save it securely
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your service account key

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the service locally:
   ```
   python main.py
   ```

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint
- `POST /predict`: Get unemployment predictions

### Example prediction request:

```json
{
  "features": {
    "feature1": 1.0,
    "feature2": 2.0
    // Add all required features for your model
  }
}
```

## Docker Deployment

Build the Docker image:
```
docker build -t unemployment-prediction-api .
```

Run the container:
```
# For PowerShell
docker run -p 8080:8080 -v "${PWD}/credentials.json:/app/credentials/credentials.json" unemployment-prediction-api

# For CMD
docker run -p 8080:8080 -v "%cd%\credentials.json:/app/credentials/credentials.json" unemployment-prediction-api

# For Bash/Linux
docker run -p 8080:8080 -v "$(pwd)/credentials.json:/app/credentials/credentials.json" unemployment-prediction-api
```

## Cloud Deployment

This service can be deployed to Google Cloud Run, Google Kubernetes Engine, or any other container orchestration platform.

For Google Cloud Run deployment:

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/msds434finalprojectmiguswong/unemployment-api

# Deploy to Cloud Run
gcloud run deploy unemployment-api \
  --image gcr.io/msds434finalprojectmiguswong/unemployment-api \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars PROJECT_ID=msds434finalprojectmiguswong,DATASET_ID=blsdata,MODEL_ID=automl_unempl
```

For production deployment, consider setting up CI/CD pipelines and properly managing secrets. 