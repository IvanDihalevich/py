from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from rental_compare.db.models import ListingData

from rental_compare.schemas.listing_data import ListingDataCreate, ListingDataRead, ListingDataUpdate
from rental_compare.db.models import Listing
from rental_compare.db.session import get_db
from rental_compare.services.listing_data_service import (
    create_listing_data,
    get_all_listing_data,
    get_listing_data,
    update_listing_data,
    delete_listing_data,
)

router = APIRouter(prefix="/listing-data", tags=["listing-data"])


@router.post("/", response_model=ListingDataRead, status_code=status.HTTP_201_CREATED)
def create_listing_data_endpoint(item: ListingDataCreate, db: Session = Depends(get_db)):
    # Перевірка, що оголошення існує
    if not db.get(Listing, item.listing_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Listing not found")
    return create_listing_data(db, item)


@router.get("/", response_model=List[ListingDataRead])
def read_all_listing_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_listing_data(db, skip, limit)


@router.get("/{listing_data_id}", response_model=ListingDataRead)
def read_listing_data(listing_data_id: int, db: Session = Depends(get_db)):
    listing_data = get_listing_data(db, listing_data_id)
    if not listing_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="ListingData not found")
    return listing_data


@router.get("/listing/{listing_id}", response_model=List[ListingDataRead])
def read_listing_history(listing_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Історія по одному listing_id
    return (
        db.query(ListingData)
        .filter(ListingData.listing_id == listing_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.put("/{listing_data_id}", response_model=ListingDataRead)
def update_listing_data_endpoint(listing_data_id: int, data: ListingDataUpdate, db: Session = Depends(get_db)):
    listing_data = update_listing_data(db, listing_data_id, data)
    if not listing_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="ListingData not found")
    return listing_data


@router.delete("/{listing_data_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing_data_endpoint(listing_data_id: int, db: Session = Depends(get_db)):
    success = delete_listing_data(db, listing_data_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="ListingData not found")
    return None
