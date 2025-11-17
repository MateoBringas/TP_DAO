import { useState, useEffect } from 'react'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'

const ClienteForm = ({ cliente, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    dni: '',
    nombre: '',
    apellido: '',
    email: '',
    telefono: '',
    direccion: '',
    licencia_num: '',
    licencia_venc: '',
    habilitado: true,
  })

  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (cliente) {
      setFormData({
        dni: cliente.dni || '',
        nombre: cliente.nombre || '',
        apellido: cliente.apellido || '',
        email: cliente.email || '',
        telefono: cliente.telefono || '',
        direccion: cliente.direccion || '',
        licencia_num: cliente.licencia_num || '',
        licencia_venc: cliente.licencia_venc || '',
        habilitado: cliente.habilitado !== undefined ? cliente.habilitado : true,
      })
    }
  }, [cliente])

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

    if (!formData.nombre.trim()) newErrors.nombre = 'El nombre es requerido'
    if (!formData.apellido.trim()) newErrors.apellido = 'El apellido es requerido'
    if (!formData.email.trim()) newErrors.email = 'El email es requerido'
    if (!formData.telefono.trim()) newErrors.telefono = 'El teléfono es requerido'
    if (!formData.licencia_num.trim()) newErrors.licencia_num = 'El número de licencia es requerido'
    if (!formData.licencia_venc) newErrors.licencia_venc = 'La fecha de vencimiento de licencia es requerida'

    // Validación de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (formData.email && !emailRegex.test(formData.email)) {
      newErrors.email = 'El email no es válido'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validate()) return

    setSubmitting(true)
    try {
      await onSave(formData)
    } catch (err) {
      alert('Error al guardar el cliente: ' + (err.response?.data?.error || err.message))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-grid">
        <Input
          label="DNI"
          name="dni"
          value={formData.dni}
          onChange={handleChange}
          error={errors.dni}
          placeholder="12345678"
        />

        <Input
          label="Nombre"
          name="nombre"
          value={formData.nombre}
          onChange={handleChange}
          error={errors.nombre}
          required
          placeholder="Juan"
        />

        <Input
          label="Apellido"
          name="apellido"
          value={formData.apellido}
          onChange={handleChange}
          error={errors.apellido}
          required
          placeholder="Pérez"
        />

        <Input
          label="Email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          required
          placeholder="juan.perez@email.com"
        />

        <Input
          label="Teléfono"
          name="telefono"
          value={formData.telefono}
          onChange={handleChange}
          error={errors.telefono}
          required
          placeholder="1122334455"
        />

        <Input
          label="Dirección"
          name="direccion"
          value={formData.direccion}
          onChange={handleChange}
          error={errors.direccion}
          placeholder="Av. Corrientes 1234"
        />

        <Input
          label="Número de Licencia"
          name="licencia_num"
          value={formData.licencia_num}
          onChange={handleChange}
          error={errors.licencia_num}
          required
          placeholder="LIC001"
        />

        <Input
          label="Vencimiento de Licencia"
          name="licencia_venc"
          type="date"
          value={formData.licencia_venc}
          onChange={handleChange}
          error={errors.licencia_venc}
          required
        />

        <div className="input-group checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="habilitado"
              checked={formData.habilitado}
              onChange={handleChange}
            />
            <span>Cliente habilitado</span>
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

export default ClienteForm
