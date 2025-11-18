from app.models.Alquiler import Alquiler
from app.repository.Alquiler import AlquilerRepository
from app.repository.ClienteRepository import ClienteRepository
from app.repository.VehiculoRepository import VehiculoRepository
from app.repository.MantenimientoRepository import MantenimientoRepository
from datetime import datetime

def crear_alquiler_service(data: dict):
    """Crea un nuevo alquiler."""
    required_fields = ["cliente_id", "vehiculo_id", "fecha_inicio", "fecha_prevista", "km_salida"]

    for campo in required_fields:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    # Verificar que el cliente existe y está habilitado
    cliente_repo = ClienteRepository()
    cliente = cliente_repo.obtener_por_id(data["cliente_id"])
    if not cliente:
        raise ValueError("El cliente especificado no existe")
    if not cliente.habilitado:
        raise ValueError("El cliente no está habilitado para realizar alquileres")

    # Verificar que el vehículo existe y está habilitado
    vehiculo_repo = VehiculoRepository()
    vehiculo = vehiculo_repo.obtener_por_id(data["vehiculo_id"])
    if not vehiculo:
        raise ValueError("El vehículo especificado no existe")
    if not vehiculo.habilitado:
        raise ValueError("El vehículo no está habilitado para alquileres")

    # Verificar que el vehículo no esté en mantenimiento
    mantenimiento_repo = MantenimientoRepository()
    en_mantenimiento = mantenimiento_repo.vehiculo_en_mantenimiento(data["vehiculo_id"])
    if en_mantenimiento:
        raise ValueError("El vehículo está actualmente en mantenimiento y no puede ser alquilado")

    repo = AlquilerRepository()

    # Verificar disponibilidad del vehículo
    disponible = repo.verificar_disponibilidad(
        vehiculo_id=data["vehiculo_id"],
        fecha_inicio=data["fecha_inicio"],
        fecha_prevista=data["fecha_prevista"]
    )

    if not disponible:
        raise ValueError("El vehículo no está disponible en el período seleccionado")

    alquiler = Alquiler(
        cliente=data.get("cliente_id"),
        vehiculo=data.get("vehiculo_id"),
        empleado=data.get("empleado_id", 1),  # Default empleado
        estado_alquiler=data.get("estado_alquiler", 1),  # Default PENDIENTE
        reserva=data.get("reserva_id"),
        fecha_inicio=data["fecha_inicio"],
        fecha_prevista=data["fecha_prevista"],
        fecha_entrega=data.get("fecha_entrega"),
        km_salida=data["km_salida"],
        km_entrada=data.get("km_entrada"),
        observaciones=data.get("observaciones"),
        creado_en=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        actualizado_en=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return repo.crear(alquiler)


def obtener_todos_alquileres_service():
    """Devuelve todos los alquileres."""
    repo = AlquilerRepository()
    return repo.obtener_todos()


def obtener_alquiler_por_id_service(id_alquiler: int):
    """Obtiene un alquiler por su ID."""
    repo = AlquilerRepository()
    return repo.obtener_por_id(id_alquiler)


def actualizar_alquiler_service(id_alquiler: int, data: dict):
    """Actualiza un alquiler existente."""
    repo = AlquilerRepository()

    # Verificar disponibilidad del vehículo (excluyendo el alquiler actual)
    disponible = repo.verificar_disponibilidad(
        vehiculo_id=data["vehiculo_id"],
        fecha_inicio=data["fecha_inicio"],
        fecha_prevista=data["fecha_prevista"],
        excluir_alquiler_id=id_alquiler
    )

    if not disponible:
        raise ValueError("El vehículo no está disponible en el período seleccionado")

    alquiler = Alquiler(
        cliente=data.get("cliente_id"),
        vehiculo=data.get("vehiculo_id"),
        empleado=data.get("empleado_id", 1),
        estado_alquiler=data.get("estado_alquiler", 1),
        reserva=data.get("reserva_id"),
        fecha_inicio=data["fecha_inicio"],
        fecha_prevista=data["fecha_prevista"],
        fecha_entrega=data.get("fecha_entrega"),
        km_salida=data["km_salida"],
        km_entrada=data.get("km_entrada"),
        observaciones=data.get("observaciones"),
        creado_en=data.get("creado_en"),
        actualizado_en=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return repo.actualizar(id_alquiler, alquiler)


def eliminar_alquiler_service(id_alquiler: int):
    """Elimina un alquiler por su ID."""
    repo = AlquilerRepository()
    return repo.eliminar(id_alquiler)
