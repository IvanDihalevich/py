# main.py
from fastapi import FastAPI
from rental_compare.api.routers import platform, listing, listing_data, regression_model, prediction_log
...

app = FastAPI(title="Rental Compare API")

app.include_router(platform.router)
app.include_router(listing.router)
app.include_router(listing_data.router)
app.include_router(regression_model.router)
app.include_router(prediction_log.router)