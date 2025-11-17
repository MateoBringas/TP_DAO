import { useState, useEffect } from 'react'
import clienteService from '../../services/clienteService'
import Table from '../../components/common/Table'
import Button from '../../components/common/Button'
import Modal from '../../components/common/Modal'
import ClienteForm from './ClienteForm'
import './Clientes.css'

const Clientes = () => {
  const [clientes, setClientes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [selectedCliente, setSelectedCliente] = useState(null)

  useEffect(() => {
    loadClientes()
  }, [])

  const loadClientes = async () => {
    try {
      setLoading(true)
      const data = await clienteService.getAll()
      setClientes(data)
      setError(null)
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Error al cargar los clientes'
      setError(`Error al cargar los clientes: ${errorMsg}`)
      console.error('Error completo:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setSelectedCliente(null)
    setShowModal(true)
  }

  const handleEdit = (cliente) => {
    setSelectedCliente(cliente)
    setShowModal(true)
  }

  const handleDelete = async (cliente) => {
    if (window.confirm(`¿Está seguro de eliminar al cliente ${cliente.nombre} ${cliente.apellido}?`)) {
      try {
        await clienteService.delete(cliente.id_cliente)
        loadClientes()
      } catch (err) {
        alert('Error al eliminar el cliente')
        console.error(err)
      }
    }
  }

  const handleSave = async (clienteData) => {
    try {
      if (selectedCliente) {
        await clienteService.update(selectedCliente.id_cliente, clienteData)
      } else {
        await clienteService.create(clienteData)
      }
      setShowModal(false)
      loadClientes()
    } catch (err) {
      throw err
    }
  }

  const columns = [
    { header: 'DNI', accessor: 'dni' },
    { header: 'Nombre', accessor: 'nombre' },
    { header: 'Apellido', accessor: 'apellido' },
    { header: 'Email', accessor: 'email' },
    { header: 'Teléfono', accessor: 'telefono' },
    { header: 'Licencia', accessor: 'licencia_num' },
    {
      header: 'Venc. Licencia',
      render: (row) => row.licencia_venc || 'N/A'
    },
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
    return <div className="loading">Cargando clientes...</div>
  }

  return (
    <div className="clientes-page">
      <div className="page-header">
        <h1 className="page-title">Gestión de Clientes</h1>
        <Button onClick={handleCreate}>
          + Nuevo Cliente
        </Button>
      </div>

      {error && <div className="error">{error}</div>}

      <Table
        columns={columns}
        data={clientes}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={selectedCliente ? 'Editar Cliente' : 'Nuevo Cliente'}
        size="large"
      >
        <ClienteForm
          cliente={selectedCliente}
          onSave={handleSave}
          onCancel={() => setShowModal(false)}
        />
      </Modal>
    </div>
  )
}

export default Clientes
