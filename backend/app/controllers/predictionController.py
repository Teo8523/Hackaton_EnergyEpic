from fastapi import APIRouter
from app.schemas.predictionSchema import PredictionInput, PredictionOutput
from app.services.predictionService import predict_energy

router = APIRouter(tags=["Prediction"])

@router.post("", response_model=PredictionOutput)
def predict(data: PredictionInput):
    return predict_energy(data)
