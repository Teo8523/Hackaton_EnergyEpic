from app.schemas.predictionSchema import PredictionInput, PredictionOutput
from app.services.predictionService import predict_energy


def predict(data: PredictionInput) -> PredictionOutput:
    return predict_energy(data)
