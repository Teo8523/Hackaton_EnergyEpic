import pandas as pd
import joblib
import json

# 1. Cargar modelo y features

model = joblib.load("rf_energia_total.pkl")

with open("feature_list.json") as f:
    FEATURES = json.load(f)

print("Modelo:", type(model))
print("Features esperadas:", len(FEATURES))

# 2. Cargar datasets 

df_readings = pd.read_csv("data/readings.csv", encoding="latin1")
df_sedes = pd.read_csv("data/sedes.csv", encoding="latin1")

# 3. Fix encoding

def fix_text(series):
    return series.str.encode("latin1").str.decode("utf-8")

df_readings["sede"] = fix_text(df_readings["sede"])

df_sedes["sede"] = fix_text(df_sedes["sede"])
df_sedes["nombre_completo"] = fix_text(df_sedes["nombre_completo"])
df_sedes["ciudad"] = fix_text(df_sedes["ciudad"])


# 4. Merge

df = df_readings.merge(
    df_sedes,
    on="sede_id",
    how="left",
    validate="many_to_one"
)

df = df.rename(columns={
    "sede_x": "sede_lectura",
    "sede_y": "sede",
    "aÃ±o": "anio"
})

df = df.drop(columns=["sede_lectura"])

# 5. Quitar columnas NO usadas

DROP_COLS = [
    "reading_id",
    "timestamp",
    "dia_nombre",
    "periodo_academico",
    "sede",
    "nombre_completo",
    "ciudad"
]

df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

# 6. Construir X EXACTO

X = df[FEATURES]

# Booleanos a int
bool_cols = X.select_dtypes(include=["bool"]).columns
X[bool_cols] = X[bool_cols].astype(int)

# Todo numérico
X = X.apply(pd.to_numeric, errors="coerce")
X = X.fillna(X.median())

# 7. Predicción REAL

row = X.iloc[[0]]
pred = model.predict(row)

print("Predicción OK:", pred)
