import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Home from './pages/Home/Home'
import Vehiculos from './pages/Vehiculos/Vehiculos'
import Clientes from './pages/Clientes/Clientes'
import Alquileres from './pages/Alquileres/Alquileres'
import Reservas from './pages/Reservas/Reservas'
import Mantenimientos from './pages/Mantenimientos/Mantenimientos'
import Reportes from './pages/Reportes/Reportes'
import './styles/App.css'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/vehiculos" element={<Vehiculos />} />
          <Route path="/clientes" element={<Clientes />} />
          <Route path="/alquileres" element={<Alquileres />} />
          <Route path="/reservas" element={<Reservas />} />
          <Route path="/mantenimientos" element={<Mantenimientos />} />
          <Route path="/reportes" element={<Reportes />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
