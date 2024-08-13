# spark_demo/S_ML/model/wine_quality_white_model.py
from pydantic import BaseModel, Field
from typing import Optional

class WineQualityWhite(BaseModel):
    fixed_acidity: Optional[float] = None
    volatile_acidity: Optional[float] = None
    citric_acid: Optional[float] = None
    residual_sugar: Optional[float] = None
    chlorides: Optional[float] = None
    free_sulfur_dioxide: Optional[float] = None
    total_sulfur_dioxide: Optional[float] = None
    density: Optional[float] = None
    ph: Optional[float] = None
    sulphates: Optional[float] = None
    alcohol: Optional[float] = None
    quality: Optional[int] = None

    class Config:
        orm_mode = True
