from pathlib import Path

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/predict-yield",
    tags=["Machine Learning"],
)

# Load the model once at startup.
MODEL_PATH = Path("app/ml/yield_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception:
    model = None


class YieldInput(BaseModel):
    country: str
    crop: str
    year: int
    avg_temp: float
    rainfall: float
    pesticides: float


@router.post("/")
def predict_yield(data: YieldInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    input_df = pd.DataFrame(
        [
            {
                "country": data.country,
                "crop": data.crop,
                "year": data.year,
                "avg_temp": data.avg_temp,
                "rainfall": data.rainfall,
                "pesticides": data.pesticides,
            }
        ]
    )

    prediction = model.predict(input_df)[0]

    return {
        "predicted_yield": round(float(prediction), 2),
        "unit": "hg/ha",
    }
