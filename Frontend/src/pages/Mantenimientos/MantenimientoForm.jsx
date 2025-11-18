import { useState, useEffect } from 'react'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'
import vehiculoService from '../../services/vehiculoService'

const MantenimientoForm = ({ mantenimiento, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    vehiculo_id: '',
    empleado_id: 1,
    estado_mantenimiento: 'PROGRAMADO',
    fecha_programada: '',
    fecha_realizada: '',
    km: '',
    costo: '',
    observacion: '',
  })

  const [vehiculos, setVehiculos] = useState([])
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  // Obtiene la fecha de hoy en formato YYYY-MM-DD
  const today = new Date().toISOString().split('T')[0]; 
  const isEditing = !!mantenimiento;
  const isProgramado = formData.estado_mantenimiento === 'PROGRAMADO';
  const isEnCurso = formData.estado_mantenimiento === 'EN_CURSO';
  const isCompletado = formData.estado_mantenimiento === 'COMPLETADO';
  const isCancelado = formData.estado_mantenimiento === 'CANCELADO';

  // Reglas de Disabling
  const isFechaRealizadaDisabled = isProgramado || isCancelado;
  
  // Deshabilitar Fecha Programada una vez que está en curso o finalizado/cancelado
  const isFechaProgramadaDisabled = isEnCurso || (isEditing && (isCompletado || isCancelado));
  
  // Reglas de Required
  const isFechaProgramadaRequired = !isCompletado && !isCancelado;
  const isFechaRealizadaRequired = isCompletado;

  useEffect(() => {
    loadVehiculos()

    if (mantenimiento) {
      setFormData({
        vehiculo_id: mantenimiento.vehiculo?.id_vehiculo || '', 
        estado_mantenimiento: mantenimiento.estado_mantenimiento || 'PROGRAMADO',
        fecha_programada: mantenimiento.fecha_programada || '',
        fecha_realizada: mantenimiento.fecha_realizada || '',
        km: mantenimiento.km || '',
        costo: mantenimiento.costo || '',
        observacion: mantenimiento.observacion || '',
      })
    } else {
      setFormData(prev => ({ ...prev, fecha_programada: today }))
    }
  }, [mantenimiento])

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
    
    setFormData(prev => {
        let newFormData = { ...prev, [name]: value };
        return newFormData;
    })

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validate = () => {
    const newErrors = {}

    if (!formData.vehiculo_id) newErrors.vehiculo_id = 'Seleccione un vehículo'
    if (!formData.km) newErrors.km = 'El kilometraje es requerido'
    if (formData.km && parseInt(formData.km) < 0) {
      newErrors.km = 'El kilometraje no puede ser negativo'
    }
    if (formData.costo && parseFloat(formData.costo) < 0) {
      newErrors.costo = 'El costo no puede ser negativo'
    }
    
    // Validación de Fecha Programada (Requerida si no es Completado/Cancelado)
    if (isFechaProgramadaRequired && !formData.fecha_programada) {
        newErrors.fecha_programada = 'La fecha programada es requerida para este estado';
    }
    
    // Validación de Fecha Realizada (Requerida solo si es Completado)
    if (isFechaRealizadaRequired && !formData.fecha_realizada) {
        newErrors.fecha_realizada = 'La fecha de realización es requerida al completar el mantenimiento';
    }

    // Validación de Fecha Programada vs Hoy (Solo si es PROGRAMADO)
    if (isProgramado && formData.fecha_programada) {
        if (new Date(formData.fecha_programada) < new Date(today)) {
             newErrors.fecha_programada = 'La fecha programada no puede ser anterior a hoy.';
        }
    }
    
    // Validación de Fecha Realizada vs Programada (Solo si ambas existen)
    if (formData.fecha_realizada && formData.fecha_programada) {
      if (new Date(formData.fecha_realizada) < new Date(formData.fecha_programada)) {
        newErrors.fecha_realizada = 'La fecha realizada no puede ser anterior a la programada'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Manejo de valores nulos para fechas opcionales según el estado antes de enviar al backend
    let finalFechaProgramada = formData.fecha_programada;
    if ((isCompletado || isCancelado) && !formData.fecha_programada) {
        finalFechaProgramada = null;
    }

    let finalFechaRealizada = formData.fecha_realizada;
    if (isFechaRealizadaDisabled && !formData.fecha_realizada) {
        finalFechaRealizada = null;
    }

    if (!validate()) return

    setSubmitting(true)
    try {
      const dataToSend = {
        ...formData,
        vehiculo_id: parseInt(formData.vehiculo_id),
        empleado_id: formData.empleado_id ? parseInt(formData.empleado_id) : null,
        km: parseInt(formData.km),
        costo: formData.costo ? parseFloat(formData.costo) : 0,
        fecha_programada: finalFechaProgramada,
        fecha_realizada: finalFechaRealizada,
      }

      await onSave(dataToSend)
    } catch (err) {
      alert('Error al guardar el mantenimiento: ' + (err.response?.data?.error || err.message))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-grid">
        <div className="input-group">
          <label htmlFor="vehiculo_id" className="input-label">
            Vehículo<span className="required">*</span>
          </label>
          <select
            id="vehiculo_id"
            name="vehiculo_id"
            value={formData.vehiculo_id}
            disabled={mantenimiento?.vehiculo?.id_vehiculo} 
            onChange={handleChange}
            className={`input-field ${errors.vehiculo_id ? 'input-error' : ''}`}
            required
          >
            <option value="">Seleccione un vehículo</option>
            {vehiculos.map(vehiculo => (
              <option key={vehiculo.id_vehiculo} value={vehiculo.id_vehiculo}>
                {vehiculo.marca} {vehiculo.modelo} - {vehiculo.patente} (KM: {vehiculo.km_actual})
              </option>
            ))}
          </select>
          {errors.vehiculo_id && <span className="error-message">{errors.vehiculo_id}</span>}
        </div>

        <div className="input-group">
          <label htmlFor="estado_mantenimiento" className="input-label">
            Estado<span className="required">*</span>
          </label>
          <select
            id="estado_mantenimiento"
            name="estado_mantenimiento"
            value={formData.estado_mantenimiento}
            onChange={handleChange}
            className="input-field"
            disabled={!mantenimiento}
            required
          >
            <option value="PROGRAMADO">Programado</option>
            <option value="EN_CURSO">En Curso</option>
            <option value="COMPLETADO">Completado</option>
            <option value="CANCELADO">Cancelado</option>
          </select>
        </div>

        <Input
          label="Fecha Programada"
          name="fecha_programada"
          type="date"
          value={formData.fecha_programada}
          onChange={handleChange}
          error={errors.fecha_programada}
          // Bloquea el campo si está EN CURSO, COMPLETADO o CANCELADO (en edición)
          disabled={isFechaProgramadaDisabled}
          // Es requerido, a menos que sea un registro histórico (Completado/Cancelado)
          required={isFechaProgramadaRequired}
          // Mínimo = Hoy, SOLO si está PROGRAMADO
          min={isProgramado ? today : undefined}
        />

        <Input
          label="Fecha Realizada"
          name="fecha_realizada"
          type="date"
          // Bloquea el campo si es PROGRAMADO o CANCELADO
          disabled={isFechaRealizadaDisabled}
          value={formData.fecha_realizada}
          onChange={handleChange}
          error={errors.fecha_realizada}
          placeholder="Completar cuando se realice"
          // Es requerido SÓLO si está COMPLETADO
          required={isFechaRealizadaRequired}
          // Mínimo: La fecha programada (si existe), para no permitir una fecha anterior a la programación
          min={formData.fecha_programada || undefined} 
        />

        <Input
          label="Kilometraje"
          name="km"
          type="number"
          value={formData.km}
          onChange={handleChange}
          error={errors.km}
          required
          placeholder="50000"
        />

        <Input
          label="Costo"
          name="costo"
          type="number"
          step="0.01"
          value={formData.costo}
          onChange={handleChange}
          error={errors.costo}
          placeholder="0.00"
        />

        <div className="input-group span-2">
          <label htmlFor="observacion" className="input-label">
            Observaciones
          </label>
          <textarea
            id="observacion"
            name="observacion"
            value={formData.observacion}
            onChange={handleChange}
            className="input-field"
            rows="4"
            placeholder="Detalles del mantenimiento (cambio de aceite, revisión de frenos, etc.)..."
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
    </form>
  )
}

export default MantenimientoForm