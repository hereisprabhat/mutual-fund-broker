import os
from fastapi import HTTPException, Header
from dotenv import load_dotenv
load_dotenv()


def authenticate_access_token(access_token: str = Header(...)):
    if access_token != os.getenv("ACCESS_TOKEN"):
        raise HTTPException(status_code=401, detail="Invalid access token")