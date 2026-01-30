from pydantic import BaseModel,Field
from typing import Dict, List

class PredictionInput(BaseModel):
    # Variables operativas
    temperatura_exterior_c: float = Field(..., ge=-20, le=60)
    ocupacion_pct: float = Field(..., ge=0, le=1) # 0.5 es la mitad de ocupacion

    # Tiempo
    hora: int = Field(..., ge=0, le=23)
    dia_semana: int = Field(..., ge=0, le=6)  # 0=Domingo, 6=Sábado
    mes: int = Field(..., ge=1, le=12) #12=Diciembre 1=Enero
    anio: int = Field(..., ge=2000, le=2100)

    # Flags
    es_fin_semana: bool
    es_festivo: bool

    # Opcional - Infraestructura
    agua_litros: float = Field(None, ge=0)



class Explanation(BaseModel):
    quantitative: Dict[str, float]
    qualitative: List[str]

class PredictionOutput(BaseModel):
    prediction_kwh: float
    explanation: Explanation
