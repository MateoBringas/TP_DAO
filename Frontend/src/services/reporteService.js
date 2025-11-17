import api from './api'

const reporteService = {
  // Reporte de vehículos más alquilados
  getVehiculosMasAlquilados: async () => {
    const response = await api.get('/reportes/vehiculos-mas-alquilados')
    return response.data
  },

  // Reporte de ingresos mensuales
  getIngresosMensuales: async (anio = '2024') => {
    const response = await api.get('/reportes/ingresos-mensuales', {
      params: { anio }
    })
    return response.data
  },

  // Reporte de mejores clientes
  getClientesTop: async () => {
    const response = await api.get('/reportes/clientes-top')
    return response.data
  },

  // Reporte de mantenimientos próximos
  getMantenimientosProximos: async () => {
    const response = await api.get('/reportes/mantenimientos-proximos')
    return response.data
  },

  // Estadísticas generales
  getEstadisticasGenerales: async () => {
    const response = await api.get('/reportes/estadisticas-generales')
    return response.data
  },
}

export default reporteService
