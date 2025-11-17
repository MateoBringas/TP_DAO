import { useState } from 'react'
import Header from './Header'
import Sidebar from './Sidebar'
import './Layout.css'

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  return (
    <div className="layout">
      <Header toggleSidebar={toggleSidebar} />
      <div className="layout-body">
        <Sidebar isOpen={sidebarOpen} />
        <main className={`main-content ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
          <div className="container">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout
