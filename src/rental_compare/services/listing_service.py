from typing import List, Optional
from sqlalchemy.orm import Session
from rental_compare.db.models import Listing
from rental_compare.schemas.listing import ListingCreate, ListingUpdate

def create_listing(db: Session, listing_data: ListingCreate) -> Listing:
    listing = Listing(
        external_id=listing_data.external_id,
        url=str(listing_data.url),  # HttpUrl → str
        title=listing_data.title,
        location=listing_data.location,
        platform_id=listing_data.platform_id
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

def get_listing(db: Session, listing_id: int) -> Optional[Listing]:
    return db.query(Listing).filter(Listing.id == listing_id).first()

def get_all_listings(db: Session, skip: int = 0, limit: int = 100) -> List[Listing]:
    return db.query(Listing).offset(skip).limit(limit).all()

def update_listing(db: Session, listing_id: int, listing_data: ListingUpdate) -> Optional[Listing]:
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        return None
    update_data = listing_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "url" and value is not None:
            setattr(listing, field, str(value))  # HttpUrl → str
        else:
            setattr(listing, field, value)
    db.commit()
    db.refresh(listing)
    return listing

def delete_listing(db: Session, listing_id: int) -> bool:
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        return False
    db.delete(listing)
    db.commit()
    return True
