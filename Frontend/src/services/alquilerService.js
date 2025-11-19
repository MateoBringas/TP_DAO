import api from './api'

const alquilerService = {
  getAll: async (filters = {}) => {
    const params = new URLSearchParams()

    if (filters.estado_id) {
      params.append('estado_id', filters.estado_id)
    }
    if (filters.fecha_desde) {
      params.append('fecha_desde', filters.fecha_desde)
    }
    if (filters.fecha_hasta) {
      params.append('fecha_hasta', filters.fecha_hasta)
    }

    const queryString = params.toString()
    const url = queryString ? `/alquileres/?${queryString}` : '/alquileres/'

    const response = await api.get(url)
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
