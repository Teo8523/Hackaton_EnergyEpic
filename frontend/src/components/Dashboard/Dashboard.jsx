import "../../Styles/Dashboard.css"
import Sidebar from "../Estructura/Sidebar"
import Header from "../Estructura/Header"
import Infoenergy from "../Estructura/Info"
import Charts from "../Estructura/Charts"
import Status from "../Estructura/Status"
import Extra from "../Estructura/Extra"

export default function Dashboard() {
    return(
        <div className="dashboard">
            <Sidebar />
            <Header />
            <Infoenergy />
            <Charts />
            <Extra />
            <Status />
        </div>
    )
}