# Fixed Cloud Deployment Instructions

We need to rebuild and redeploy the application to fix the credentials issue. The problem was that the application was looking for a credentials file, but in Cloud Run we should use the service account's built-in authentication.

## 1. Fix the Code

The following changes have been made:
1. Removed the credentials file dependency in the code
2. Updated the Dockerfile to not expect a credentials file
3. Added an `/auth-test` endpoint for debugging authentication

## 2. Rebuild and Deploy

### Option 1: Using Cloud Shell (Recommended)

1. **Open Google Cloud Console**
   - Go to [https://console.cloud.google.com](https://console.cloud.google.com)
   - Make sure you're in the correct project: `msds434finalprojectmiguswong`

2. **Open Cloud Shell**
   - Click the Cloud Shell icon (>_) in the top-right corner of the console

3. **Upload the updated files**
   - Upload the updated `main.py` and `Dockerfile` files

4. **Build and deploy**
   ```bash
   # Set your project ID
   export PROJECT_ID=msds434finalprojectmiguswong
   
   # Build the container
   gcloud builds submit --tag gcr.io/${PROJECT_ID}/unemployment-api
   
   # Deploy to Cloud Run with appropriate service account
   gcloud run deploy unemployment-api \
     --image gcr.io/${PROJECT_ID}/unemployment-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars PROJECT_ID=${PROJECT_ID},DATASET_ID=blsdata,MODEL_ID=automl_unempl \
     --service-account YOUR_SERVICE_ACCOUNT_EMAIL
   ```
   
   Replace `YOUR_SERVICE_ACCOUNT_EMAIL` with a service account that has BigQuery access rights. If you don't have one:

## 3. Create a Service Account (if needed)

1. **Create a service account**
   ```bash
   # Create the service account
   gcloud iam service-accounts create unemployment-api-sa \
     --display-name="Unemployment API Service Account"
   
   # Grant BigQuery access
   gcloud projects add-iam-policy-binding ${PROJECT_ID} \
     --member="serviceAccount:unemployment-api-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
     --role="roles/bigquery.user"
   
   gcloud projects add-iam-policy-binding ${PROJECT_ID} \
     --member="serviceAccount:unemployment-api-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
     --role="roles/bigquery.dataViewer"
   ```

2. **Redeploy with the service account**
   ```bash
   gcloud run deploy unemployment-api \
     --image gcr.io/${PROJECT_ID}/unemployment-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars PROJECT_ID=${PROJECT_ID},DATASET_ID=blsdata,MODEL_ID=automl_unempl \
     --service-account unemployment-api-sa@${PROJECT_ID}.iam.gserviceaccount.com
   ```

## 4. Testing the Deployment

1. **Test authentication**
   - Access the `/auth-test` endpoint to verify BigQuery authentication is working
   - Go to: `https://your-service-url/auth-test`

2. **Test the prediction endpoint**
   ```bash
   curl -X POST "https://your-service-url/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "series_id": "LNS14000000",
       "year": 2023,
       "date": "2023-09-01",
       "period": "M09"
     }'
   ```

## Explanation of the Fix

The original error occurred because:
1. The Dockerfile was setting `GOOGLE_APPLICATION_CREDENTIALS` to a path that didn't exist in the Cloud Run environment
2. The application was trying to use this non-existent credentials file

The fix:
1. Remove the explicit credentials path in the Dockerfile
2. Let the BigQuery client automatically use the Cloud Run service account credentials
3. Ensure the service account has the proper permissions for BigQuery access 