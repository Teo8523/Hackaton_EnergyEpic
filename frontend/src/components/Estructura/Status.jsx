import "../../Styles/Status.css"

export default function Status({ value }) {
    return (
        <section className="status card">
            <h3>Estado general</h3>
            <p>
                {value > 150 ? " Consumo alto" : " Consumo controlado"}
            </p>
        </section>
    );
}
