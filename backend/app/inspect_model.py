import joblib

model = joblib.load("app/training/rf_energia_total.pkl")

print("Número de features:", model.n_features_in_)
print("Features del modelo:")
print(model.feature_names_in_)
