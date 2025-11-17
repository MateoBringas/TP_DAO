from app.models.Mantenimiento import Mantenimiento
from app.repository.MantenimientoRepository import MantenimientoRepository
from app.repository.VehiculoRepository import VehiculoRepository
from app.repository.EmpleadoRepository import EmpleadoRepository
from datetime import datetime

def crear_mantenimiento_service(data: dict):
    """Crea un nuevo mantenimiento."""
    required_fields = ["vehiculo_id", "fecha_programada", "km"]

    for campo in required_fields:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    # Verificar que el vehículo existe
    vehiculo_repo = VehiculoRepository()
    vehiculo = vehiculo_repo.obtener_por_id(data["vehiculo_id"])
    if not vehiculo:
        raise ValueError("El vehículo especificado no existe")

    mantenimiento = Mantenimiento(
        vehiculo=vehiculo,
        empleado=None,  # Se puede asignar después
        estado_mantenimiento=data.get("estado_mantenimiento", "PROGRAMADO"),
        fecha_programada=data["fecha_programada"],
        fecha_realizada=data.get("fecha_realizada"),
        km=data["km"],
        costo=data.get("costo", 0),
        observacion=data.get("observacion")
    )

    repo = MantenimientoRepository()
    return repo.crear(mantenimiento)


def obtener_todos_mantenimientos_service():
    """Devuelve todos los mantenimientos."""
    repo = MantenimientoRepository()
    return repo.obtener_todos()


def obtener_mantenimiento_por_id_service(id_mantenimiento: int):
    """Obtiene un mantenimiento por su ID."""
    repo = MantenimientoRepository()
    mantenimientos = repo.obtener_todos()
    for mantenimiento in mantenimientos:
        if mantenimiento.id_mantenimiento == id_mantenimiento:
            return mantenimiento
    return None


def actualizar_mantenimiento_service(id_mantenimiento: int, data: dict):
    """Actualiza un mantenimiento existente."""
    # Verificar que existe
    mantenimiento_existente = obtener_mantenimiento_por_id_service(id_mantenimiento)
    if not mantenimiento_existente:
        raise ValueError("El mantenimiento no existe")

    # Obtener el vehículo
    vehiculo_repo = VehiculoRepository()
    vehiculo = vehiculo_repo.obtener_por_id(data.get("vehiculo_id"))
    if not vehiculo:
        raise ValueError("El vehículo especificado no existe")

    # Actualizar en la base de datos
    query = """
        UPDATE mantenimientos
        SET vehiculo_id = ?, empleado_id = ?, estado_mantenimiento = ?,
            fecha_programada = ?, fecha_realizada = ?, km = ?,
            costo = ?, observacion = ?
        WHERE id_mantenimiento = ?
    """

    from app.database.database import get_connection
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            data.get("vehiculo_id"),
            data.get("empleado_id"),
            data.get("estado_mantenimiento", "PROGRAMADO"),
            data.get("fecha_programada"),
            data.get("fecha_realizada"),
            data.get("km"),
            data.get("costo", 0),
            data.get("observacion"),
            id_mantenimiento
        ))
        conn.commit()

    # Retornar el mantenimiento actualizado
    return obtener_mantenimiento_por_id_service(id_mantenimiento)


def eliminar_mantenimiento_service(id_mantenimiento: int):
    """Elimina un mantenimiento por su ID."""
    from app.database.database import get_connection

    # Verificar que existe
    mantenimiento = obtener_mantenimiento_por_id_service(id_mantenimiento)
    if not mantenimiento:
        return False

    query = "DELETE FROM mantenimientos WHERE id_mantenimiento = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (id_mantenimiento,))
        conn.commit()

    return True
