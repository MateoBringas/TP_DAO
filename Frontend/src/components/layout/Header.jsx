import './Header.css'

const Header = ({ toggleSidebar }) => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-btn" onClick={toggleSidebar}>
          ☰
        </button>
        <h1 className="header-title">Sistema de Gestión de Alquileres</h1>
      </div>
      <div className="header-right">
        <span className="user-info">Usuario: Admin</span>
      </div>
    </header>
  )
}

export default Header
