from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Optional
import json

class PredictionLogBase(BaseModel):
    model_id: int
    input_values: List[float]
    prediction: float

    @validator('model_id')
    def model_id_positive(cls, v):
        if v <= 0:
            raise ValueError('model_id must be positive')
        return v

    @validator('input_values', each_item=True)
    def input_non_negative(cls, v):
        if v < 0:
            raise ValueError('input values must be non-negative')
        return v

class PredictionLogCreate(PredictionLogBase):
    pass

class PredictionLogRead(PredictionLogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True