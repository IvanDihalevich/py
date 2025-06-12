# src/rental_compare/api/routers/regression_model.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from rental_compare.db.session import get_db
from rental_compare.schemas.regression_model import (
    RegressionModelCreate,
    RegressionModelRead,
    PredictionRequest,
    PredictionResponse,
)
from rental_compare.services.regression_model_service import (
    create_regression_model,
    get_regression_model,
    get_all_regression_models,
    delete_regression_model,
    predict_with_model,
)

router = APIRouter(prefix="/regression-models", tags=["regression-models"])

@router.post("/", response_model=RegressionModelRead, status_code=status.HTTP_201_CREATED)
def create_model_endpoint(model_data: RegressionModelCreate, db: Session = Depends(get_db)):
    return create_regression_model(db, model_data)

@router.get("/", response_model=List[RegressionModelRead])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_regression_models(db, skip, limit)

@router.get("/{model_id}", response_model=RegressionModelRead)
def read_model(model_id: int, db: Session = Depends(get_db)):
    db_model = get_regression_model(db, model_id)
    if not db_model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Model not found")
    return db_model

@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(model_id: int, db: Session = Depends(get_db)):
    if not delete_regression_model(db, model_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Model not found")
    return None

