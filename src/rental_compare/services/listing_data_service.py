from sqlalchemy.orm import Session
from typing import List, Optional

from rental_compare.db.models import ListingData
from rental_compare.schemas.listing_data import ListingDataCreate, ListingDataUpdate


def create_listing_data(db: Session, data: ListingDataCreate) -> ListingData:
    listing_data = ListingData(**data.dict())
    db.add(listing_data)
    db.commit()
    db.refresh(listing_data)
    return listing_data


def get_listing_data(db: Session, listing_data_id: int) -> Optional[ListingData]:
    return db.query(ListingData).filter(ListingData.id == listing_data_id).first()


def get_all_listing_data(db: Session, skip: int = 0, limit: int = 100) -> List[ListingData]:
    return db.query(ListingData).offset(skip).limit(limit).all()


def update_listing_data(
    db: Session, listing_data_id: int, data: ListingDataUpdate
) -> Optional[ListingData]:
    listing_data = db.query(ListingData).filter(ListingData.id == listing_data_id).first()
    if not listing_data:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(listing_data, field, value)

    db.commit()
    db.refresh(listing_data)
    return listing_data


def delete_listing_data(db: Session, listing_data_id: int) -> bool:
    listing_data = db.query(ListingData).filter(ListingData.id == listing_data_id).first()
    if not listing_data:
        return False

    db.delete(listing_data)
    db.commit()
    return True
