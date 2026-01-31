import "../../Styles/Charts.css"

export default function Charts({ quantitative }) {
    // Ordenar por impacto absoluto
    const sortedData = Object.entries(quantitative)
        .sort(([, a], [, b]) => Math.abs(b) - Math.abs(a))
        .slice(0, 6); // Top 6 variables

    // Encontrar el valor máximo para escalar las barras
    const maxValue = Math.max(...sortedData.map(([, val]) => Math.abs(val)));

    return (
        <section className="charts card">
            <h3>📊 Impacto de Variables</h3>
            <p className="subtitle">Variables que más afectan el consumo</p>

            <div className="chart-container">
                {sortedData.map(([key, val]) => {
                    const isPositive = val > 0;
                    const percentage = (Math.abs(val) / maxValue) * 100;

                    return (
                        <div key={key} className="chart-item">
                            <div className="chart-label">
                                <span className="variable-name">
                                    {formatVariableName(key)}
                                </span>
                                <span className={`value ${isPositive ? 'positive' : 'negative'}`}>
                                    {isPositive ? '+' : ''}{val.toFixed(2)}
                                </span>
                            </div>

                            <div className="chart-bar-container">
                                <div
                                    className={`chart-bar ${isPositive ? 'positive' : 'negative'}`}
                                    style={{ width: `${percentage}%` }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>
        </section>
    );
}

// Función para formatear nombres de variables
function formatVariableName(key) {
    const names = {
        'temperatura_exterior_c': '🌡️ Temperatura',
        'ocupacion_pct': '👥 Ocupación',
        'hora': '🕐 Hora del día',
        'agua_litros': '💧 Consumo agua',
        'es_fin_semana': '📅 Fin de semana',
        'es_festivo': '🎉 Día festivo',
        'mes': '📆 Mes',
        'dia_semana': '📅 Día de semana'
    };

    return names[key] || key;
}