from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from rental_compare.schemas.platform import PlatformCreate, PlatformRead
from rental_compare.db.session import get_db
from rental_compare.services.platform_service import (
    create_platform,
    get_platform,
    get_all_platforms,
    update_platform,
    delete_platform,
)

router = APIRouter(prefix="/platforms", tags=["platforms"])


@router.post("/", response_model=PlatformRead, status_code=status.HTTP_201_CREATED)
def create_platform_endpoint(pl: PlatformCreate, db: Session = Depends(get_db)):
    db_pl = create_platform(db, pl)
    return db_pl


@router.get("/", response_model=list[PlatformRead])
def read_all_platforms(db: Session = Depends(get_db)):
    return get_all_platforms(db)


@router.get("/{platform_id}", response_model=PlatformRead)
def read_platform(platform_id: int, db: Session = Depends(get_db)):
    pl = get_platform(db, platform_id)
    if not pl:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Platform not found")
    return pl


@router.put("/{platform_id}", response_model=PlatformRead)
def update_platform_endpoint(platform_id: int, pl_data: PlatformCreate, db: Session = Depends(get_db)):
    pl = update_platform(db, platform_id, pl_data)
    if not pl:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Platform not found")
    return pl


@router.delete("/{platform_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_platform_endpoint(platform_id: int, db: Session = Depends(get_db)):
    success = delete_platform(db, platform_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Platform not found")
    return None
