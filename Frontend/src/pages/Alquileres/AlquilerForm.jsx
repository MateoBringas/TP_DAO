import { useState, useEffect } from 'react'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'
import ClienteDeshabilitadoModal from '../../components/common/ClienteDeshabilitadoModal'
import clienteService from '../../services/clienteService'
import vehiculoService from '../../services/vehiculoService'

const AlquilerForm = ({ alquiler, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    cliente_id: '',
    vehiculo_id: '',
    fecha_inicio: '',
    fecha_prevista: '',
    fecha_entrega: '',
    km_salida: '',
    km_entrada: '',
    observaciones: '',
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

    if (alquiler) {
      setFormData({
        cliente_id: alquiler.cliente_id || '',
        vehiculo_id: alquiler.vehiculo_id || '',
        fecha_inicio: alquiler.fecha_inicio || '',
        fecha_prevista: alquiler.fecha_prevista || '',
        fecha_entrega: alquiler.fecha_entrega || '',
        km_salida: alquiler.km_salida || '',
        km_entrada: alquiler.km_entrada || '',
        observaciones: alquiler.observaciones || '',
      })
    }
  }, [alquiler])

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
      setVehiculos(data)
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

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }

    // Si cambian las fechas, recargar vehículos disponibles
    if (name === 'fecha_inicio' || name === 'fecha_prevista') {
      const newFechaInicio = name === 'fecha_inicio' ? value : formData.fecha_inicio
      const newFechaPrevista = name === 'fecha_prevista' ? value : formData.fecha_prevista

      if (newFechaInicio && newFechaPrevista) {
        loadVehiculosDisponibles(newFechaInicio, newFechaPrevista)
      }
    }
  }

  const loadVehiculosDisponibles = async (fechaInicio, fechaPrevista) => {
    try {
      const response = await fetch(
        `http://localhost:5000/vehiculos/disponibles?fecha_inicio=${fechaInicio}&fecha_prevista=${fechaPrevista}`
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
    if (!formData.fecha_inicio) newErrors.fecha_inicio = 'La fecha de inicio es requerida'
    if (!formData.fecha_prevista) newErrors.fecha_prevista = 'La fecha prevista de devolución es requerida'
    if (!formData.km_salida) newErrors.km_salida = 'El kilometraje de salida es requerido'

    if (formData.fecha_inicio && formData.fecha_prevista) {
      if (new Date(formData.fecha_inicio) > new Date(formData.fecha_prevista)) {
        newErrors.fecha_prevista = 'La fecha prevista debe ser posterior a la de inicio'
      }
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
        km_salida: parseInt(formData.km_salida),
        km_entrada: formData.km_entrada ? parseInt(formData.km_entrada) : null,
      }

      await onSave(dataToSend)
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message

      // Detectar si el error es por cliente deshabilitado
      if (errorMessage.includes('no está habilitado')) {
        setClienteDeshabilitadoId(formData.cliente_id)
        setShowClienteModal(true)
      } else {
        alert('Error al guardar el alquiler: ' + errorMessage)
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
            disabled={formData.fecha_inicio && formData.fecha_prevista ? false : true}
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
          label="Fecha de Inicio"
          name="fecha_inicio"
          type="date"
          value={formData.fecha_inicio}
          onChange={handleChange}
          error={errors.fecha_inicio}
          required
        />

        <Input
          label="Fecha Prevista de Devolución"
          name="fecha_prevista"
          type="date"
          value={formData.fecha_prevista}
          onChange={handleChange}
          error={errors.fecha_prevista}
          min={formData.fecha_inicio || undefined}
          required
        />

        <Input
          label="Fecha Real de Entrega"
          name="fecha_entrega"
          type="date"
          value={formData.fecha_entrega}
          onChange={handleChange}
          min={formData.fecha_inicio || undefined}
          placeholder="Completar al devolver"
        />

        <Input
          label="KM de Salida"
          name="km_salida"
          type="number"
          value={formData.km_salida}
          onChange={handleChange}
          error={errors.km_salida}
          required
          placeholder="50000"
        />

        <Input
          label="KM de Entrada"
          name="km_entrada"
          type="number"
          value={formData.km_entrada}
          onChange={handleChange}
          placeholder="Completar al devolver (ej: 50500)"
        />

        <div className="input-group span-2">
          <label htmlFor="observaciones" className="input-label">
            Observaciones
          </label>
          <textarea
            id="observaciones"
            name="observaciones"
            value={formData.observaciones}
            onChange={handleChange}
            className="input-field"
            rows="3"
            placeholder="Observaciones adicionales..."
          />
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

export default AlquilerForm
