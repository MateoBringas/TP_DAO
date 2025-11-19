import { useState, useEffect } from 'react'
import alquilerService from '../../services/alquilerService'
import Table from '../../components/common/Table'
import Button from '../../components/common/Button'
import Modal from '../../components/common/Modal'
import AlquilerForm from './AlquilerForm'
import './Alquileres.css'

const Alquileres = () => {
  const [alquileres, setAlquileres] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [selectedAlquiler, setSelectedAlquiler] = useState(null)

  // Estados para los filtros
  const [filters, setFilters] = useState({
    estado_id: '',
    fecha_desde: '',
    fecha_hasta: ''
  })

  useEffect(() => {
    loadAlquileres()
  }, [])

  const loadAlquileres = async (appliedFilters = {}) => {
    try {
      setLoading(true)
      const data = await alquilerService.getAll(appliedFilters)
      setAlquileres(data)
      setError(null)
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Error al cargar los alquileres'
      setError(`Error al cargar los alquileres: ${errorMsg}`)
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

    loadAlquileres(appliedFilters)
  }

  const handleClearFilters = () => {
    setFilters({
      estado_id: '',
      fecha_desde: '',
      fecha_hasta: ''
    })
    loadAlquileres()
  }

  const handleCreate = () => {
    setSelectedAlquiler(null)
    setShowModal(true)
  }

  const handleEdit = (alquiler) => {
    setSelectedAlquiler(alquiler)
    setShowModal(true)
  }

  const handleDelete = async (alquiler) => {
    if (window.confirm(`¿Está seguro de eliminar el alquiler #${alquiler.id_alquiler}?`)) {
      try {
        await alquilerService.delete(alquiler.id_alquiler)
        loadAlquileres()
      } catch (err) {
        alert('Error al eliminar el alquiler')
        console.error(err)
      }
    }
  }

  const handleSave = async (alquilerData) => {
    try {
      if (selectedAlquiler) {
        await alquilerService.update(selectedAlquiler.id_alquiler, alquilerData)
      } else {
        await alquilerService.create(alquilerData)
      }
      setShowModal(false)
      loadAlquileres()
    } catch (err) {
      throw err
    }
  }

  const columns = [
    { header: 'ID', accessor: 'id_alquiler' },
    { header: 'Cliente', accessor: 'cliente_nombre_completo' },
    { header: 'Vehículo', accessor: 'vehiculo_descripcion' },
    { header: 'Fecha Inicio', accessor: 'fecha_inicio' },
    { header: 'Fecha Prevista', accessor: 'fecha_prevista' },
    { header: 'Fecha Entrega', render: (row) => row.fecha_entrega || 'Pendiente' },
    { header: 'KM Salida', accessor: 'km_salida' },
    { header: 'KM Entrada', render: (row) => row.km_entrada || 'Pendiente' },
  ]

  if (loading) {
    return <div className="loading">Cargando alquileres...</div>
  }

  return (
    <div className="alquileres-page">
      <div className="page-header">
        <h1 className="page-title">Gestión de Alquileres</h1>
        <Button onClick={handleCreate}>
          + Nuevo Alquiler
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
              <option value="2">Activo</option>
              <option value="3">Finalizado</option>
              <option value="4">Cancelado</option>
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
        data={alquileres}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={selectedAlquiler ? 'Editar Alquiler' : 'Nuevo Alquiler'}
        size="large"
      >
        <AlquilerForm
          alquiler={selectedAlquiler}
          onSave={handleSave}
          onCancel={() => setShowModal(false)}
        />
      </Modal>
    </div>
  )
}

export default Alquileres
