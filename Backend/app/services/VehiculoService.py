from app.models.Vehiculo import Vehiculo
from app.repository.VehiculoRepository import VehiculoRepository

# Reglas de negocio relacionadas con Vehiculo

def crear_vehiculo_service(data: dict):
    """Crea un nuevo vehículo a partir de un diccionario con sus datos."""
    required_fields = ["patente", "marca", "modelo", "anio", "tarifa_base_dia", "km_service_cada"]

    # Validación básica
    for campo in required_fields:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    # Crear instancia de Vehiculo
    vehiculo = Vehiculo(
        patente=data["patente"],
        marca=data["marca"],
        modelo=data["modelo"],
        anio=data["anio"],
        tarifa_base_dia=data["tarifa_base_dia"],
        km_actual=data.get("km_actual", 0),
        habilitado=data.get("habilitado", True),
        seguro_venc=data.get("seguro_venc"),
        vtv_venc=data.get("vtv_venc"),
        km_service_cada=data.get("km_service_cada"),
        km_ultimo_service=data.get("km_ultimo_service", 0),
        fecha_ultimo_service=data.get("fecha_ultimo_service"),
        foto_url=data.get("foto_url")
    )

    # Insertar en la base
    repo = VehiculoRepository()
    return repo.crear(vehiculo)


def obtener_todos_vehiculos_service():
    """Devuelve todos los vehículos."""
    repo = VehiculoRepository()
    return repo.obtener_todos()


def obtener_vehiculos_disponibles_service(fecha_inicio: str, fecha_prevista: str):
    """Devuelve vehículos disponibles en un rango de fechas."""
    from app.repository.Alquiler import AlquilerRepository
    from app.repository.MantenimientoRepository import MantenimientoRepository

    vehiculo_repo = VehiculoRepository()
    alquiler_repo = AlquilerRepository()
    mantenimiento_repo = MantenimientoRepository()

    # Obtener todos los vehículos habilitados
    todos_vehiculos = vehiculo_repo.obtener_todos()
    vehiculos_habilitados = [v for v in todos_vehiculos if v.habilitado]

    # Filtrar solo los disponibles (sin alquileres conflictivos y sin mantenimiento)
    vehiculos_disponibles = []
    for vehiculo in vehiculos_habilitados:
        # Verificar que no esté en mantenimiento
        en_mantenimiento = mantenimiento_repo.vehiculo_en_mantenimiento(vehiculo.id_vehiculo)
        if en_mantenimiento:
            continue

        # Verificar disponibilidad de alquileres
        disponible = alquiler_repo.verificar_disponibilidad(
            vehiculo_id=vehiculo.id_vehiculo,
            fecha_inicio=fecha_inicio,
            fecha_prevista=fecha_prevista
        )
        if disponible:
            vehiculos_disponibles.append(vehiculo)

    return vehiculos_disponibles


def actualizar_vehiculo_service(id_vehiculo: int, data: dict):
    """Actualiza un vehículo existente."""
    repo = VehiculoRepository()

    # Obtener el vehículo existente
    vehiculo = repo.obtener_por_id(id_vehiculo)
    if not vehiculo:
        raise ValueError(f"No se encontró el vehículo con ID {id_vehiculo}")

    # Actualizar los campos
    vehiculo.patente = data.get("patente", vehiculo.patente)
    vehiculo.marca = data.get("marca", vehiculo.marca)
    vehiculo.modelo = data.get("modelo", vehiculo.modelo)
    vehiculo.anio = data.get("anio", vehiculo.anio)
    vehiculo.tarifa_base_dia = data.get("tarifa_base_dia", vehiculo.tarifa_base_dia)
    vehiculo.km_actual = data.get("km_actual", vehiculo.km_actual)
    vehiculo.habilitado = data.get("habilitado", vehiculo.habilitado)
    vehiculo.seguro_venc = data.get("seguro_venc", vehiculo.seguro_venc)
    vehiculo.vtv_venc = data.get("vtv_venc", vehiculo.vtv_venc)
    vehiculo.km_service_cada = data.get("km_service_cada", vehiculo.km_service_cada)
    vehiculo.km_ultimo_service = data.get("km_ultimo_service", vehiculo.km_ultimo_service)
    vehiculo.fecha_ultimo_service = data.get("fecha_ultimo_service", vehiculo.fecha_ultimo_service)

    # Actualizar foto_url si se proporciona
    if "foto_url" in data:
        vehiculo.foto_url = data["foto_url"]

    return repo.actualizar(vehiculo)


def obtener_todos_vehiculos_con_estado_service():
    """Devuelve todos los vehículos con su estado actual (disponible/alquilado/reservado/mantenimiento)"""
    repo = VehiculoRepository()
    return repo.obtener_todos_con_estado()