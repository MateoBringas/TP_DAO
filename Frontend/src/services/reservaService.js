import api from './api'

const reservaService = {
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
    const url = queryString ? `/reservas/?${queryString}` : '/reservas/'

    const response = await api.get(url)
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/reservas/${id}`)
    return response.data
  },

  create: async (reserva) => {
    const response = await api.post('/reservas/', reserva)
    return response.data
  },

  update: async (id, reserva) => {
    const response = await api.put(`/reservas/${id}`, reserva)
    return response.data
  },

  delete: async (id) => {
    const response = await api.delete(`/reservas/${id}`)
    return response.data
  },

  // Confirmar reserva
  confirmar: async (id) => {
    const response = await api.post(`/reservas/${id}/confirmar`)
    return response.data
  },

  // Cancelar reserva
  cancelar: async (id) => {
    const response = await api.post(`/reservas/${id}/cancelar`)
    return response.data
  },
}

export default reservaService
