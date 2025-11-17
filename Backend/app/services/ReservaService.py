from app.models.Reserva import Reserva
from app.repository.ReservaRepository import ReservaRepository
from app.repository.VehiculoRepository import VehiculoRepository
from app.repository.ClienteRepository import ClienteRepository
from app.repository.EmpleadoRepository import EmpleadoRepository
from datetime import datetime

def crear_reserva_service(data: dict):
    """Crea una nueva reserva."""
    required_fields = ["cliente_id", "vehiculo_id", "fecha_reserva", "fecha_alquiler"]

    for campo in required_fields:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    # Verificar que el vehículo existe y está habilitado
    vehiculo_repo = VehiculoRepository()
    vehiculo = vehiculo_repo.obtener_por_id(data["vehiculo_id"])
    if not vehiculo:
        raise ValueError("El vehículo especificado no existe")
    if not vehiculo.habilitado:
        raise ValueError("El vehículo no está habilitado para reservas")

    # Verificar que el cliente existe
    cliente_repo = ClienteRepository()
    cliente = cliente_repo.obtener_por_id(data["cliente_id"])
    if not cliente:
        raise ValueError("El cliente especificado no existe")

    reserva = Reserva(
        cliente=data.get("cliente_id"),
        vehiculo=data.get("vehiculo_id"),
        empleado=data.get("empleado_id", 1),  # Default empleado
        estado_reserva=data.get("estado_reserva_id", 1),  # Default PENDIENTE
        fecha_reserva=data["fecha_reserva"],
        fecha_alquiler=data["fecha_alquiler"],
        senia_monto=data.get("senia_monto", 0),
        actualizado_en=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    repo = ReservaRepository()
    return repo.crear(reserva)


def obtener_todas_reservas_service():
    """Devuelve todas las reservas."""
    repo = ReservaRepository()
    return repo.obtener_todos()


def obtener_reserva_por_id_service(id_reserva: int):
    """Obtiene una reserva por su ID."""
    repo = ReservaRepository()
    reservas = repo.obtener_todos()
    for reserva in reservas:
        if reserva.id_reserva == id_reserva:
            return reserva
    return None


def actualizar_reserva_service(id_reserva: int, data: dict):
    """Actualiza una reserva existente."""
    repo = ReservaRepository()

    # Verificar que existe
    reserva_existente = obtener_reserva_por_id_service(id_reserva)
    if not reserva_existente:
        raise ValueError("La reserva no existe")

    reserva = Reserva(
        cliente=data.get("cliente_id"),
        vehiculo=data.get("vehiculo_id"),
        empleado=data.get("empleado_id", 1),
        estado_reserva=data.get("estado_reserva_id", 1),
        fecha_reserva=data["fecha_reserva"],
        fecha_alquiler=data["fecha_alquiler"],
        senia_monto=data.get("senia_monto", 0),
        actualizado_en=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        id_reserva=id_reserva
    )

    # Actualizar en la base de datos
    query = """
        UPDATE reservas
        SET cliente_id = ?, vehiculo_id = ?, empleado_id = ?,
            estado_reserva_id = ?, fecha_reserva = ?, fecha_alquiler = ?,
            senia_monto = ?, actualizado_en = ?
        WHERE id_reserva = ?
    """

    from app.database.database import get_connection
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            reserva.cliente_id,
            reserva.vehiculo_id,
            reserva.empleado_id,
            reserva.estado_reserva_id,
            reserva.fecha_reserva,
            reserva.fecha_alquiler,
            reserva.senia_monto,
            reserva.actualizado_en,
            id_reserva
        ))
        conn.commit()

    return reserva


def eliminar_reserva_service(id_reserva: int):
    """Elimina una reserva por su ID."""
    from app.database.database import get_connection

    # Verificar que existe
    reserva = obtener_reserva_por_id_service(id_reserva)
    if not reserva:
        return False

    query = "DELETE FROM reservas WHERE id_reserva = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (id_reserva,))
        conn.commit()

    return True
