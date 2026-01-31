import { useState, useRef, useEffect } from "react";
import "../../Styles/Chatbot.css";

export default function Chatbot({ prediction, explanation, formData }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        {
            role: "assistant",
            content: "👋 ¡Hola! Soy tu asistente energético con IA. Pregúntame sobre el consumo, cómo reducirlo, o cualquier duda que tengas."
        }
    ]);
    const [inputValue, setInputValue] = useState("");
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Generar respuesta con IA REAL
 const generateAIResponse = async (userMessage) => {
    try {
        const context = buildContext();

        const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userMessage,
                context
            })
        });

        const data = await response.json();
        return data.reply;

    } catch (error) {
        console.error(error);
        return "🤖 Estoy teniendo problemas técnicos, intenta de nuevo.";
    }
};

    const buildContext = () => {
        const pred = prediction || "No disponible";
        const status = prediction > 150 ? "alto ⚠️" : "normal ✅";
        const temp = formData?.temperatura_exterior_c || "N/A";
        const ocupacion = formData?.ocupacion_pct ? (formData.ocupacion_pct * 100).toFixed(0) : "N/A";
        const hora = formData?.hora || "N/A";
        const agua = formData?.agua_litros || "N/A";
        const potencia = formData?.potencia_total_kw || "N/A";
        const energiaSalones = formData?.energia_salones_kwh || "N/A";
        const isWeekend = formData?.es_fin_semana ? "Sí" : "No";
        const isFestivo = formData?.es_festivo ? "Sí" : "No";

        const factores = explanation?.qualitative || [];
        
        return `
- Consumo energético predicho: ${pred} kWh
- Estado: Consumo ${status}
- Temperatura exterior: ${temp}°C
- Nivel de ocupación: ${ocupacion}%
- Hora del día: ${hora}:00
- Consumo de agua: ${agua} litros
- Potencia total instalada: ${potencia} kW
- Energía en salones: ${energiaSalones} kWh
- Es fin de semana: ${isWeekend}
- Es día festivo: ${isFestivo}

Factores que más impactan el consumo:
${factores.map(f => `• ${f}`).join('\n')}
        `;
    };

    const handleSend = async () => {
        if (!inputValue.trim()) return;

        const userMessage = {
            role: "user",
            content: inputValue
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue("");
        setLoading(true);

        try {
            // Llamar a IA REAL
            const aiResponse = await generateAIResponse(inputValue);

            const assistantMessage = {
                role: "assistant",
                content: aiResponse
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            const errorMessage = {
                role: "assistant",
                content: "❌ Lo siento, hubo un error. ¿Puedes intentar de nuevo?"
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Preguntas rápidas sugeridas
    const quickQuestions = [
        "¿Cómo puedo reducir el consumo?",
        "¿Por qué es alto el consumo?",
        "Dame consejos de ahorro",
        "¿Cuál es mi consumo actual?"
    ];

    return (
        <>
            {/* Botón flotante */}
            <button 
                className={`chatbot-toggle ${isOpen ? 'open' : ''}`}
                onClick={() => setIsOpen(!isOpen)}
                title="Asistente energético con IA"
            >
                {isOpen ? '✕' : '🤖'}
            </button>

            {/* Ventana del chat */}
            {isOpen && (
                <div className="chatbot-container">
                    <div className="chatbot-header">
                        <div className="chatbot-header-info">
                            <span className="chatbot-avatar">🤖</span>
                            <div>
                                <h4>Asistente Energético IA</h4>
                                <span className="chatbot-status">Powered by Claude AI</span>
                            </div>
                        </div>
                    </div>

                    <div className="chatbot-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message ${msg.role}`}>
                                <div className="message-content">
                                    {msg.content.split('\n').map((line, i) => (
                                        <p key={i}>{line}</p>
                                    ))}
                                </div>
                            </div>
                        ))}

                        {loading && (
                            <div className="message assistant">
                                <div className="message-content typing">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Preguntas rápidas */}
                    {messages.length <= 2 && !loading && (
                        <div className="quick-questions">
                            <p style={{ fontSize: "12px", color: "#666", marginBottom: "8px" }}>
                                Preguntas sugeridas:
                            </p>
                            {quickQuestions.map((q, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => {
                                        setInputValue(q);
                                        setTimeout(() => handleSend(), 100);
                                    }}
                                    className="quick-question"
                                >
                                    {q}
                                </button>
                            ))}
                        </div>
                    )}

                    <div className="chatbot-input">
                        <input
                            type="text"
                            placeholder="Pregunta lo que quieras..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyPress={handleKeyPress}
                            disabled={loading}
                        />
                        <button 
                            onClick={handleSend}
                            disabled={loading || !inputValue.trim()}
                        >
                            {loading ? '⏳' : '📤'}
                        </button>
                    </div>
                </div>
            )}
        </>
    );
}