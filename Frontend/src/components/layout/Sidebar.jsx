import { NavLink } from 'react-router-dom'
import './Sidebar.css'

const Sidebar = ({ isOpen }) => {
  const menuItems = [
    { path: '/', label: 'Inicio', icon: '🏠' },
    { path: '/vehiculos', label: 'Vehículos', icon: '🚗' },
    { path: '/clientes', label: 'Clientes', icon: '👥' },
    { path: '/alquileres', label: 'Alquileres', icon: '📋' },
    { path: '/reservas', label: 'Reservas', icon: '📅' },
    { path: '/mantenimientos', label: 'Mantenimientos', icon: '🔧' },
    { path: '/reportes', label: 'Reportes', icon: '📊' },
  ]

  return (
    <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
      <nav className="sidebar-nav">
        <ul className="menu-list">
          {menuItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  isActive ? 'menu-item active' : 'menu-item'
                }
                end={item.path === '/'}
              >
                <span className="menu-icon">{item.icon}</span>
                {isOpen && <span className="menu-label">{item.label}</span>}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar
