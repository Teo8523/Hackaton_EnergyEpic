from fastapi import APIRouter, HTTPException
from app.schemas.predictionSchema import PredictionInput, PredictionOutput
from app.controllers.predictionController import predict

router = APIRouter()

@router.post("/", response_model=PredictionOutput)
async def predict_endpoint(data: PredictionInput):
    """
    Endpoint para predecir el consumo energético
    """
    try:
        result = predict(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Verificar que el servicio de predicción esté funcionando
    """
    return {"status": "ok", "service": "prediction"}
