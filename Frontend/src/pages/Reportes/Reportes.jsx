import { useState, useEffect } from 'react'
import reporteService from '../../services/reporteService'
import './Reportes.css'

const Reportes = () => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [estadisticas, setEstadisticas] = useState(null)
  const [vehiculosMasAlquilados, setVehiculosMasAlquilados] = useState([])
  const [clientesTop, setClientesTop] = useState([])
  const [ingresosMensuales, setIngresosMensuales] = useState([])
  const [mantenimientosProximos, setMantenimientosProximos] = useState([])
  const [anioSeleccionado, setAnioSeleccionado] = useState('2024')

  useEffect(() => {
    loadReportes()
  }, [anioSeleccionado])

  const loadReportes = async () => {
    try {
      setLoading(true)

      // Cargar todas las estadísticas en paralelo
      const [stats, vehiculos, clientes, ingresos, mantenimientos] = await Promise.all([
        reporteService.getEstadisticasGenerales(),
        reporteService.getVehiculosMasAlquilados(),
        reporteService.getClientesTop(),
        reporteService.getIngresosMensuales(anioSeleccionado),
        reporteService.getMantenimientosProximos(),
      ])

      setEstadisticas(stats)
      setVehiculosMasAlquilados(vehiculos)
      setClientesTop(clientes)
      setIngresosMensuales(ingresos)
      setMantenimientosProximos(mantenimientos)
      setError(null)
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Error al cargar los reportes'
      setError(`Error al cargar los reportes: ${errorMsg}`)
      console.error('Error completo:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Cargando reportes...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  return (
    <div className="reportes-page">
      <h1 className="page-title">Reportes y Estadísticas</h1>

      {/* Estadísticas Generales */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon vehicles">🚗</div>
          <div className="stat-content">
            <h3 className="stat-value">{estadisticas?.total_vehiculos || 0}</h3>
            <p className="stat-label">Vehículos Activos</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon clients">👥</div>
          <div className="stat-content">
            <h3 className="stat-value">{estadisticas?.total_clientes || 0}</h3>
            <p className="stat-label">Clientes Registrados</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon rentals">📋</div>
          <div className="stat-content">
            <h3 className="stat-value">{estadisticas?.alquileres_activos || 0}</h3>
            <p className="stat-label">Alquileres Activos</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon reservations">📅</div>
          <div className="stat-content">
            <h3 className="stat-value">{estadisticas?.reservas_pendientes || 0}</h3>
            <p className="stat-label">Reservas Pendientes</p>
          </div>
        </div>

        <div className="stat-card highlight">
          <div className="stat-icon revenue">💰</div>
          <div className="stat-content">
            <h3 className="stat-value">${estadisticas?.ingresos_mes_actual?.toFixed(2) || 0}</h3>
            <p className="stat-label">Ingresos del Mes</p>
          </div>
        </div>
      </div>

      {/* Reportes en dos columnas */}
      <div className="reports-container">
        {/* Vehículos Más Alquilados */}
        <div className="report-card">
          <h2 className="report-title">Vehículos Más Alquilados</h2>
          <div className="report-content">
            {vehiculosMasAlquilados.length > 0 ? (
              <table className="report-table">
                <thead>
                  <tr>
                    <th>Vehículo</th>
                    <th>Alquileres</th>
                    <th>Días Totales</th>
                  </tr>
                </thead>
                <tbody>
                  {vehiculosMasAlquilados.map((vehiculo, index) => (
                    <tr key={vehiculo.id_vehiculo}>
                      <td>
                        <div className="vehicle-info">
                          <span className="rank">#{index + 1}</span>
                          <span>{vehiculo.marca} {vehiculo.modelo}</span>
                          <small>{vehiculo.patente}</small>
                        </div>
                      </td>
                      <td className="text-center">{vehiculo.cantidad_alquileres}</td>
                      <td className="text-center">{vehiculo.dias_alquilados}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="no-data">No hay datos disponibles</p>
            )}
          </div>
        </div>

        {/* Mejores Clientes */}
        <div className="report-card">
          <h2 className="report-title">Mejores Clientes</h2>
          <div className="report-content">
            {clientesTop.length > 0 ? (
              <table className="report-table">
                <thead>
                  <tr>
                    <th>Cliente</th>
                    <th>Alquileres</th>
                    <th>Días Totales</th>
                  </tr>
                </thead>
                <tbody>
                  {clientesTop.map((cliente, index) => (
                    <tr key={cliente.id_cliente}>
                      <td>
                        <div className="client-info">
                          <span className="rank">#{index + 1}</span>
                          <span>{cliente.nombre} {cliente.apellido}</span>
                          <small>{cliente.email}</small>
                        </div>
                      </td>
                      <td className="text-center">{cliente.cantidad_alquileres}</td>
                      <td className="text-center">{cliente.dias_totales}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="no-data">No hay datos disponibles</p>
            )}
          </div>
        </div>

        {/* Ingresos Mensuales */}
        <div className="report-card full-width">
          <div className="report-header">
            <h2 className="report-title">Ingresos Mensuales</h2>
            <select
              value={anioSeleccionado}
              onChange={(e) => setAnioSeleccionado(e.target.value)}
              className="year-select"
            >
              <option value="2023">2023</option>
              <option value="2024">2024</option>
              <option value="2025">2025</option>
            </select>
          </div>
          <div className="report-content">
            {ingresosMensuales.length > 0 ? (
              <div>
                <div className="chart-simple">
                  {ingresosMensuales.map((mes) => (
                    <div key={mes.mes} className="chart-bar-container">
                      <div className="chart-bar-label">{mes.mes_nombre}</div>
                      <div className="chart-bar-wrapper">
                        <div
                          className="chart-bar"
                          style={{
                            width: `${(mes.total_ingresos / Math.max(...ingresosMensuales.map(m => m.total_ingresos))) * 100}%`
                          }}
                        >
                          <span className="chart-bar-value">${mes.total_ingresos.toFixed(2)}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="total-summary">
                  <strong>Total Anual: </strong>
                  ${ingresosMensuales.reduce((sum, mes) => sum + mes.total_ingresos, 0).toFixed(2)}
                </div>
              </div>
            ) : (
              <p className="no-data">No hay datos disponibles para el año {anioSeleccionado}</p>
            )}
          </div>
        </div>

        {/* Mantenimientos Próximos */}
        <div className="report-card full-width">
          <h2 className="report-title">Mantenimientos Próximos</h2>
          <div className="report-content">
            {mantenimientosProximos.length > 0 ? (
              <table className="report-table">
                <thead>
                  <tr>
                    <th>Vehículo</th>
                    <th>Fecha Programada</th>
                    <th>KM Mantenimiento</th>
                    <th>KM Actual</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {mantenimientosProximos.map((mant) => (
                    <tr key={mant.id_mantenimiento}>
                      <td>
                        <div>{mant.marca} {mant.modelo}</div>
                        <small>{mant.patente}</small>
                      </td>
                      <td>{mant.fecha_programada}</td>
                      <td className="text-center">{mant.km.toLocaleString()}</td>
                      <td className="text-center">{mant.km_actual.toLocaleString()}</td>
                      <td>
                        <span className={`badge badge-${mant.estado_mantenimiento === 'PROGRAMADO' ? 'warning' : 'info'}`}>
                          {mant.estado_mantenimiento}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="no-data">No hay mantenimientos programados</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Reportes
