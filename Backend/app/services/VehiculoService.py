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
        fecha_ultimo_service=data.get("fecha_ultimo_service")
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

    vehiculo_repo = VehiculoRepository()
    alquiler_repo = AlquilerRepository()

    # Obtener todos los vehículos habilitados
    todos_vehiculos = vehiculo_repo.obtener_todos()
    vehiculos_habilitados = [v for v in todos_vehiculos if v.habilitado]

    # Filtrar solo los disponibles
    vehiculos_disponibles = []
    for vehiculo in vehiculos_habilitados:
        disponible = alquiler_repo.verificar_disponibilidad(
            vehiculo_id=vehiculo.id_vehiculo,
            fecha_inicio=fecha_inicio,
            fecha_prevista=fecha_prevista
        )
        if disponible:
            vehiculos_disponibles.append(vehiculo)

    return vehiculos_disponibles