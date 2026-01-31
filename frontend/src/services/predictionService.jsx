// Servicio para hacer predicciones de consumo energético

export const predictEnergy = async (formData) => {
    try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        
        console.log("🔵 Enviando datos al backend:", formData);
        
        const response = await fetch("http://127.0.0.1:8000/api/predict", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en la predicción');
        }

        const data = await response.json();
        console.log("🟢 Respuesta del backend:", data);
        
        return data;
        
    } catch (error) {
        console.error("🔴 Error en predictEnergy:", error);
        throw new Error(error.message || 'Error conectando con el servidor');
    }
};