import "../../Styles/Extra.css"

export default function Extra({ qualitative }) {
    return (
        <section className="extra card">
            <h3>¿Por qué este consumo?</h3>

            <ul>
                {qualitative.map((text, i) => (
                    <li key={i}>{text}</li>
                ))}
            </ul>
        </section>
    );
}