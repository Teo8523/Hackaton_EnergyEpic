import "../../Styles/Dashboard.css"
import { useState, useEffect } from "react"
import { predictEnergy } from "../../services/predictionService"

import Sidebar from "../Estructura/Sidebar"
import Header from "../Estructura/Header"
import Infoenergy from "../Estructura/Info"
import Charts from "../Estructura/Charts"
import Status from "../Estructura/Status"
import Extra from "../Estructura/Extra"
import Chatbot from "../Dashboard/Chatbot"

export default function Dashboard() {
    const [loading, setLoading] = useState(false);
    const [prediction, setPrediction] = useState(null);
    const [explanation, setExplanation] = useState(null);
    const [error, setError] = useState(null);

    
    const now = new Date();
    const [formData, setFormData] = useState({
        temperatura_exterior_c: 18,
        ocupacion_pct: 0.6,
        hora: now.getHours(),
        dia_semana: now.getDay(),
        mes: now.getMonth() + 1,
        anio: now.getFullYear(),
        es_fin_semana: now.getDay() === 0 || now.getDay() === 6,
        es_festivo: false,
        agua_litros: 1200,
        potencia_total_kw: 300,
        energia_salones_kwh: 200
    });

    
    useEffect(() => {
        getPrediction();
    }, []);

    const getPrediction = async () => {
        setLoading(true);
        setError(null);

        try {
            console.log(" Datos enviados:", formData);
            
            const data = await predictEnergy(formData);
            console.log(" Respuesta recibida:", data);

            setPrediction(data.prediction_kwh);
            setExplanation(data.explanation);

        } catch (err) {
            console.error(" Error:", err);
            setError(err.message || "Error al obtener la predicción");
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;

        const newValue = type === 'checkbox' ? checked :
                        type === 'number' ? parseFloat(value) || 0 : 
                        value;

        console.log(`🔄 Cambiando ${name} a:`, newValue);

        setFormData(prev => ({
            ...prev,
            [name]: newValue
        }));
    };

    
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(" RECALCULANDO con nuevos datos:", formData);
        getPrediction();
    };

    return (
        <div className="dashboard-container">
            <Sidebar />

            <div className="main-content">
                <Header />

                {/* Panel de control */}
                <section className="controls card">
                    <h3>⚙️ Configurar Predicción</h3>
                    <p style={{ fontSize: "14px", color: "#666", marginBottom: "20px" }}>
                        💡 Cambia los valores y presiona "Predecir Consumo" para ver cómo cambia la predicción
                    </p>
                    
                    <form onSubmit={handleSubmit} className="prediction-form">
                        <div className="form-grid">
                            {/* Temperatura */}
                            <div className="form-group">
                                <label>🌡️ Temperatura (°C)</label>
                                <input
                                    type="number"
                                    name="temperatura_exterior_c"
                                    value={formData.temperatura_exterior_c}
                                    onChange={handleInputChange}
                                    min="-20"
                                    max="60"
                                    step="0.1"
                                />
                                <small>Actual: {formData.temperatura_exterior_c}°C</small>
                            </div>

                            {/* Ocupación */}
                            <div className="form-group">
                                <label>👥 Ocupación (%)</label>
                                <input
                                    type="number"
                                    name="ocupacion_pct"
                                    value={formData.ocupacion_pct}
                                    onChange={handleInputChange}
                                    min="0"
                                    max="1"
                                    step="0.01"
                                />
                                <small>Actual: {(formData.ocupacion_pct * 100).toFixed(0)}%</small>
                            </div>

                            {/* Hora */}
                            <div className="form-group">
                                <label>🕐 Hora del día</label>
                                <input
                                    type="number"
                                    name="hora"
                                    value={formData.hora}
                                    onChange={handleInputChange}
                                    min="0"
                                    max="23"
                                />
                                <small>Actual: {formData.hora}:00</small>
                            </div>

                            {/* Agua */}
                            <div className="form-group">
                                <label>💧 Consumo de Agua (L)</label>
                                <input
                                    type="number"
                                    name="agua_litros"
                                    value={formData.agua_litros}
                                    onChange={handleInputChange}
                                    min="0"
                                    step="100"
                                />
                                <small>Actual: {formData.agua_litros}L</small>
                            </div>

                            {/* Potencia */}
                            <div className="form-group">
                                <label>⚡ Potencia Total (kW)</label>
                                <input
                                    type="number"
                                    name="potencia_total_kw"
                                    value={formData.potencia_total_kw}
                                    onChange={handleInputChange}
                                    min="0"
                                    step="10"
                                />
                                <small>Actual: {formData.potencia_total_kw} kW</small>
                            </div>

                            {/* Energía salones */}
                            <div className="form-group">
                                <label>🏫 Energía Salones (kWh)</label>
                                <input
                                    type="number"
                                    name="energia_salones_kwh"
                                    value={formData.energia_salones_kwh}
                                    onChange={handleInputChange}
                                    min="0"
                                    step="10"
                                />
                                <small>Actual: {formData.energia_salones_kwh} kWh</small>
                            </div>

                            {/* Fin de semana */}
                            <div className="form-group checkbox-group">
                                <label>
                                    <input
                                        type="checkbox"
                                        name="es_fin_semana"
                                        checked={formData.es_fin_semana}
                                        onChange={handleInputChange}
                                    />
                                    📅 Fin de semana
                                </label>
                            </div>

                            {/* Festivo */}
                            <div className="form-group checkbox-group">
                                <label>
                                    <input
                                        type="checkbox"
                                        name="es_festivo"
                                        checked={formData.es_festivo}
                                        onChange={handleInputChange}
                                    />
                                    🎉 Día festivo
                                </label>
                            </div>
                        </div>

                        <button
                            type="submit"
                            className="predict-button"
                            disabled={loading}
                        >
                            {loading ? "⏳ Calculando..." : "🔮 Predecir Consumo"}
                        </button>

                        <p style={{ fontSize: "12px", color: "#999", marginTop: "10px", textAlign: "center" }}>
                            Tip: Prueba cambiar la temperatura a 30°C o la ocupación a 0.9
                        </p>
                    </form>
                </section>

                {/* Mensaje de error */}
                {error && (
                    <div className="error-message card" style={{
                        padding: "20px",
                        background: "#fee",
                        border: "1px solid #fcc",
                        borderRadius: "8px",
                        marginBottom: "20px"
                    }}>
                        <p>❌ {error}</p>
                        <small>Verifica que el backend esté corriendo en el puerto correcto</small>
                    </div>
                )}

                {/* Resultados */}
                {!loading && prediction !== null && explanation && (
                    <>
                        <div style={{
                            padding: "10px 20px",
                            background: "#e6f7ff",
                            border: "1px solid #91d5ff",
                            borderRadius: "8px",
                            marginBottom: "20px"
                        }}>
                            <p style={{ margin: 0, fontSize: "14px", color: "#0050b3" }}>
                                ℹ️ Predicción actualizada con los valores actuales
                            </p>
                        </div>

                        <div className="results-grid">
                            {/* Consumo principal */}
                            <Infoenergy value={prediction} />

                            {/* Estado */}
                            <Status value={prediction} />

                            {/* Gráfico de impacto */}
                            <Charts quantitative={explanation.quantitative} />

                            {/* Explicación cualitativa */}
                            <Extra qualitative={explanation.qualitative} />
                        </div>
                    </>
                )}
            </div>

            {/* CHATBOT CON IA REAL */}
            <Chatbot 
                prediction={prediction}
                explanation={explanation}
                formData={formData}
            />
        </div>
    );
}