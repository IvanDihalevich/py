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
    db_model = create_regression_model(db, model_data)
    return db_model


@router.get("/", response_model=List[RegressionModelRead])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_regression_models(db, skip, limit)


@router.get("/{model_id}", response_model=RegressionModelRead)
def read_model(model_id: int, db: Session = Depends(get_db)):
    db_model = get_regression_model(db, model_id)
    if not db_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return db_model


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(model_id: int, db: Session = Depends(get_db)):
    success = delete_regression_model(db, model_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return None


@router.post("/{model_id}/predict", response_model=PredictionResponse)
def predict(model_id: int, input: PredictionRequest, db: Session = Depends(get_db)):
    try:
        result = predict_with_model(db, model_id, input.input_values)
        return PredictionResponse(prediction=result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
