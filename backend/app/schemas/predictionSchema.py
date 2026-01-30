from pydantic import BaseModel

class PredictionInput(BaseModel):
    hora: int
    diaSemana: int
    mes: int
    temperaturaExterior_c: float
    ocupacionPct: float
    esFinSemana: bool
    esFestivo: bool

class PredictionOutput(BaseModel):
    predictionKwh: float
    explanation: dict
