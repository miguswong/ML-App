# Unemployment Prediction Microservice

This microservice provides access to a BigQuery ML regression model for predicting unemployment rates based on Bureau of Labor Statistics (BLS) data.

## Overview

The service uses a pre-trained machine learning model in BigQuery ML to predict unemployment rates based on time series data. The model was trained using historical BLS unemployment data.

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
- `GET /auth-test`: Test BigQuery authentication
- `POST /predict`: Get unemployment predictions

### Example prediction request:

```json
{
  "series_id": "LNS14000000",
  "year": 2023,
  "date": "2023-06-01",
  "period": "M06"
}
```

### Example response:

```json
{
  "predicted_unemployment": 3.6,
  "model_version": "automl_unempl",
  "series_id": "LNS14000000",
  "year": 2023,
  "date": "2023-06-01",
  "period": "M06"
}
```

## Environment Variables

Create a `.env` file based on the included `env.example`:

- `PROJECT_ID`: Your Google Cloud project ID (default: "msds434finalprojectmiguswong")
- `DATASET_ID`: The BigQuery dataset ID containing your model (default: "blsdata")
- `MODEL_ID`: The ID of your BigQuery ML model (default: "automl_unempl")
- `PORT`: Port to run the service on (default: 8080)

## Docker Deployment

Build the Docker image:
```
docker build -t unemployment-prediction-api .
```

Run the container:
```
# For PowerShell
docker run -p 8080:8080 -v "${PWD}/credentials.json:/app/credentials/credentials.json" -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/credentials.json unemployment-prediction-api

# For CMD
docker run -p 8080:8080 -v "%cd%\credentials.json:/app/credentials/credentials.json" -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/credentials.json unemployment-prediction-api

# For Bash/Linux
docker run -p 8080:8080 -v "$(pwd)/credentials.json:/app/credentials/credentials.json" -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/credentials.json unemployment-prediction-api
```

## Cloud Deployment

This service can be deployed to Google Cloud Run using the provided `cloudbuild.yaml`:

```bash
# Build and deploy using Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Or manually deploy to Cloud Run
gcloud run deploy unemployment-api \
  --image gcr.io/msds434finalprojectmiguswong/unemployment-api \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars PROJECT_ID=msds434finalprojectmiguswong,DATASET_ID=blsdata,MODEL_ID=automl_unempl
```

## Testing

Use the included `test_predict.py` script to test the API:

```
python test_predict.py
```

## Notes

- For production deployment, consider setting up CI/CD pipelines and properly managing secrets.
- Ensure the service account has the necessary permissions to access BigQuery and the ML model. 