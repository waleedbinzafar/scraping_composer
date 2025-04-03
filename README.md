
# Alembic Migration Example
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Running the app
uvicorn main:app --reload

