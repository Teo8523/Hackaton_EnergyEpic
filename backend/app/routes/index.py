from fastapi import APIRouter
from app.routes.predictionRoutes import router as prediction_router

router = APIRouter()

router.include_router(
    prediction_router,
    prefix="/api/predict",
    tags=["Prediction"]
)
