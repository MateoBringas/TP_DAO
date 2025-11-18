import { useState, useEffect } from 'react'
import reporteService from '../../services/reporteService'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
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

  const COLORS = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140']

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="label">{payload[0].payload.label || payload[0].name}</p>
          <p className="value" style={{ color: payload[0].color }}>
            {payload[0].name}: {payload[0].value}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="reportes-page">
      <div className="page-header">
        <h1 className="page-title">Reportes y Estadísticas</h1>
      </div>

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
        {/* Vehículos Más Alquilados - Gráfico */}
        <div className="report-card">
          <h2 className="report-title">Top 5 Vehículos Más Alquilados</h2>
          <div className="report-content">
            {vehiculosMasAlquilados.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={vehiculosMasAlquilados.slice(0, 5).map(v => ({
                  nombre: `${v.marca} ${v.modelo}`,
                  alquileres: v.cantidad_alquileres,
                  dias: v.dias_alquilados
                }))}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="nombre" tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Bar dataKey="alquileres" fill="#667eea" name="Alquileres" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="dias" fill="#4facfe" name="Días Totales" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="no-data">No hay datos disponibles</p>
            )}
          </div>
        </div>

        {/* Mejores Clientes - Gráfico Circular */}
        <div className="report-card">
          <h2 className="report-title">Top 5 Mejores Clientes</h2>
          <div className="report-content">
            {clientesTop.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={clientesTop.slice(0, 5).map((c, i) => ({
                      name: `${c.nombre} ${c.apellido}`,
                      value: c.cantidad_alquileres,
                      label: `${c.nombre} ${c.apellido}`
                    }))}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {clientesTop.slice(0, 5).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="no-data">No hay datos disponibles</p>
            )}
          </div>
        </div>

        {/* Ingresos Mensuales - Gráfico de Líneas */}
        <div className="report-card full-width">
          <div className="report-header">
            <h2 className="report-title">Evolución de Ingresos Mensuales</h2>
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
                <ResponsiveContainer width="100%" height={350}>
                  <LineChart data={ingresosMensuales.map(m => ({
                    mes: m.mes_nombre,
                    ingresos: m.total_ingresos,
                    cantidad: m.cantidad_pagos
                  }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="mes" tick={{ fontSize: 12 }} />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line
                      yAxisId="left"
                      type="monotone"
                      dataKey="ingresos"
                      stroke="#667eea"
                      strokeWidth={3}
                      name="Ingresos ($)"
                      dot={{ r: 5 }}
                      activeDot={{ r: 8 }}
                    />
                    <Line
                      yAxisId="right"
                      type="monotone"
                      dataKey="cantidad"
                      stroke="#f093fb"
                      strokeWidth={2}
                      name="Cantidad de Pagos"
                      strokeDasharray="5 5"
                    />
                  </LineChart>
                </ResponsiveContainer>
                <div className="total-summary">
                  <strong>Total Anual: </strong>
                  <span className="highlight-value">
                    ${ingresosMensuales.reduce((sum, mes) => sum + mes.total_ingresos, 0).toFixed(2)}
                  </span>
                  <span className="separator">|</span>
                  <strong>Promedio Mensual: </strong>
                  <span className="highlight-value">
                    ${(ingresosMensuales.reduce((sum, mes) => sum + mes.total_ingresos, 0) / ingresosMensuales.length).toFixed(2)}
                  </span>
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
