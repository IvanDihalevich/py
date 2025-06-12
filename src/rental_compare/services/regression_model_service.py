# src/rental_compare/services/regression_model_service.py

import json
from sqlalchemy.orm import Session
from typing import List, Optional
from rental_compare.db.models import RegressionModel         # ← Ось цей рядок
from rental_compare.schemas.regression_model import RegressionModelCreate

def create_regression_model(db: Session, model_data: RegressionModelCreate) -> RegressionModel:
    db_model = RegressionModel(
        name=model_data.name,
        intercept=model_data.intercept,
        coefficients=model_data.coefficients,               # JSON column
        feature_descriptions=[fd.dict() for fd in model_data.feature_descriptions],
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_regression_model(db: Session, model_id: int) -> Optional[RegressionModel]:
    return db.query(RegressionModel).filter(RegressionModel.id == model_id).first()

def get_all_regression_models(db: Session, skip: int = 0, limit: int = 100) -> List[RegressionModel]:
    return db.query(RegressionModel).offset(skip).limit(limit).all()

def delete_regression_model(db: Session, model_id: int) -> bool:
    db_model = db.query(RegressionModel).filter(RegressionModel.id == model_id).first()
    if not db_model:
        return False
    db.delete(db_model)
    db.commit()
    return True

def predict_with_model(db: Session, model_id: int, input_values: List[float]) -> float:
    model = get_regression_model(db, model_id)
    if not model:
        raise ValueError("Model not found")
    coeffs = model.coefficients
    if len(input_values) != len(coeffs):
        raise ValueError("Input length does not match number of coefficients")
    return model.intercept + sum(c * x for c, x in zip(coeffs, input_values))
