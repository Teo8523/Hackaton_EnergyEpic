import pandas as pd

# Lecturas energéticas

df_readings = pd.read_csv(
    "data/readings.csv",
    encoding="latin1"
)

# Maestro de sedes
df_sedes = pd.read_csv(
    "data/sedes.csv",
    encoding="latin1"
)

print(df_readings.shape)
print(df_sedes.shape)

def fix_text(series):
    return series.str.encode("latin1").str.decode("utf-8")

# Lecturas
df_readings["sede"] = fix_text(df_readings["sede"])

# Sedes
df_sedes["sede"] = fix_text(df_sedes["sede"])
df_sedes["nombre_completo"] = fix_text(df_sedes["nombre_completo"])
df_sedes["ciudad"] = fix_text(df_sedes["ciudad"])

bool_cols = [
    "tiene_residencias",
    "tiene_laboratorios_pesados"
]

for col in bool_cols:
    df_sedes[col] = df_sedes[col].astype(bool)

df = df_readings.merge(
    df_sedes,
    on="sede_id",
    how="left",
    validate="many_to_one"
)

print("Dataset final:", df.shape)

df = df.rename(columns={
    "sede_x": "sede_lectura",
    "sede_y": "sede"
})


df = df.drop(columns=["sede_lectura"])


df = df.rename(columns={"aÃ±o": "anio"})

print(
    df.loc[df["sede_id"] == "UPTC_CHI",
           ["sede", "nombre_completo", "ciudad", "area_m2", "num_estudiantes"]]
    .head()
)


DROP_COLS = [
    "reading_id",
    "timestamp",
    "dia_nombre",
    "periodo_academico",
    "sede",
    "nombre_completo",
    "ciudad"
]

df_model = df.drop(columns=DROP_COLS)


TARGET = "energia_total_kwh"

X = df_model.drop(columns=[TARGET])
y = df_model[TARGET]

import json

feature_names = X.columns.tolist()

with open("feature_list.json", "w") as f:
    json.dump(feature_names, f, indent=2)

print("Features guardadas:", len(feature_names))


print("X:", X.shape)
print("y:", y.shape)


# Convertir booleanos a int
bool_cols = X.select_dtypes(include=["bool"]).columns
X[bool_cols] = X[bool_cols].astype(int)

# Asegurar todo numérico
X = X.apply(pd.to_numeric, errors="coerce")

# Rellenar nulos
X = X.fillna(X.median())
# Convertir booleanos a int
bool_cols = X.select_dtypes(include=["bool"]).columns
X[bool_cols] = X[bool_cols].astype(int)

# Asegurar todo numérico
X = X.apply(pd.to_numeric, errors="coerce")

# Rellenar nulos
X = X.fillna(X.median())


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

from sklearn.metrics import mean_squared_error
import numpy as np

y_pred = rf.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE:", rmse)

import joblib

joblib.dump(rf, "rf_energia_total.pkl")
print("Modelo guardado ✔")
