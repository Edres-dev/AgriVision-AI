from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.ml import router as ml_router
from app.db.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgriVision AI API",
    swagger_ui_parameters={"operationsSorter": "method"},
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(ml_router)


@app.get("/")
def root():
    return {"message": "AgriVision AI API is running."}
