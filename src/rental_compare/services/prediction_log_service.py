from sqlalchemy.orm import Session
from typing import List, Optional
from rental_compare.db.models import PredictionLog
from rental_compare.schemas.prediction_log import PredictionLogCreate


def create_prediction_log(db: Session, log_data: PredictionLogCreate) -> PredictionLog:
    db_log = PredictionLog(
        model_id=log_data.model_id,
        input_values=log_data.input_values,
        prediction=log_data.prediction,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_prediction_log(db: Session, log_id: int) -> Optional[PredictionLog]:
    return db.query(PredictionLog).filter(PredictionLog.id == log_id).first()


def get_all_prediction_logs(db: Session, skip: int = 0, limit: int = 100) -> List[PredictionLog]:
    return db.query(PredictionLog).offset(skip).limit(limit).all()


def delete_prediction_log(db: Session, log_id: int) -> bool:
    log = db.query(PredictionLog).filter(PredictionLog.id == log_id).first()
    if not log:
        return False
    db.delete(log)
    db.commit()
    return True