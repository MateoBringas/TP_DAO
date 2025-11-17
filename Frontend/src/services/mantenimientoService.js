import api from './api'

const mantenimientoService = {
  getAll: async () => {
    const response = await api.get('/mantenimientos/')
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/mantenimientos/${id}`)
    return response.data
  },

  create: async (mantenimiento) => {
    const response = await api.post('/mantenimientos/', mantenimiento)
    return response.data
  },

  update: async (id, mantenimiento) => {
    const response = await api.put(`/mantenimientos/${id}`, mantenimiento)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/mantenimientos/${id}`)
    return response.data
  },

  // Obtener mantenimientos por vehículo
  getByVehiculo: async (vehiculoId) => {
    const response = await api.get(`/mantenimientos/vehiculo/${vehiculoId}`)
    return response.data
  },
}

export default mantenimientoService
