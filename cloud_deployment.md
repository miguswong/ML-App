# Google Cloud Deployment Guide

This guide provides instructions for deploying your ML microservice to Google Cloud Run.

## Option 1: Using Google Cloud Shell (Recommended)

1. **Open Google Cloud Console**
   - Go to [https://console.cloud.google.com](https://console.cloud.google.com)
   - Make sure you're in the correct project: `msds434finalprojectmiguswong`

2. **Open Cloud Shell**
   - Click the Cloud Shell icon (>_) in the top-right corner of the console

3. **Clone your repository (if available) or create necessary files**
   ```bash
   mkdir -p unemployment-api
   cd unemployment-api
   # Create main.py, requirements.txt, etc. in Cloud Shell
   ```

4. **Build and push the container**
   ```bash
   # Set your project ID
   export PROJECT_ID=msds434finalprojectmiguswong
   
   # Build the container
   gcloud builds submit --tag gcr.io/${PROJECT_ID}/unemployment-api
   ```

5. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy unemployment-api \
     --image gcr.io/${PROJECT_ID}/unemployment-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars PROJECT_ID=${PROJECT_ID},DATASET_ID=blsdata,MODEL_ID=automl_unempl
   ```

## Option 2: Using Local Docker Push (If you have Docker configured for GCP)

If you have Docker configured to authenticate with Google Cloud:

1. **Push the image to Google Container Registry**
   ```bash
   docker push gcr.io/msds434finalprojectmiguswong/unemployment-api:latest
   ```

2. **Deploy from GCR**
   - Go to Google Cloud Console
   - Navigate to Cloud Run
   - Click "Create Service"
   - Use the container image: `gcr.io/msds434finalprojectmiguswong/unemployment-api:latest`
   - Set the required environment variables:
     - PROJECT_ID: msds434finalprojectmiguswong
     - DATASET_ID: blsdata
     - MODEL_ID: automl_unempl
   - Configure service settings (memory, CPU, etc.)
   - Deploy!

## Option 3: Install Google Cloud SDK Locally

1. **Download and install the Google Cloud SDK**
   - [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

2. **Initialize and authenticate**
   ```bash
   gcloud init
   gcloud auth login
   gcloud auth configure-docker
   ```

3. **Push the image**
   ```bash
   docker push gcr.io/msds434finalprojectmiguswong/unemployment-api:latest
   ```

4. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy unemployment-api \
     --image gcr.io/msds434finalprojectmiguswong/unemployment-api:latest \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars PROJECT_ID=msds434finalprojectmiguswong,DATASET_ID=blsdata,MODEL_ID=automl_unempl
   ```

## Service Account Setup

For Cloud Run to access BigQuery, you'll need to:

1. **Create a service account with BigQuery permissions**
   - Go to IAM & Admin > Service Accounts
   - Create a new service account
   - Add the BigQuery User and BigQuery Data Viewer roles
   
2. **Assign the service account to your Cloud Run service**
   - When creating or updating your Cloud Run service
   - In the "Security" section, select your service account

## Testing your deployed API

Once deployed, you'll receive a URL for your Cloud Run service. Test with:

```bash
curl -X GET "https://your-service-url/health"

curl -X POST "https://your-service-url/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "series_id": "LNS14000000",
    "year": 2023,
    "date": "2023-09-01",
    "period": "M09"
  }'
``` 