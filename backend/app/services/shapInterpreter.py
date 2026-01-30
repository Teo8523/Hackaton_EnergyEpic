FEATURE_DESCRIPTIONS = {
    "ocupacion_pct": "el nivel de ocupación del edificio",
    "hora": "el horario de uso",
    "temperatura_exterior_c": "la temperatura exterior",
    "es_fin_semana": "el hecho de ser fin de semana",
    "es_festivo": "el hecho de ser día festivo",
    "agua_litros": "el consumo de agua",
}

def explain_prediction(shap_values: dict, top_n: int = 5):
    explanations = []

    sorted_features = sorted(
        shap_values.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    for feature, value in sorted_features[:top_n]:
        description = FEATURE_DESCRIPTIONS.get(feature, feature)

        if value > 0:
            text = f"{description.capitalize()} aumentó el consumo energético."
        else:
            text = f"{description.capitalize()} ayudó a reducir el consumo energético."

        explanations.append(text)

    return explanations
