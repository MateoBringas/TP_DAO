from app.database.database import get_connection
from app.models.Reserva import Reserva


class ReservaRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    # CREATE
    def crear(self, reserva: Reserva) -> Reserva:
        query = """
            INSERT INTO reservas (
                cliente_id,
                vehiculo_id,
                empleado_id,
                estado_reserva_id,
                fecha_reserva,
                fecha_alquiler,
                senia_monto,
                actualizado_en
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        valores = (
            reserva.cliente_id,
            reserva.vehiculo_id,
            reserva.empleado_id,
            reserva.estado_reserva_id,
            reserva.fecha_reserva,
            reserva.fecha_alquiler,
            reserva.senia_monto,
            reserva.actualizado_en,
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            reserva.id_reserva = cursor.lastrowid  # guardar el ID generado
            return reserva

    # READ: obtener todos
    def obtener_todos(self) -> list[dict]:
        """Obtiene todas las reservas con información completa de cliente y vehículo"""
        query = """
            SELECT
                r.*,
                c.nombre as cliente_nombre,
                c.apellido as cliente_apellido,
                c.dni as cliente_dni,
                v.patente as vehiculo_patente,
                v.marca as vehiculo_marca,
                v.modelo as vehiculo_modelo,
                er.codigo as estado_nombre
            FROM reservas r
            LEFT JOIN clientes c ON r.cliente_id = c.id_cliente
            LEFT JOIN vehiculos v ON r.vehiculo_id = v.id_vehiculo
            LEFT JOIN estados_reserva er ON r.estado_reserva_id = er.id_estado_reserva
            ORDER BY r.fecha_reserva DESC
        """
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            reservas = []

            for fila in filas:
                reserva_dict = {
                    "id_reserva": fila["id_reserva"],
                    "cliente_id": fila["cliente_id"],
                    "cliente_nombre_completo": f"{fila['cliente_nombre']} {fila['cliente_apellido']}" if fila['cliente_nombre'] else "N/A",
                    "cliente_dni": fila["cliente_dni"],
                    "vehiculo_id": fila["vehiculo_id"],
                    "vehiculo_descripcion": f"{fila['vehiculo_marca']} {fila['vehiculo_modelo']} - {fila['vehiculo_patente']}" if fila['vehiculo_marca'] else "N/A",
                    "empleado_id": fila["empleado_id"],
                    "estado_reserva_id": fila["estado_reserva_id"],
                    "estado_nombre": fila["estado_nombre"],
                    "fecha_reserva": fila["fecha_reserva"],
                    "fecha_alquiler": fila["fecha_alquiler"],
                    "senia_monto": fila["senia_monto"],
                    "actualizado_en": fila["actualizado_en"]
                }
                reservas.append(reserva_dict)

            return reservas

    def verificar_disponibilidad(self, vehiculo_id: int, fecha_alquiler: str, excluir_reserva_id: int = None) -> bool:
        """
        Verifica si un vehículo está disponible para una fecha de alquiler específica.
        Retorna True si está disponible, False si ya está reservado o alquilado.
        """
        query = """
            SELECT COUNT(*) as count FROM (
                -- Verificar reservas existentes para la misma fecha
                SELECT 1 FROM reservas
                WHERE vehiculo_id = ?
                AND estado_reserva_id IN (1, 2)  -- PENDIENTE (1) o CONFIRMADA (2)
                AND fecha_alquiler = ?
                AND (? IS NULL OR id_reserva != ?)

                UNION

                -- Verificar alquileres que cubren esa fecha
                SELECT 1 FROM alquileres
                WHERE vehiculo_id = ?
                AND estado_alquiler_id IN (1, 2)  -- PENDIENTE (1) o ACTIVO (2)
                AND date(fecha_inicio) <= date(?)
                AND (fecha_entrega IS NULL OR date(fecha_prevista) >= date(?))
            ) AS conflictos
        """

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                vehiculo_id, fecha_alquiler, excluir_reserva_id, excluir_reserva_id,
                vehiculo_id, fecha_alquiler, fecha_alquiler
            ))
            resultado = cursor.fetchone()
            return resultado["count"] == 0
