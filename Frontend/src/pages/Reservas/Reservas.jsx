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

  useEffect(() => {
    loadReservas()
  }, [])

  const loadReservas = async () => {
    try {
      setLoading(true)
      const data = await reservaService.getAll()
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
