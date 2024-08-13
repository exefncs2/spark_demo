# spark_demo/S_ML/model/wine_quality_red_model.py
from pydantic import BaseModel, Field

class WineQualityRed(BaseModel):
    id: str
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float
    quality: int

    class Config:
        orm_mode = True
