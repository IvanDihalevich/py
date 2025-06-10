from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from rental_compare.schemas.listing import ListingCreate, ListingRead, ListingUpdate
from rental_compare.db.models import Listing
from rental_compare.db.session import get_db

router = APIRouter(prefix="/listings", tags=["listings"])

@router.post("/", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
def create_listing(listing: ListingCreate, db: Session = Depends(get_db)):
    db_listing = Listing(
        external_id=listing.external_id,
        url=str(listing.url),  # перетворення HttpUrl у str
        title=listing.title,
        location=listing.location,
        platform_id=listing.platform_id,
    )
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@router.get("/", response_model=List[ListingRead])
def read_listings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Listing).offset(skip).limit(limit).all()

@router.get("/{listing_id}", response_model=ListingRead)
def read_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return listing

@router.put("/{listing_id}", response_model=ListingRead)
def update_listing(listing_id: int, data: ListingUpdate, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Listing not found")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "url" and value is not None:
            setattr(listing, key, str(value))  # перетворення HttpUrl у str
        else:
            setattr(listing, key, value)
    db.commit()
    db.refresh(listing)
    return listing

@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Listing not found")
    db.delete(listing)
    db.commit()
    return None
