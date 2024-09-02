from typing import Optional
from pydantic import BaseModel, Field


class MutualFundScheme(BaseModel):
    scheme_code: int = Field(alias="Scheme_Code")
    scheme_name: str = Field(alias="Scheme_Name")
    scheme_type: str = Field(alias="Scheme_Type")
    scheme_category: str = Field(alias="Scheme_Category")
    isin_div_payout: str = Field(alias="ISIN_Div_Payout_ISIN_Growth")
    isin_div_reinvestment: Optional[str] = Field(alias="ISIN_Div_Reinvestment")
    net_asset_value: float = Field(alias="Net_Asset_Value")
    date: str = Field(alias="Date")
    mutual_fund_family: str = Field(alias="Mutual_Fund_Family")


class FundFamilyRequest(BaseModel):
    family: str


class UserLogin(BaseModel):
    username: str
    password: str