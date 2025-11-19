import { useState, useEffect } from 'react'
import reservaService from '../../services/reservaService'
import Table from '../../components/common/Table'
import Button from '../../components/common/Button'
import Modal from '../../components/common/Modal'
import ReservaForm from './ReservaForm'
import './Reservas.css'

const Reservas = () => {
  const [reservas, setReservas] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [selectedReserva, setSelectedReserva] = useState(null)

  // Estados para los filtros
  const [filters, setFilters] = useState({
    estado_id: '',
    fecha_desde: '',
    fecha_hasta: ''
  })

  useEffect(() => {
    loadReservas()
  }, [])

  const loadReservas = async (appliedFilters = {}) => {
    try {
      setLoading(true)
      const data = await reservaService.getAll(appliedFilters)
      setReservas(data)
      setError(null)
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Error al cargar las reservas'
      setError(`Error al cargar las reservas: ${errorMsg}`)
      console.error('Error completo:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (e) => {
    const { name, value } = e.target
    setFilters(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleApplyFilters = () => {
    const appliedFilters = {}
    if (filters.estado_id) appliedFilters.estado_id = filters.estado_id
    if (filters.fecha_desde) appliedFilters.fecha_desde = filters.fecha_desde
    if (filters.fecha_hasta) appliedFilters.fecha_hasta = filters.fecha_hasta

    loadReservas(appliedFilters)
  }

  const handleClearFilters = () => {
    setFilters({
      estado_id: '',
      fecha_desde: '',
      fecha_hasta: ''
    })
    loadReservas()
  }

  const handleCreate = () => {
    setSelectedReserva(null)
    setShowModal(true)
  }

  const handleEdit = (reserva) => {
    setSelectedReserva(reserva)
    setShowModal(true)
  }

  const handleDelete = async (reserva) => {
    if (window.confirm(`¿Está seguro de eliminar la reserva #${reserva.id_reserva}?`)) {
      try {
        await reservaService.delete(reserva.id_reserva)
        loadReservas()
      } catch (err) {
        alert('Error al eliminar la reserva')
        console.error(err)
      }
    }
  }

  const handleSave = async (reservaData) => {
    try {
      if (selectedReserva) {
        await reservaService.update(selectedReserva.id_reserva, reservaData)
      } else {
        await reservaService.create(reservaData)
      }
      setShowModal(false)
      loadReservas()
    } catch (err) {
      throw err
    }
  }

  const getEstadoBadge = (estadoId) => {
    const estados = {
      1: { label: 'Pendiente', class: 'badge-warning' },
      2: { label: 'Confirmada', class: 'badge-info' },
      3: { label: 'Cancelada', class: 'badge-danger' },
      4: { label: 'Completada', class: 'badge-success' }
    }
    const estado = estados[estadoId] || { label: 'Desconocido', class: 'badge-secondary' }
    return <span className={`badge ${estado.class}`}>{estado.label}</span>
  }

  const columns = [
    { header: 'ID', accessor: 'id_reserva' },
    { header: 'Cliente', accessor: 'cliente_nombre_completo' },
    { header: 'Vehículo', accessor: 'vehiculo_descripcion' },
    { header: 'Fecha Reserva', accessor: 'fecha_reserva' },
    { header: 'Fecha Alquiler', accessor: 'fecha_alquiler' },
    {
      header: 'Seña',
      render: (row) => `$${row.senia_monto || 0}`
    },
    {
      header: 'Estado',
      render: (row) => getEstadoBadge(row.estado_reserva_id)
    },
  ]

  if (loading) {
    return <div className="loading">Cargando reservas...</div>
  }

  return (
    <div className="reservas-page">
      <div className="page-header">
        <h1 className="page-title">Gestión de Reservas</h1>
        <Button onClick={handleCreate}>
          + Nueva Reserva
        </Button>
      </div>

      {error && <div className="error">{error}</div>}

      {/* Filtros */}
      <div className="filters-section">
        <h3>Filtros</h3>
        <div className="filters-container">
          <div className="filter-group">
            <label htmlFor="estado_id">Estado:</label>
            <select
              id="estado_id"
              name="estado_id"
              value={filters.estado_id}
              onChange={handleFilterChange}
              className="filter-select"
            >
              <option value="">Todos los estados</option>
              <option value="1">Pendiente</option>
              <option value="2">Confirmada</option>
              <option value="3">Cancelada</option>
              <option value="4">Completada</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="fecha_desde">Fecha desde:</label>
            <input
              type="date"
              id="fecha_desde"
              name="fecha_desde"
              value={filters.fecha_desde}
              onChange={handleFilterChange}
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="fecha_hasta">Fecha hasta:</label>
            <input
              type="date"
              id="fecha_hasta"
              name="fecha_hasta"
              value={filters.fecha_hasta}
              onChange={handleFilterChange}
              className="filter-input"
            />
          </div>

          <div className="filter-actions">
            <Button onClick={handleApplyFilters} variant="primary">
              Aplicar Filtros
            </Button>
            <Button onClick={handleClearFilters} variant="secondary">
              Limpiar
            </Button>
          </div>
        </div>
      </div>

      <Table
        columns={columns}
        data={reservas}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={selectedReserva ? 'Editar Reserva' : 'Nueva Reserva'}
        size="large"
      >
        <ReservaForm
          reserva={selectedReserva}
          onSave={handleSave}
          onCancel={() => setShowModal(false)}
        />
      </Modal>
    </div>
  )
}

export default Reservas
