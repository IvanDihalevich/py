from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from rental_compare.schemas.platform import PlatformCreate, PlatformRead
from rental_compare.db.models import Platform
from rental_compare.db.session import get_db

router = APIRouter(prefix="/platforms", tags=["platforms"])


@router.post("/", response_model=PlatformRead, status_code=status.HTTP_201_CREATED)
def create_platform(pl: PlatformCreate, db: Session = Depends(get_db)):
    data = pl.dict()
    data["search_url_template"] = str(data["search_url_template"])
    db_pl = Platform(**data)
    db.add(db_pl)
    db.commit()
    db.refresh(db_pl)
    return db_pl


@router.get("/", response_model=list[PlatformRead])
def read_all_platforms(db: Session = Depends(get_db)):
    return db.query(Platform).all()


@router.get("/{platform_id}", response_model=PlatformRead)
def read_platform(platform_id: int, db: Session = Depends(get_db)):
    pl = db.get(Platform, platform_id)
    if not pl:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Platform not found")
    return pl


@router.put("/{platform_id}", response_model=PlatformRead)
def update_platform(platform_id: int, pl_data: PlatformCreate, db: Session = Depends(get_db)):
    pl = db.get(Platform, platform_id)
    if not pl:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Platform not found")
    for key, value in pl_data.dict().items():
        setattr(pl, key, value)
    db.commit()
    db.refresh(pl)
    return pl


@router.delete("/{platform_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_platform(platform_id: int, db: Session = Depends(get_db)):
    pl = db.get(Platform, platform_id)
    if not pl:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Platform not found")
    db.delete(pl)
    db.commit()
    return None
