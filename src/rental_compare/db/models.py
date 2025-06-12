from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    search_url_template = Column(Text, nullable=False)

    listings = relationship("Listing", back_populates="platform")


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    external_id = Column(String, index=True, nullable=False)
    url = Column(Text, nullable=False)
    title = Column(String, nullable=True)
    location = Column(String, nullable=True)

    platform = relationship("Platform", back_populates="listings")
    data = relationship("ListingData", back_populates="listing")


class ListingData(Base):
    __tablename__ = "listing_data"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, nullable=True)
    scraped_at = Column(DateTime, nullable=False)

    listing = relationship("Listing", back_populates="data")

class RegressionModel(Base):
    __tablename__ = "regression_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    intercept = Column(Float, nullable=False)
    coefficients = Column(JSON, nullable=False)            # список коефіцієнтів
    feature_descriptions = Column(JSON, nullable=False)    # [{"name": ..., "description": ...}, ...]
    trained_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, nullable=False)
    input_values = Column(JSON, nullable=False)
    prediction = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)