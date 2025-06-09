from fastapi import FastAPI
from rental_compare.api.routers import platform

app = FastAPI(title="Rental Compare API")
app.include_router(platform.router)
