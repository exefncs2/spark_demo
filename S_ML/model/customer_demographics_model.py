# spark_demo/S_ML/model/customer_demographics_model.py
from typing import Optional
from pydantic import BaseModel

class CustomerDemographics(BaseModel):
    customer_type_id: str
    customer_desc: Optional[str] = None
