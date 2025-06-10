from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from rental_compare.schemas.listing import ListingCreate, ListingRead, ListingUpdate
from rental_compare.db.session import get_db
from rental_compare.services.listing_service import create_listing, get_listing, get_all_listings, update_listing, delete_listing

router = APIRouter(prefix="/listings", tags=["listings"])

@router.post("/", response_model=ListingRead, status_code=status.HTTP_201_CREATED)
def create_listing_endpoint(listing: ListingCreate, db: Session = Depends(get_db)):
    return create_listing(db, listing)

@router.get("/", response_model=List[ListingRead])
def read_listings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_listings(db, skip, limit)

@router.get("/{listing_id}", response_model=ListingRead)
def read_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = get_listing(db, listing_id)
    if not listing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return listing

@router.put("/{listing_id}", response_model=ListingRead)
def update_listing_endpoint(listing_id: int, listing_data: ListingUpdate, db: Session = Depends(get_db)):
    updated = update_listing(db, listing_id, listing_data)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return updated

@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing_endpoint(listing_id: int, db: Session = Depends(get_db)):
    success = delete_listing(db, listing_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return None
