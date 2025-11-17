import { Link } from 'react-router-dom'
import './Home.css'

const Home = () => {
  const modules = [
    {
      title: 'Vehículos',
      description: 'Gestión de la flota de vehículos',
      icon: '🚗',
      path: '/vehiculos',
      color: '#3b82f6'
    },
    {
      title: 'Clientes',
      description: 'Administración de clientes',
      icon: '👥',
      path: '/clientes',
      color: '#10b981'
    },
    {
      title: 'Alquileres',
      description: 'Gestión de alquileres activos',
      icon: '📋',
      path: '/alquileres',
      color: '#f59e0b'
    },
    {
      title: 'Reservas',
      description: 'Reservas anticipadas',
      icon: '📅',
      path: '/reservas',
      color: '#8b5cf6'
    },
    {
      title: 'Mantenimientos',
      description: 'Control de mantenimientos',
      icon: '🔧',
      path: '/mantenimientos',
      color: '#ef4444'
    },
    {
      title: 'Reportes',
      description: 'Estadísticas y reportes',
      icon: '📊',
      path: '/reportes',
      color: '#06b6d4'
    },
  ]

  return (
    <div className="home-page">
      <div className="home-header">
        <h1 className="page-title">Sistema de Gestión de Alquileres</h1>
        <p className="home-subtitle">
          Bienvenido al sistema de gestión de alquileres de vehículos
        </p>
      </div>

      <div className="modules-grid">
        {modules.map((module) => (
          <Link
            key={module.path}
            to={module.path}
            className="module-card"
            style={{ borderTopColor: module.color }}
          >
            <div className="module-icon" style={{ color: module.color }}>
              {module.icon}
            </div>
            <h3 className="module-title">{module.title}</h3>
            <p className="module-description">{module.description}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default Home
