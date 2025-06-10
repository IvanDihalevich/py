from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from rental_compare.schemas.listing_data import ListingDataCreate, ListingDataRead
from rental_compare.db.models import Listing, ListingData
from rental_compare.db.session import get_db
from rental_compare.services.listing_data_service import create_listing_data, get_all_listing_data

router = APIRouter(prefix="/listing-data", tags=["listing-data"])


@router.post("/", response_model=ListingDataRead, status_code=status.HTTP_201_CREATED)
def create_listing_data_endpoint(item: ListingDataCreate, db: Session = Depends(get_db)):
    # Перевірка, що оголошення існує
    if not db.get(Listing, item.listing_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Listing not found")
    db_item = create_listing_data(db, item)
    return db_item


@router.get("/listing/{listing_id}", response_model=list[ListingDataRead])
def read_listing_history(
    listing_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    items = (
        db.query(ListingData)
        .filter(ListingData.listing_id == listing_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return items
