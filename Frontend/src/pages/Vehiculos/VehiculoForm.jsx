import { useState, useEffect } from 'react'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'

const VehiculoForm = ({ vehiculo, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    patente: '',
    marca: '',
    modelo: '',
    anio: '',
    tarifa_base_dia: '',
    km_actual: '',
    km_service_cada: '',
    km_ultimo_service: '',
    fecha_ultimo_service: '',
    seguro_venc: '',
    vtv_venc: '',
    habilitado: true,
  })

  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (vehiculo) {
      setFormData({
        patente: vehiculo.patente || '',
        marca: vehiculo.marca || '',
        modelo: vehiculo.modelo || '',
        anio: vehiculo.anio || '',
        tarifa_base_dia: vehiculo.tarifa_base_dia || '',
        km_actual: vehiculo.km_actual || '',
        km_service_cada: vehiculo.km_service_cada || '',
        km_ultimo_service: vehiculo.km_ultimo_service || '',
        fecha_ultimo_service: vehiculo.fecha_ultimo_service || '',
        seguro_venc: vehiculo.seguro_venc || '',
        vtv_venc: vehiculo.vtv_venc || '',
        habilitado: vehiculo.habilitado !== undefined ? vehiculo.habilitado : true,
      })
    }
  }, [vehiculo])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
    // Limpiar error del campo
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validate = () => {
    const newErrors = {}

    if (!formData.patente.trim()) newErrors.patente = 'La patente es requerida'
    if (!formData.marca.trim()) newErrors.marca = 'La marca es requerida'
    if (!formData.modelo.trim()) newErrors.modelo = 'El modelo es requerido'
    if (!formData.anio) newErrors.anio = 'El año es requerido'
    if (!formData.tarifa_base_dia) newErrors.tarifa_base_dia = 'La tarifa es requerida'
    if (!formData.km_actual) newErrors.km_actual = 'El kilometraje actual es requerido'
    if (!formData.km_service_cada) newErrors.km_service_cada = 'Los KM entre servicios son requeridos'

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
        anio: parseInt(formData.anio),
        tarifa_base_dia: parseFloat(formData.tarifa_base_dia),
        km_actual: parseInt(formData.km_actual),
        km_service_cada: parseInt(formData.km_service_cada),
        km_ultimo_service: formData.km_ultimo_service ? parseInt(formData.km_ultimo_service) : 0,
      }

      await onSave(dataToSend)
    } catch (err) {
      alert('Error al guardar el vehículo: ' + (err.response?.data?.error || err.message))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-grid">
        <Input
          label="Patente"
          name="patente"
          value={formData.patente}
          onChange={handleChange}
          error={errors.patente}
          required
          placeholder="ABC123"
        />

        <Input
          label="Marca"
          name="marca"
          value={formData.marca}
          onChange={handleChange}
          error={errors.marca}
          required
          placeholder="Toyota"
        />

        <Input
          label="Modelo"
          name="modelo"
          value={formData.modelo}
          onChange={handleChange}
          error={errors.modelo}
          required
          placeholder="Corolla"
        />

        <Input
          label="Año"
          name="anio"
          type="number"
          value={formData.anio}
          onChange={handleChange}
          error={errors.anio}
          required
          placeholder="2024"
        />

        <Input
          label="Tarifa por día ($)"
          name="tarifa_base_dia"
          type="number"
          step="0.01"
          value={formData.tarifa_base_dia}
          onChange={handleChange}
          error={errors.tarifa_base_dia}
          required
          placeholder="5000"
        />

        <Input
          label="KM Actual"
          name="km_actual"
          type="number"
          value={formData.km_actual}
          onChange={handleChange}
          error={errors.km_actual}
          required
          placeholder="50000"
        />

        <Input
          label="KM entre servicios"
          name="km_service_cada"
          type="number"
          value={formData.km_service_cada}
          onChange={handleChange}
          error={errors.km_service_cada}
          required
          placeholder="10000"
        />

        <Input
          label="KM último service"
          name="km_ultimo_service"
          type="number"
          value={formData.km_ultimo_service}
          onChange={handleChange}
          placeholder="40000"
        />

        <Input
          label="Fecha último service"
          name="fecha_ultimo_service"
          type="date"
          value={formData.fecha_ultimo_service}
          onChange={handleChange}
        />

        <Input
          label="Vencimiento seguro"
          name="seguro_venc"
          type="date"
          value={formData.seguro_venc}
          onChange={handleChange}
        />

        <Input
          label="Vencimiento VTV"
          name="vtv_venc"
          type="date"
          value={formData.vtv_venc}
          onChange={handleChange}
        />

        <div className="input-group checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="habilitado"
              checked={formData.habilitado}
              onChange={handleChange}
            />
            <span>Vehículo habilitado</span>
          </label>
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

export default VehiculoForm
