from app.models.mlModel import mlModel
from app.services.shapInterpreter import explain_prediction

def predict_energy(data):
    prediction, shap_values = mlModel.predict_with_explanation(data.dict())

    explanations_text = explain_prediction(shap_values)

    return {
        "prediction_kwh": round(prediction, 2),
        "explanation": {
            "quantitative": shap_values,
            "qualitative": explanations_text
        }
    }
