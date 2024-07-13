# spark_demo/S_ML/model/categories_model.py
from typing import Optional
from pydantic import BaseModel

class Category(BaseModel):
    category_id: int
    category_name: str
    description: Optional[str] = None
    picture: Optional[bytes] = None
