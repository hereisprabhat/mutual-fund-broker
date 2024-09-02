import os
import requests
from dotenv import load_dotenv
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


headers = {"X-RapidAPI-Key": os.getenv("RAPID_API_KEY"), "X-RapidAPI-Host": os.getenv("RAPID_API_URL")}
base_url = "https://" + os.getenv("RAPID_API_URL")


@app.post("/login")
def login(user_data: UserLogin):
    """
    endpoint for dummy login and returning the dummpy access token
    """
    if user_data.username == os.getenv("USERNAME") and user_data.password == os.getenv("PASSWORD"):
        return {"access_token": os.getenv("ACCESS_TOKEN")}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/fund-families", dependencies=[Depends(authenticate_access_token)])
def get_fund_families():
    """
    Endpoint to get all the fund details
    """
    url = base_url + "/latest"

    query_params = {"Scheme_Type": "Open"}

    response = requests.get(url, headers=headers, params=query_params)

    if response.status_code == 200:
        schemes_data = response.json()
        schemes = [
            MutualFundScheme(**scheme).dict() for scheme in schemes_data
        ]
        families = list(set([scheme.get('mutual_fund_family') for scheme in schemes]))
        families.sort()
        return {"families": families}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch all schemes"
        )


@app.get("/fund-schemes", dependencies=[Depends(authenticate_access_token)])
def get_fund_schemes(family: str):
    """
    Endpoint to get details for the perticular fund family
    """
    url = base_url + "/latest"

    query_params = {
        "Scheme_Type": "Open",
        "Mutual_Fund_Family": family
    }

    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code == 200:
        schemes_data = response.json()
        schemes = [
            MutualFundScheme(**scheme).dict() for scheme in schemes_data
        ]
        return {"schemes": schemes}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch fund family"
        )


@app.post("/purchase", dependencies=[Depends(authenticate_access_token)])
def purchase_units(isin: str, units: int):
    """
    Endpoint to purchase of units for a selected mutual fund
    """
    url = base_url + "/master"

    querystring = {"ISIN": isin}

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        respons_json = response.json()
        if not respons_json:
            return {
                "status": 503,
                "message": "No records found !"
            }
        for option in respons_json:
            if option["Purchase_Allowed"] and option["Minimum_Purchase_Amount"] >= units:
                return {
                    "status": 200,
                    "message": f"Successfully purchased {units} units"
                }
        return {
            "status": 400,
            "message": "Units not satisfying the minimum desired values"
        }
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Unexpected error occured"
        )