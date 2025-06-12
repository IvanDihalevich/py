# src/rental_compare/api/routers/prediction_log.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from rental_compare.db.session import get_db
from rental_compare.schemas.prediction_log import PredictionLogCreate, PredictionLogRead
from rental_compare.services.prediction_log_service import (
    create_prediction_log,
    get_prediction_log,
    get_all_prediction_logs,
    delete_prediction_log,
)

router = APIRouter(prefix="/prediction-logs", tags=["prediction-logs"])

@router.post("/", response_model=PredictionLogRead, status_code=status.HTTP_201_CREATED)
def create_log_endpoint(log_data: PredictionLogCreate, db: Session = Depends(get_db)):
    return create_prediction_log(db, log_data)

@router.get("/", response_model=List[PredictionLogRead])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_prediction_logs(db, skip, limit)

@router.get("/{log_id}", response_model=PredictionLogRead)
def read_log(log_id: int, db: Session = Depends(get_db)):
    db_log = get_prediction_log(db, log_id)
    if not db_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    return db_log

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    if not delete_prediction_log(db, log_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    return None
