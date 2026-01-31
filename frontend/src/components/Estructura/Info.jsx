import "../../Styles/Infoenergy.css"

export default function Infoenergy({ value }) {
    // Clasificar el consumo
    const getConsumptionLevel = (kwh) => {
        if (kwh < 100) return { label: "Bajo", emoji: "💚", color: "#48bb78" };
        if (kwh < 200) return { label: "Normal", emoji: "💛", color: "#ecc94b" };
        if (kwh < 300) return { label: "Alto", emoji: "🧡", color: "#ed8936" };
        return { label: "Muy Alto", emoji: "❤️", color: "#f56565" };
    };

    const level = getConsumptionLevel(value);

    return (
        <section className="info card" style={{ borderLeft: `6px solid ${level.color}` }}>
            <div className="info-header">
                <span className="emoji">{level.emoji}</span>
                <h3>Consumo Estimado</h3>
            </div>
            
            <div className="consumption-value">
                <h1>{value.toFixed(2)}</h1>
                <span className="unit">kWh</span>
            </div>
            
            <div className="consumption-level" style={{ color: level.color }}>
                <span className="level-badge" style={{ background: level.color }}>
                    {level.label}
                </span>
            </div>

            <div className="info-footer">
                <p>Basado en las condiciones actuales</p>
            </div>
        </section>
    );
}