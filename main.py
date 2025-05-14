from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google.cloud import bigquery
import os
import json
from typing import Dict, Any, List
import uvicorn
from datetime import date as date_type

app = FastAPI(title="Unemployment Prediction API",
              description="API to predict unemployment using a BigQuery ML model")

# BigQuery configuration
PROJECT_ID = "msds434finalprojectmiguswong"
DATASET_ID = "blsdata"
MODEL_ID = "automl_unempl"

class PredictionRequest(BaseModel):
    series_id: str = Field(..., description="BLS Series ID")
    year: int = Field(..., description="Year for prediction", ge=1900, le=2100)
    date: date_type = Field(..., description="Date for prediction in YYYY-MM-DD format")
    period: str = Field(..., description="Period code (e.g., M01 for January)")

class PredictionResponse(BaseModel):
    predicted_unemployment: float
    model_version: str = "automl_unempl"
    series_id: str
    year: int
    date: date_type
    period: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Unemployment Prediction API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Initialize BigQuery client
        client = bigquery.Client(project=PROJECT_ID)
        
        # Extract parameters
        series_id = request.series_id
        year = request.year
        date = request.date
        period = request.period
        
        # Construct the query for prediction
        query = f"""
        SELECT * FROM ML.PREDICT(
            MODEL `{PROJECT_ID}.{DATASET_ID}.{MODEL_ID}`,
            (SELECT 
                '{series_id}' AS series_id,
                {year} AS year,
                DATE '{date}' AS date,
                '{period}' AS period
            )
        )
        """
        
        # Run the prediction query
        query_job = client.query(query)
        results = query_job.result()
        
        # Get the prediction result
        for row in results:
            # The column name depends on your model output
            # Adjust based on your actual model's output column
            prediction_value = row.get('predicted_value', 0.0)
            
            return PredictionResponse(
                predicted_unemployment=prediction_value,
                series_id=series_id,
                year=year,
                date=date,
                period=period
            )
        
        # If no results were returned
        raise HTTPException(status_code=500, detail="No prediction results returned")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 