import api from './api'

const alquilerService = {
  getAll: async () => {
    const response = await api.get('/alquileres/')
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/alquileres/${id}`)
    return response.data
  },

  create: async (alquiler) => {
    const response = await api.post('/alquileres/', alquiler)
    return response.data
  },

  update: async (id, alquiler) => {
    const response = await api.put(`/alquileres/${id}`, alquiler)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/alquileres/${id}`)
    return response.data
  },

  // Obtener alquileres por cliente
  getByCliente: async (clienteId) => {
    const response = await api.get(`/alquileres/cliente/${clienteId}`)
    return response.data
  },

  // Obtener alquileres activos
  getActivos: async () => {
    const response = await api.get('/alquileres/activos')
    return response.data
  },
}

export default alquilerService
