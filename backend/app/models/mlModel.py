import joblib
import json
import pandas as pd
import numpy as np
import shap
from pathlib import Path

class MLModel:
    def __init__(self):
        self.model = None
        self.features = None
        self.explainer = None
        self.model_path = Path("app/training/rf_energia_total.pkl")
        self.features_path = Path("app/training/feature_list.json")
    
    def load(self):
        """Cargar el modelo y las features al iniciar la aplicación"""
        try:
            # Cargar modelo
            self.model = joblib.load(self.model_path)
            print(f"✓ Modelo cargado: {self.model.n_features_in_} features")
            
            # Cargar lista de features
            with open(self.features_path, 'r') as f:
                self.features = json.load(f)
            print(f"✓ Features cargadas: {len(self.features)}")
            
            # Inicializar SHAP explainer
            self.explainer = shap.TreeExplainer(self.model)
            print("✓ SHAP TreeExplainer inicializado")
            
        except Exception as e:
            print(f"✗ Error cargando modelo: {e}")
            raise
    
    def predict_with_explanation(self, input_data: dict):
        """
        Hacer predicción y calcular valores SHAP reales
        """
        if self.model is None or self.features is None:
            raise ValueError("Modelo no cargado. Llama a load() primero.")
        
        # Crear DataFrame con TODAS las features necesarias
        df = pd.DataFrame([self._prepare_features(input_data)])
        
        # Asegurar que estén en el orden correcto
        df = df[self.features]
        
        # Convertir booleanos a int
        bool_cols = df.select_dtypes(include=['bool']).columns
        df[bool_cols] = df[bool_cols].astype(int)
        
        # Asegurar todo numérico
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.fillna(df.median())
        
        # Predicción
        prediction = self.model.predict(df)[0]
        
        # Calcular SHAP values REALES
        shap_values = self._calculate_shap_values(df)
        
        return float(prediction), shap_values
    
    def _prepare_features(self, input_data: dict):
        """
        Preparar TODAS las features que el modelo necesita
        Rellenar con valores por defecto las que no vienen en el input
        """
        # Features del input del usuario
        features = {
            'temperatura_exterior_c': input_data.get('temperatura_exterior_c', 20),
            'ocupacion_pct': input_data.get('ocupacion_pct', 0.5),
            'hora': input_data.get('hora', 12),
            'dia_semana': input_data.get('dia_semana', 2),
            'mes': input_data.get('mes', 6),
            'anio': input_data.get('anio', 2024),
            'es_fin_semana': int(input_data.get('es_fin_semana', False)),
            'es_festivo': int(input_data.get('es_festivo', False)),
            'agua_litros': input_data.get('agua_litros', 1000),
        }
        
        # ⚠️ FEATURES ADICIONALES que el modelo espera
        # Valores por defecto basados en una sede típica
        default_features = {
            # Información de la sede
            'sede_id': 0,
            'area_m2': 5000,
            'num_estudiantes': 1000,
            'num_empleados': 100,
            'tiene_residencias': 0,
            'tiene_laboratorios_pesados': 0,
            'anio_construccion': 2000,
            'num_edificios': 3,
            'altitud_msnm': 2600,
            
            # Consumo por áreas (proporcional al total estimado)
            'energia_comedor_kwh': 30,
            'energia_salones_kwh': 80,
            'energia_laboratorios_kwh': 60,
            'energia_auditorios_kwh': 20,
            'energia_oficinas_kwh': 40,
            
            # Métricas eléctricas
            'potencia_total_kw': 150,
            
            # Temporales
            'trimestre': (input_data.get('mes', 6) - 1) // 3 + 1,
            'es_semana_parciales': 0,
            'es_semana_finales': 0,
            
            # Ambientales
            'co2_kg': 100,
            'temp_promedio_c': input_data.get('temperatura_exterior_c', 20),
            
            # Porcentajes de distribución (deben sumar ~1.0)
            'pct_comedores': 0.15,
            'pct_salones': 0.35,
            'pct_laboratorios': 0.25,
            'pct_auditorios': 0.10,
            'pct_oficinas': 0.15,
        }
        
        # Combinar todo (prioridad a lo que viene del input)
        for key, value in default_features.items():
            if key not in features:
                features[key] = value
        
        return features
    
    def _calculate_shap_values(self, df):
        """
        Calcular valores SHAP REALES usando TreeExplainer
        """
        # Calcular SHAP values para esta predicción
        shap_values_array = self.explainer.shap_values(df)
        
        # Convertir a diccionario con solo las features más relevantes
        shap_dict = {}
        
        # Features importantes para mostrar al usuario
        important_features = [
            'temperatura_exterior_c',
            'ocupacion_pct', 
            'hora',
            'es_fin_semana',
            'es_festivo',
            'agua_litros',
            'mes',
            'dia_semana',
            'energia_salones_kwh',
            'energia_laboratorios_kwh',
            'potencia_total_kw'
        ]
        
        for feat in important_features:
            if feat in df.columns:
                idx = list(df.columns).index(feat)
                # SHAP value real para esta feature
                shap_dict[feat] = float(shap_values_array[0][idx])
        
        return shap_dict

# Instancia global
mlModel = MLModel()