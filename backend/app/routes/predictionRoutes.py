from fastapi import APIRouter
from app.controllers.predictionController import predict

router = APIRouter()

router.post(
    "",
    response_model=None,  # se define en el controller
)(predict)
