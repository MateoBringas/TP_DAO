import { useState, useEffect } from 'react'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'
import api from '../../services/api'

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
    foto_url: '',
  })

  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [uploading, setUploading] = useState(false)

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
        foto_url: vehiculo.foto_url || '',
      })
      // Establecer preview si existe foto
      if (vehiculo.foto_url) {
        setPreviewUrl(`http://localhost:5000${vehiculo.foto_url}`)
      }
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

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Validar tipo de archivo
      const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
      if (!allowedTypes.includes(file.type)) {
        alert('Solo se permiten archivos de imagen (PNG, JPG, GIF, WEBP)')
        return
      }

      // Validar tamaño (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('El archivo no debe superar los 5MB')
        return
      }

      setSelectedFile(file)
      // Crear preview local
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewUrl(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const uploadPhoto = async () => {
    if (!selectedFile) return null

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('foto', selectedFile)

      const response = await api.post('/vehiculos/upload-foto', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      return response.data.foto_url
    } catch (error) {
      console.error('Error al subir foto:', error)
      throw new Error('Error al subir la foto')
    } finally {
      setUploading(false)
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
      // Subir foto primero si hay una seleccionada
      let fotoUrl = formData.foto_url
      if (selectedFile) {
        fotoUrl = await uploadPhoto()
      }

      const dataToSend = {
        ...formData,
        anio: parseInt(formData.anio),
        tarifa_base_dia: parseFloat(formData.tarifa_base_dia),
        km_actual: parseInt(formData.km_actual),
        km_service_cada: parseInt(formData.km_service_cada),
        km_ultimo_service: formData.km_ultimo_service ? parseInt(formData.km_ultimo_service) : 0,
        foto_url: fotoUrl,
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
          disabled={true}
        />

        <Input
          label="Fecha último service"
          name="fecha_ultimo_service"
          type="date"
          value={formData.fecha_ultimo_service}
          onChange={handleChange}
          disabled={true}
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

      <div className="photo-upload-section">
        <label className="input-label">Foto del vehículo</label>
        <div className="photo-upload-container">
          {previewUrl && (
            <div className="photo-preview">
              <img src={previewUrl} alt="Preview" />
            </div>
          )}
          <div className="photo-upload-controls">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              id="foto-input"
              style={{ display: 'none' }}
            />
            <Button
              type="button"
              variant="outline"
              onClick={() => document.getElementById('foto-input').click()}
            >
              {previewUrl ? 'Cambiar foto' : 'Seleccionar foto'}
            </Button>
            {selectedFile && (
              <span className="file-name">{selectedFile.name}</span>
            )}
          </div>
        </div>
      </div>

      <div className="form-actions">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
        <Button type="submit" disabled={submitting || uploading}>
          {uploading ? 'Subiendo foto...' : submitting ? 'Guardando...' : 'Guardar'}
        </Button>
      </div>
    </form>
  )
}

export default VehiculoForm
