import { useState, useEffect } from 'react'
import vehiculoService from '../../services/vehiculoService'
import Table from '../../components/common/Table'
import Button from '../../components/common/Button'
import Modal from '../../components/common/Modal'
import VehiculoForm from './VehiculoForm'
import './Vehiculos.css'

const Vehiculos = () => {
  const [vehiculos, setVehiculos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [selectedVehiculo, setSelectedVehiculo] = useState(null)

  useEffect(() => {
    loadVehiculos()
  }, [])

  const loadVehiculos = async () => {
    try {
      setLoading(true)
      const data = await vehiculoService.getAll()
      setVehiculos(data)
      setError(null)
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Error al cargar los vehículos'
      setError(`Error al cargar los vehículos: ${errorMsg}`)
      console.error('Error completo:', err)
      console.error('Error response:', err.response)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setSelectedVehiculo(null)
    setShowModal(true)
  }

  const handleEdit = (vehiculo) => {
    setSelectedVehiculo(vehiculo)
    setShowModal(true)
  }

  const handleDelete = async (vehiculo) => {
    if (window.confirm(`¿Está seguro de eliminar el vehículo ${vehiculo.patente}?`)) {
      try {
        await vehiculoService.delete(vehiculo.id_vehiculo)
        loadVehiculos()
      } catch (err) {
        alert('Error al eliminar el vehículo')
        console.error(err)
      }
    }
  }

  const handleSave = async (vehiculoData) => {
    try {
      if (selectedVehiculo) {
        await vehiculoService.update(selectedVehiculo.id_vehiculo, vehiculoData)
      } else {
        await vehiculoService.create(vehiculoData)
      }
      setShowModal(false)
      loadVehiculos()
    } catch (err) {
      throw err
    }
  }

  const columns = [
    {
      header: 'Foto',
      render: (row) => (
        <div className="vehicle-photo-cell">
          {row.foto_url ? (
            <img
              src={`http://localhost:5000${row.foto_url}`}
              alt={`${row.marca} ${row.modelo}`}
              className="vehicle-thumbnail"
            />
          ) : (
            <div className="no-photo">Sin foto</div>
          )}
        </div>
      )
    },
    { header: 'Patente', accessor: 'patente' },
    { header: 'Marca', accessor: 'marca' },
    { header: 'Modelo', accessor: 'modelo' },
    { header: 'Año', accessor: 'anio' },
    {
      header: 'Tarifa/Día',
      render: (row) => `$${row.tarifa_base_dia}`
    },
    { header: 'KM Actual', accessor: 'km_actual' },
    {
      header: 'Estado',
      render: (row) => (
        <span className={`badge ${row.habilitado ? 'badge-success' : 'badge-danger'}`}>
          {row.habilitado ? 'Habilitado' : 'No habilitado'}
        </span>
      )
    },
  ]

  if (loading) {
    return <div className="loading">Cargando vehículos...</div>
  }

  return (
    <div className="vehiculos-page">
      <div className="page-header">
        <h1 className="page-title">Gestión de Vehículos</h1>
        <Button onClick={handleCreate}>
          + Nuevo Vehículo
        </Button>
      </div>

      {error && <div className="error">{error}</div>}

      <Table
        columns={columns}
        data={vehiculos}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={selectedVehiculo ? 'Editar Vehículo' : 'Nuevo Vehículo'}
        size="large"
      >
        <VehiculoForm
          vehiculo={selectedVehiculo}
          onSave={handleSave}
          onCancel={() => setShowModal(false)}
        />
      </Modal>
    </div>
  )
}

export default Vehiculos
