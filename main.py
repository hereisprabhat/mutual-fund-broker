import os
import requests
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from helper import authenticate_access_token
from model import MutualFundScheme, UserLogin

load_dotenv()


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration constants
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_URL = os.getenv("RAPID_API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_URL}
base_url = f"https://{RAPID_API_URL}"

def fetch_data(url: str, params: dict) -> List[dict]:
    """
    Fetch data from the given URL with specified query parameters.
    """
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")


@app.post("/login")
def login(user_data: UserLogin):
    """
    endpoint for dummy login and returning the dummpy access token
    """
    if user_data.username == USERNAME and user_data.password == PASSWORD:
        return {"access_token": ACCESS_TOKEN}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/fund-families", dependencies=[Depends(authenticate_access_token)])
def get_fund_families():
    """
    Endpoint to get all the fund details
    """
    url = f"{base_url}/latest"
    params = {"Scheme_Type": "Open"}
    schemes_data = fetch_data(url, params)

    schemes = [MutualFundScheme(**scheme).dict() for scheme in schemes_data]
    families = sorted(set(scheme.get('mutual_fund_family') for scheme in schemes))
    return {"families": families}


@app.get("/fund-schemes", dependencies=[Depends(authenticate_access_token)])
def get_fund_schemes(family: str):
    """
    Endpoint to get details for the perticular fund family
    """
    url = f"{base_url}/latest"
    params = {"Scheme_Type": "Open", "Mutual_Fund_Family": family}
    schemes_data = fetch_data(url, params)

    schemes = [MutualFundScheme(**scheme).dict() for scheme in schemes_data]
    return {"schemes": schemes}


@app.post("/purchase", dependencies=[Depends(authenticate_access_token)])
def purchase_units(isin: str, units: int):
    """
    Endpoint to purchase of units for a selected mutual fund
    """
    url = f"{base_url}/master"
    params = {"ISIN": isin}
    respons_json = fetch_data(url, params)

    if not respons_json:
        return {"status": 503, "message": "No records found!"}

    for option in respons_json:
        if option["Purchase_Allowed"] and option["Minimum_Purchase_Amount"] <= units:
            return {"status": 200, "message": f"Successfully purchased {units} units"}

    return {"status": 400, "message": "Units do not meet the minimum purchase requirements"}