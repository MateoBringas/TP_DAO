import api from './api'

const reporteService = {
  // Reporte de vehículo más alquilado
  getVehiculoMasAlquilado: async () => {
    const response = await api.get('/reportes/vehiculo-mas-alquilado')
    return response.data
  },

  // Reporte de alquileres por período
  getAlquileresPorPeriodo: async (fechaInicio, fechaFin) => {
    const response = await api.get('/reportes/alquileres-por-periodo', {
      params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin }
    })
    return response.data
  },

  // Estadísticas de facturación mensual
  getFacturacionMensual: async (anio) => {
    const response = await api.get('/reportes/facturacion-mensual', {
      params: { anio }
    })
    return response.data
  },

  // Listado de alquileres por cliente
  getListadoPorCliente: async (clienteId) => {
    const response = await api.get(`/reportes/alquileres-cliente/${clienteId}`)
    return response.data
  },
}

export default reporteService
