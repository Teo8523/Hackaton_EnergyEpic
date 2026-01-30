from app.models.mlModel import mlModel

def predict_energy(data):
    prediction, explanation = mlModel.predict_with_explanation(data.dict())

    return {
        "prediction_kwh": round(prediction, 2),
        "explanation": explanation
    }
