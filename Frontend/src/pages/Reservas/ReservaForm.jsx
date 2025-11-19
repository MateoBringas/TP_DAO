import { useState, useEffect } from 'react'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'
import ClienteDeshabilitadoModal from '../../components/common/ClienteDeshabilitadoModal'
import clienteService from '../../services/clienteService'
import vehiculoService from '../../services/vehiculoService'

const ReservaForm = ({ reserva, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    cliente_id: '',
    vehiculo_id: '',
    empleado_id: 1,
    estado_reserva_id: 1,
    fecha_reserva: '',
    fecha_alquiler: '',
    senia_monto: '',
  })

  const [clientes, setClientes] = useState([])
  const [vehiculos, setVehiculos] = useState([])
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [showClienteModal, setShowClienteModal] = useState(false)
  const [clienteDeshabilitadoId, setClienteDeshabilitadoId] = useState(null)

  useEffect(() => {
    loadClientes()
    loadVehiculos()

    if (reserva) {
      setFormData({
        cliente_id: reserva.cliente_id || '',
        vehiculo_id: reserva.vehiculo_id || '',
        empleado_id: reserva.empleado_id || 1,
        estado_reserva_id: reserva.estado_reserva_id || 1,
        fecha_reserva: reserva.fecha_reserva || '',
        fecha_alquiler: reserva.fecha_alquiler || '',
        senia_monto: reserva.senia_monto || '',
      })
    } else {
      // Establecer la fecha de reserva como hoy por defecto
      const today = new Date().toISOString().split('T')[0]
      setFormData(prev => ({ ...prev, fecha_reserva: today }))
    }
  }, [reserva])

  const loadClientes = async () => {
    try {
      const data = await clienteService.getAll()
      setClientes(data)
    } catch (err) {
      console.error('Error al cargar clientes:', err)
    }
  }

  const loadVehiculos = async () => {
    try {
      const data = await vehiculoService.getAll()
      setVehiculos(data.filter(v => v.habilitado))
    } catch (err) {
      console.error('Error al cargar vehículos:', err)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))

     // Si cambian las fechas, recargar vehículos disponibles
    if (name === 'fecha_reserva' || name === 'fecha_alquiler') {
      const newFechaReserva = name === 'fecha_reserva' ? value : formData.fecha_reserva
      const newFechaAlquiler = name === 'fecha_alquiler' ? value : formData.fecha_alquiler

      if (newFechaReserva && newFechaAlquiler) {
        loadVehiculosDisponibles(newFechaReserva, newFechaAlquiler)
      }
    }

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const loadVehiculosDisponibles = async (fecha_reserva, fecha_alquiler) => {
    try {
      const response = await fetch(
        `http://localhost:5000/vehiculos/disponibles?fecha_inicio=${fecha_reserva}&fecha_prevista=${fecha_alquiler}`
      )
      const data = await response.json()
      setVehiculos(data)
    } catch (err) {
      console.error('Error al cargar vehículos disponibles:', err)
    }
  }

  const validate = () => {
    const newErrors = {}

    if (!formData.cliente_id) newErrors.cliente_id = 'Seleccione un cliente'
    if (!formData.vehiculo_id) newErrors.vehiculo_id = 'Seleccione un vehículo'
    if (!formData.fecha_reserva) newErrors.fecha_reserva = 'La fecha de reserva es requerida'
    if (!formData.fecha_alquiler) newErrors.fecha_alquiler = 'La fecha de alquiler es requerida'

    if (formData.fecha_reserva && formData.fecha_alquiler) {
      if (new Date(formData.fecha_alquiler) < new Date(formData.fecha_reserva)) {
        newErrors.fecha_alquiler = 'La fecha de alquiler debe ser posterior a la de reserva'
      }
    }

    if (formData.senia_monto && parseFloat(formData.senia_monto) < 0) {
      newErrors.senia_monto = 'El monto de la seña no puede ser negativo'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validate()) return

    setSubmitting(true)
    try {
      const dataToSend = {
        ...formData,
        cliente_id: parseInt(formData.cliente_id),
        vehiculo_id: parseInt(formData.vehiculo_id),
        empleado_id: parseInt(formData.empleado_id),
        estado_reserva_id: parseInt(formData.estado_reserva_id),
        senia_monto: formData.senia_monto ? parseFloat(formData.senia_monto) : 0,
      }

      await onSave(dataToSend)
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message

      // Detectar si el error es por cliente deshabilitado
      if (errorMessage.includes('no está habilitado')) {
        setClienteDeshabilitadoId(formData.cliente_id)
        setShowClienteModal(true)
      } else {
        alert('Error al guardar la reserva: ' + errorMessage)
      }
    } finally {
      setSubmitting(false)
    }
  }

  const handleClienteChange = (nuevoClienteId) => {
    setFormData(prev => ({
      ...prev,
      cliente_id: nuevoClienteId
    }))
    setClienteDeshabilitadoId(null)
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-grid">
        <div className="input-group">
          <label htmlFor="cliente_id" className="input-label">
            Cliente<span className="required">*</span>
          </label>
          <select
            id="cliente_id"
            name="cliente_id"
            value={formData.cliente_id}
            onChange={handleChange}
            className={`input-field ${errors.cliente_id ? 'input-error' : ''}`}
            required
          >
            <option value="">Seleccione un cliente</option>
            {clientes.map(cliente => (
              <option key={cliente.id_cliente} value={cliente.id_cliente}>
                {cliente.nombre} {cliente.apellido} - DNI: {cliente.dni}
              </option>
            ))}
          </select>
          {errors.cliente_id && <span className="error-message">{errors.cliente_id}</span>}
        </div>

        <div className="input-group">
          <label htmlFor="vehiculo_id" className="input-label">
            Vehículo<span className="required">*</span>
          </label>
          <select
            id="vehiculo_id"
            name="vehiculo_id"
            value={formData.vehiculo_id}
            onChange={handleChange}
            className={`input-field ${errors.vehiculo_id ? 'input-error' : ''}`}
            required
            disabled={formData.fecha_reserva && formData.fecha_alquiler ? false : true}
          >
            <option value="">Seleccione un vehículo</option>
            {vehiculos.map(vehiculo => (
              <option key={vehiculo.id_vehiculo} value={vehiculo.id_vehiculo}>
                {vehiculo.marca} {vehiculo.modelo} - {vehiculo.patente} (${vehiculo.tarifa_base_dia}/día)
              </option>
            ))}
          </select>
          {errors.vehiculo_id && <span className="error-message">{errors.vehiculo_id}</span>}
        </div>

        <Input
          label="Fecha de Reserva"
          name="fecha_reserva"
          type="date"
          value={formData.fecha_reserva}
          onChange={handleChange}
          error={errors.fecha_reserva}
          required
        />

        <Input
          label="Fecha de Alquiler Prevista"
          name="fecha_alquiler"
          type="date"
          value={formData.fecha_alquiler}
          onChange={handleChange}
          error={errors.fecha_alquiler}
          min={formData.fecha_reserva || undefined}
          required
        />

        <Input
          label="Monto de Seña"
          name="senia_monto"
          type="number"
          step="0.01"
          value={formData.senia_monto}
          onChange={handleChange}
          error={errors.senia_monto}
          placeholder="0.00"
        />

        <div className="input-group">
          <label htmlFor="estado_reserva_id" className="input-label">
            Estado
          </label>
          <select
            id="estado_reserva_id"
            name="estado_reserva_id"
            value={formData.estado_reserva_id}
            onChange={handleChange}
            className="input-field"
          >
            <option value="1">Pendiente</option>
            <option value="2">Confirmada</option>
            <option value="3">Cancelada</option>
            <option value="4">Completada</option>
          </select>
        </div>
      </div>

      <div className="form-actions">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
        <Button type="submit" disabled={submitting}>
          {submitting ? 'Guardando...' : 'Guardar'}
        </Button>
      </div>

      <ClienteDeshabilitadoModal
        isOpen={showClienteModal}
        onClose={() => setShowClienteModal(false)}
        onClienteChange={handleClienteChange}
        clientes={clientes}
        clienteActual={clienteDeshabilitadoId}
      />
    </form>
  )
}

export default ReservaForm
