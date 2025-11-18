import { useState, useEffect } from 'react'
import Modal from './Modal'
import Button from './Button'
import './ClienteDeshabilitadoModal.css'

const ClienteDeshabilitadoModal = ({ isOpen, onClose, onClienteChange, clientes, clienteActual }) => {
  const [selectedCliente, setSelectedCliente] = useState('')
  const [clientesHabilitados, setClientesHabilitados] = useState([])

  useEffect(() => {
    if (clientes) {
      // Filtrar solo clientes habilitados
      const habilitados = clientes.filter(c => c.habilitado)
      setClientesHabilitados(habilitados)
    }
  }, [clientes])

  const handleConfirm = () => {
    if (selectedCliente) {
      onClienteChange(selectedCliente)
      setSelectedCliente('')
      onClose()
    }
  }

  const handleCancel = () => {
    setSelectedCliente('')
    onClose()
  }

  const clienteNombre = clienteActual
    ? clientes?.find(c => c.id_cliente === parseInt(clienteActual))
    : null

  return (
    <Modal isOpen={isOpen} onClose={handleCancel} title="Cliente No Habilitado" size="medium">
      <div className="cliente-deshabilitado-content">
        <div className="warning-icon">⚠️</div>
        <div className="warning-message">
          <p className="message-title">El cliente seleccionado no está habilitado</p>
          {clienteNombre && (
            <p className="cliente-info">
              <strong>{clienteNombre.nombre} {clienteNombre.apellido}</strong>
              {clienteNombre.dni && ` (DNI: ${clienteNombre.dni})`}
            </p>
          )}
          <p className="message-description">
            Este cliente no puede realizar alquileres ni reservas en este momento.
            Por favor, seleccione un cliente habilitado para continuar.
          </p>
        </div>

        <div className="cliente-selector">
          <label htmlFor="nuevo-cliente" className="selector-label">
            Seleccione un cliente habilitado:
          </label>
          <select
            id="nuevo-cliente"
            value={selectedCliente}
            onChange={(e) => setSelectedCliente(e.target.value)}
            className="selector-field"
          >
            <option value="">-- Seleccione un cliente --</option>
            {clientesHabilitados.map(cliente => (
              <option key={cliente.id_cliente} value={cliente.id_cliente}>
                {cliente.nombre} {cliente.apellido} - DNI: {cliente.dni}
              </option>
            ))}
          </select>
          {clientesHabilitados.length === 0 && (
            <p className="no-clientes-warning">
              No hay clientes habilitados disponibles
            </p>
          )}
        </div>

        <div className="modal-actions">
          <Button variant="outline" onClick={handleCancel}>
            Cancelar
          </Button>
          <Button
            onClick={handleConfirm}
            disabled={!selectedCliente}
          >
            Continuar con cliente seleccionado
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default ClienteDeshabilitadoModal
