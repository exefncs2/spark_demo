# spark_demo/S_ML/model/customers_model.py
from typing import Optional
from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: str
    company_name: str
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
