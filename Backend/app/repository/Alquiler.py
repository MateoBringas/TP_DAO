from app.database.database import get_connection
from app.models.Alquiler import Alquiler


class AlquilerRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def crear(self, alquiler: Alquiler) -> Alquiler:
        data = alquiler.to_dict()

        query = """
            INSERT INTO alquileres (
                cliente_id,
                vehiculo_id,
                empleado_id,
                reserva_id,
                estado_alquiler,
                fecha_inicio,
                fecha_fin,
                km_inicio,
                km_fin,
                monto_total,
                observaciones,
                creado_en,
                actualizado_en
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        valores = (
            data["cliente_id"],
            data["vehiculo_id"],
            data["empleado_id"],
            data["reserva_id"],
            data["estado_alquiler"],
            data["fecha_inicio"],
            data["fecha_fin"],
            data["km_inicio"],
            data["km_fin"],
            data["monto_total"],
            data["observaciones"],
            data["creado_en"],
            data["actualizado_en"],
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            alquiler.id_alquiler = cursor.lastrowid
            return alquiler

    def obtener_todos(self) -> list[Alquiler]:
        query = "SELECT * FROM alquileres"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            alquileres: list[Alquiler] = []

            for fila in filas:
                alquiler = Alquiler(
                    cliente=None,   # luego podés cargar Cliente con ClienteRepository usando fila["cliente_id"]
                    vehiculo=None,  # idem VehiculoRepository
                    empleado=None,  # idem EmpleadoRepository
                    estado_alquiler=fila["estado_alquiler"],
                    creado_en=fila["creado_en"],
                    reserva=None,   # si la usás, podés cargarla con ReservaRepository
                    fecha_inicio=fila["fecha_inicio"],
                    fecha_fin=fila["fecha_fin"],
                    km_inicio=fila["km_inicio"],
                    km_fin=fila["km_fin"],
                    monto_total=fila["monto_total"],
                    observaciones=fila["observaciones"],
                    actualizado_en=fila["actualizado_en"],
                    id_alquiler=fila["id_alquiler"],
                )
                alquileres.append(alquiler)

            return alquileres
