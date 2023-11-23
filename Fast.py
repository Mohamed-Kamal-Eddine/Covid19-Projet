from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_data():
    covid = pd.read_csv("data.csv")
    covid["Date"] = pd.to_datetime(covid["Date"], format="%d-%m-%Y")
    latest = covid[covid["Date"] == "2020-11-30"][["Country", "Confirmed", "Recovered", "Deaths", "Active"]]
    return covid, latest


@app.get("/get_data_covid", response_model=None)
def get_data():
    try:
        data1 = load_data()
        covid = data1[0]

        # Convert DataFrame to a list of dictionaries
        covid = json.loads(covid.to_json(orient="records", default_handler=str))

        return JSONResponse(content=covid, status_code=200)
    except Exception as e:
        # Handle exceptions appropriately, e.g., returning an HTTP error response
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/get_data_latest", response_model=None)
def get_data():
    try:
        data1 = load_data()
        latest = data1[1]
        # Convert DataFrame to a list of dictionaries
        latest = json.loads(latest.to_json(orient="records", default_handler=str))

        return JSONResponse(content=latest, status_code=200)

    except Exception as e:
        # Handle exceptions appropriately, e.g., returning an HTTP error response
        return JSONResponse(content={"error": str(e)}, status_code=500)
