import json
from sqlalchemy.orm import Session
from typing import List, Optional
from rental_compare.db.models import RegressionModel
from rental_compare.schemas.regression_model import RegressionModelCreate


def create_regression_model(db: Session, model_data: RegressionModelCreate) -> RegressionModel:
    db_model = RegressionModel(
        name=model_data.name,
        intercept=model_data.intercept,
        coefficients=json.dumps(model_data.coefficients),  # зберігаємо як JSON-рядок
        features=json.dumps(model_data.features),          # зберігаємо як JSON-рядок
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def get_regression_model(db: Session, model_id: int) -> Optional[RegressionModel]:
    model = db.query(RegressionModel).filter(RegressionModel.id == model_id).first()
    # НЕ міняємо model.coefficients і model.features тут
    return model


def get_all_regression_models(db: Session, skip: int = 0, limit: int = 100) -> List[RegressionModel]:
    models = db.query(RegressionModel).offset(skip).limit(limit).all()
    # НЕ міняємо поля тут
    return models


def delete_regression_model(db: Session, model_id: int) -> bool:
    db_model = db.query(RegressionModel).filter(RegressionModel.id == model_id).first()
    if not db_model:
        return False
    db.delete(db_model)
    db.commit()
    return True
def predict_with_model(db: Session, model_id: int, input_values: List[float]) -> float:
    model = db.query(RegressionModel).filter(RegressionModel.id == model_id).first()
    if not model:
        raise ValueError("Model not found")

    coefficients = json.loads(model.coefficients)
    intercept = model.intercept

    if len(input_values) != len(coefficients):
        raise ValueError("Input length does not match number of coefficients")

    prediction = intercept + sum(c * x for c, x in zip(coefficients, input_values))
    return prediction
