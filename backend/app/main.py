import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.models.mlModel import mlModel

#rutas
from app.routes.index import router as predictionRouter

# Cargar variables de entorno al principio para que esten disponibles globalmente
load_dotenv()

# Configuracionde la aplicacion
project_name = os.getenv("PROJECT_NAME", "EnergyEpic")

version = os.getenv("VERSION", "1.0.0")

# Cargar origenes CORS desde .env, separados por coma, o usar valores por defecto
frontend_origins_str = os.getenv("FRONTEND_ORIGINS",
                            "http://localhost:5173," \
                            "http://localhost:3000," \
                            "http://127.0.0.1:5173," \
                            "http://127.0.0.1:3000," \
                            "https://localhost:5173," \
                            "https://127.0.0.1:5173")

origins = [origin.strip() for origin in frontend_origins_str.split(',')]

# Inicializacion unica de la aplicación FastAPI
app = FastAPI(
    title=project_name,
    version=version,
    description="Backend para el sistema de ahorro",
)


# Configuración del middleware CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Lista de orígenes permitidos
    allow_credentials=True,      # Permitir cookies y auth headers
    allow_methods=["*"],         # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],         # Permitir todos los headers
    expose_headers=["*"],        # Exponer todos los headers al frontend
    max_age=600,                 # Cachear preflight requests por 10 minutos
)

#rutas
app.include_router(predictionRouter)


@app.on_event("startup")
def load_model():
    mlModel.load()

# - Endpoints de Salud y Raiz
@app.get("/", summary="Estado de la API Principal")
def root_check(): 
    return {
        "status": "ok", 
        "message": f"{project_name} API operativa",
        "version": version,
        "cors_enabled": True,
        "allowed_origins": origins
    }
app.include_router(chat_router)

@app.get("/health", summary="Estado de Salud del Servicio")
def health():
    return {"status": "ok"}