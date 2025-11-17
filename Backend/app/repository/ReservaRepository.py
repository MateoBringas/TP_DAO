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
    def obtener_todos(self) -> list[Reserva]:
        query = "SELECT * FROM reservas"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            reservas: list[Reserva] = []

            for fila in filas:
                reserva = Reserva(
                    cliente=fila["cliente_id"],
                    vehiculo=fila["vehiculo_id"],
                    empleado=fila["empleado_id"],
                    estado_reserva=fila["estado_reserva_id"],
                    fecha_reserva=fila["fecha_reserva"],
                    fecha_alquiler=fila["fecha_alquiler"],
                    senia_monto=fila["senia_monto"],
                    actualizado_en=fila["actualizado_en"],
                    id_reserva=fila["id_reserva"]
                )
                reservas.append(reserva)

            return reservas
