# setup.py
from setuptools import setup, find_packages

setup(
    name="rental_compare",
    version="0.1.0",
    description="Порівняння вартості оренди на Airbnb і Booking",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "sqlalchemy",
        "alembic",
        "playwright",
        "beautifulsoup4",
        "statsmodels",
        "psycopg2-binary",
    ],
    python_requires=">=3.10",
)
