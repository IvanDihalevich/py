from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import json

class FeatureDescription(BaseModel):
    name: str
    description: str

class RegressionModelBase(BaseModel):
    name: str
    intercept: float
    coefficients: List[float]
    feature_descriptions: List[FeatureDescription]

    @validator('coefficients', pre=True)
    def parse_coefficients(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

    @validator('feature_descriptions', pre=True)
    def parse_feature_descriptions(cls, v):
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

    @validator('input_values', each_item=True)
    def non_negative(cls, v):
        if v < 0:
            raise ValueError('each input value must be non-negative')
        return v

class PredictionResponse(BaseModel):
    prediction: float
