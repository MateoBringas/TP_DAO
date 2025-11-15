from app.database.database import get_connection
from app.models.Mantenimiento import Mantenimiento


class MantenimientoRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def crear(self, mantenimiento: Mantenimiento) -> Mantenimiento:
        query = """
            INSERT INTO mantenimientos (
                vehiculo_id,
                empleado_id,
                estado_mantenimiento,
                fecha_programada,
                fecha_realizada,
                km,
                costo,
                observacion
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            mantenimiento.vehiculo.id_vehiculo if mantenimiento.vehiculo else None,
            mantenimiento.empleado.id_empleado if mantenimiento.empleado else None,
            mantenimiento.estado_mantenimiento,
            mantenimiento.fecha_programada,
            mantenimiento.fecha_realizada,
            mantenimiento.km,
            mantenimiento.costo,
            mantenimiento.observacion,
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            mantenimiento.id_mantenimiento = cursor.lastrowid
            return mantenimiento

    def obtener_todos(self) -> list[Mantenimiento]:
        query = "SELECT * FROM mantenimientos"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            mantenimientos: list[Mantenimiento] = []

            for fila in filas:
                mantenimiento = Mantenimiento(
                    vehiculo=None,   # después podés cargarlo con VehiculoRepository si querés
                    empleado=None,   # idem con EmpleadoRepository
                    estado_mantenimiento=fila["estado_mantenimiento"],
                    fecha_programada=fila["fecha_programada"],
                    fecha_realizada=fila["fecha_realizada"],
                    km=fila["km"],
                    costo=fila["costo"],
                    observacion=fila["observacion"],
                    id_mantenimiento=fila["id_mantenimiento"],
                )
                mantenimientos.append(mantenimiento)

            return mantenimientos
