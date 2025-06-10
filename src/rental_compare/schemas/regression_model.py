from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import json


class RegressionModelBase(BaseModel):
    name: str
    intercept: float
    coefficients: List[float]
    features: List[str]

    # Валідатори для автоматичного парсингу JSON-рядка у список, якщо прийде рядок
    @validator('coefficients', pre=True)
    def parse_coefficients(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

    @validator('features', pre=True)
    def parse_features(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class RegressionModelCreate(RegressionModelBase):
    pass


class RegressionModelRead(RegressionModelBase):
    id: int
    trained_at: datetime

    class Config:
        orm_mode = True

class PredictionRequest(BaseModel):
    input_values: List[float]


class PredictionResponse(BaseModel):
    prediction: float
