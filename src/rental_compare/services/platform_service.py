from sqlalchemy.orm import Session
from typing import List, Optional

from rental_compare.db.models import Platform
from rental_compare.schemas.platform import PlatformCreate


def create_platform(db: Session, platform_data: PlatformCreate) -> Platform:
    data = platform_data.dict()
    data["search_url_template"] = str(data["search_url_template"])  # Якщо потрібно
    db_platform = Platform(**data)
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform


def get_platform(db: Session, platform_id: int) -> Optional[Platform]:
    return db.get(Platform, platform_id)


def get_all_platforms(db: Session) -> List[Platform]:
    return db.query(Platform).all()


def update_platform(db: Session, platform_id: int, platform_data: PlatformCreate) -> Optional[Platform]:
    platform = db.get(Platform, platform_id)
    if not platform:
        return None
    for key, value in platform_data.dict().items():
        setattr(platform, key, value)
    db.commit()
    db.refresh(platform)
    return platform


def delete_platform(db: Session, platform_id: int) -> bool:
    platform = db.get(Platform, platform_id)
    if not platform:
        return False
    db.delete(platform)
    db.commit()
    return True
