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

  useEffect(() => {
    loadAlquileres()
  }, [])

  const loadAlquileres = async () => {
    try {
      setLoading(true)
      const data = await alquilerService.getAll()
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
