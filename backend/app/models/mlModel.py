import joblib
import shap
import pandas as pd

MODEL_PATH = "app/training/rf_energia_total.pkl"


class MLModel:
    def __init__(self):
        self.model = None
        self.explainer = None
        self.feature_names = []

        #  Valores por defecto 
        self.default_values = {
            "sede_id": 1,
            "energia_comedor_kwh": 0,
            "energia_salones_kwh": 0,
            "energia_laboratorios_kwh": 0,
            "energia_auditorios_kwh": 0,
            "energia_oficinas_kwh": 0,
            "potencia_total_kw": 0,
            "agua_litros": 0,
            "trimestre": 1,
            "es_semana_parciales": False,
            "es_semana_finales": False,
            "co2_kg": 0,
            "area_m2": 10000,
            "num_estudiantes": 5000,
            "num_empleados": 500,
            "num_edificios": 10,
            "tiene_residencias": False,
            "tiene_laboratorios_pesados": True,
            "altitud_msnm": 2800,
            "temp_promedio_c": 14,
            "pct_comedores": 0.12,
            "pct_salones": 0.25,
            "pct_laboratorios": 0.30,
            "pct_auditorios": 0.08,
            "pct_oficinas": 0.25
        }

    def load(self):
        self.model = joblib.load(MODEL_PATH)
        self.feature_names = list(self.model.feature_names_in_)
        self.explainer = shap.TreeExplainer(self.model)

    def predict_with_explanation(self, data: dict):
        if self.model is None:
            raise RuntimeError("Modelo no cargado")

        #  Unir input del usuario + valores por defecto
        full_data = self.default_values.copy()
        full_data.update(data)

        #  DataFrame con TODAS las columnas
        df = pd.DataFrame([full_data])

        #  Orden EXACTO
        df = df[self.feature_names]

        #  Predicción
        prediction = float(self.model.predict(df)[0])

        #  SHAP
        shap_values = self.explainer.shap_values(df)[0]

        explanation = {
            feature: float(shap_values[i])
            for i, feature in enumerate(self.feature_names)
        }

        return prediction, explanation


mlModel = MLModel()
