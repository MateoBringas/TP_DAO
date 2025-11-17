import api from './api'

const vehiculoService = {
  // Obtener todos los vehículos
  getAll: async () => {
    const response = await api.get('/vehiculos/')
    return response.data
  },

  // Obtener un vehículo por ID
  getById: async (id) => {
    const response = await api.get(`/vehiculos/${id}`)
    return response.data
  },

  // Crear un nuevo vehículo
  create: async (vehiculo) => {
    const response = await api.post('/vehiculos/', vehiculo)
    return response.data
  },

  // Actualizar un vehículo
  update: async (id, vehiculo) => {
    const response = await api.put(`/vehiculos/${id}`, vehiculo)
    return response.data
  },

  // Eliminar un vehículo
  delete: async (id) => {
    const response = await api.delete(`/vehiculos/${id}`)
    return response.data
  },

  // Obtener vehículos disponibles
  getDisponibles: async () => {
    const response = await api.get('/vehiculos/disponibles')
    return response.data
  },
}

export default vehiculoService
