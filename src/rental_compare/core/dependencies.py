# src/rental_compare/core/dependencies.py

from sqlalchemy.orm import Session
from fastapi import Depends

from rental_compare.db.session import get_db

def get_db_session() -> Session:
    return Depends(get_db)
