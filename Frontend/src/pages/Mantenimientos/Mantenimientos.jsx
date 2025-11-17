import { useState, useEffect } from 'react'
import mantenimientoService from '../../services/mantenimientoService'
import Table from '../../components/common/Table'
import Button from '../../components/common/Button'
import Modal from '../../components/common/Modal'
import MantenimientoForm from './MantenimientoForm'
import './Mantenimientos.css'

const Mantenimientos = () => {
  const [mantenimientos, setMantenimientos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [selectedMantenimiento, setSelectedMantenimiento] = useState(null)

  useEffect(() => {
    loadMantenimientos()
  }, [])

  const loadMantenimientos = async () => {
    try {
      setLoading(true)
      const data = await mantenimientoService.getAll()
      setMantenimientos(data)
      setError(null)
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Error al cargar los mantenimientos'
      setError(`Error al cargar los mantenimientos: ${errorMsg}`)
      console.error('Error completo:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setSelectedMantenimiento(null)
    setShowModal(true)
  }

  const handleEdit = (mantenimiento) => {
    setSelectedMantenimiento(mantenimiento)
    setShowModal(true)
  }

  const handleDelete = async (mantenimiento) => {
    if (window.confirm(`¿Está seguro de eliminar el mantenimiento #${mantenimiento.id_mantenimiento}?`)) {
      try {
        await mantenimientoService.delete(mantenimiento.id_mantenimiento)
        loadMantenimientos()
      } catch (err) {
        alert('Error al eliminar el mantenimiento')
        console.error(err)
      }
    }
  }

  const handleSave = async (mantenimientoData) => {
    try {
      if (selectedMantenimiento) {
        await mantenimientoService.update(selectedMantenimiento.id_mantenimiento, mantenimientoData)
      } else {
        await mantenimientoService.create(mantenimientoData)
      }
      setShowModal(false)
      loadMantenimientos()
    } catch (err) {
      throw err
    }
  }

  const getEstadoBadge = (estado) => {
    const estados = {
      'PROGRAMADO': { label: 'Programado', class: 'badge-warning' },
      'EN_CURSO': { label: 'En Curso', class: 'badge-info' },
      'COMPLETADO': { label: 'Completado', class: 'badge-success' },
      'CANCELADO': { label: 'Cancelado', class: 'badge-danger' }
    }
    const estadoInfo = estados[estado] || { label: estado, class: 'badge-secondary' }
    return <span className={`badge ${estadoInfo.class}`}>{estadoInfo.label}</span>
  }

  const columns = [
    { header: 'ID', accessor: 'id_mantenimiento' },
    { header: 'Vehículo ID', accessor: 'vehiculo_id' },
    { header: 'Fecha Programada', accessor: 'fecha_programada' },
    {
      header: 'Fecha Realizada',
      render: (row) => row.fecha_realizada || 'Pendiente'
    },
    { header: 'KM', accessor: 'km' },
    {
      header: 'Costo',
      render: (row) => `$${row.costo || 0}`
    },
    {
      header: 'Estado',
      render: (row) => getEstadoBadge(row.estado_mantenimiento)
    },
  ]

  if (loading) {
    return <div className="loading">Cargando mantenimientos...</div>
  }

  return (
    <div className="mantenimientos-page">
      <div className="page-header">
        <h1 className="page-title">Gestión de Mantenimientos</h1>
        <Button onClick={handleCreate}>
          + Nuevo Mantenimiento
        </Button>
      </div>

      {error && <div className="error">{error}</div>}

      <Table
        columns={columns}
        data={mantenimientos}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={selectedMantenimiento ? 'Editar Mantenimiento' : 'Nuevo Mantenimiento'}
        size="large"
      >
        <MantenimientoForm
          mantenimiento={selectedMantenimiento}
          onSave={handleSave}
          onCancel={() => setShowModal(false)}
        />
      </Modal>
    </div>
  )
}

export default Mantenimientos
