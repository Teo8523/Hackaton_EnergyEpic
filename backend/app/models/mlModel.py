import joblib
import shap
import pandas as pd

MODEL_PATH = "models/rf_model.pkl"

class MLModel:
    def __init__(self):
        self.model = None
        self.explainer = None

    def load(self):
        self.model = joblib.load(MODEL_PATH)
        self.explainer = shap.TreeExplainer(self.model)

    def predict_with_explanation(self, data: dict):
        if self.model is None:
            raise RuntimeError("Modelo no cargado")

        df = pd.DataFrame([data])

        prediction = self.model.predict(df)[0]

        shap_values = self.explainer.shap_values(df)[0]
        explanation = dict(zip(df.columns, shap_values))

        return prediction, explanation


mlModel = MLModel()
