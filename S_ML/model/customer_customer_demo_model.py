# spark_demo/S_ML/model/customer_customer_demo_model.py
from pydantic import BaseModel

class CustomerCustomerDemo(BaseModel):
    customer_id: str
    customer_type_id: str
