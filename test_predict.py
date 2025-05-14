import requests
import json
from datetime import date

# Base URL of your API
BASE_URL = "http://localhost:8080"

def test_predict_endpoint():
    """Test the prediction endpoint with BLS data parameters"""
    
    # Sample prediction request
    prediction_data = {
        "series_id": "LNS14000000",  # Unemployment Rate - All workers
        "year": 2023,
        "date": str(date(2023, 9, 1)),  # September 1, 2023
        "period": "M09"  # September
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("\nTesting /predict endpoint...")
    print("Sending prediction request with data:")
    print(json.dumps(prediction_data, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict", 
            headers=headers,
            json=prediction_data
        )
        
        print(f"Predict endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Prediction result: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_predict_endpoint() 