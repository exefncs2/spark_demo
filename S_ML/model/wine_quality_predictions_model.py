# spark_demo/S_ML/model/wine_quality_predictions_model.py
from pydantic import BaseModel

class WineQualityPrediction(BaseModel):
    id: str
    prediction: float
    residual_sugar: float

    class Config:
        orm_mode = True
