from app.database.database import get_connection
from app.models.Incidente import Incidente


class IncidenteRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def crear(self, incidente: Incidente) -> Incidente:
        query = """
            INSERT INTO incidentes (
                alquiler_id,
                empleado_id,
                tipo_incidente_id,
                estado_incidente_id,
                fecha,
                descripcion,
                costo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            incidente.alquiler_id,
            incidente.empleado_id,
            incidente.tipo_incidente_id,
            incidente.estado_incidente_id,
            incidente.fecha,
            incidente.descripcion,
            incidente.costo,
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            incidente.id_incidente = cursor.lastrowid
            return incidente

    def obtener_todos(self) -> list[Incidente]:
        query = "SELECT * FROM incidentes"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            incidentes: list[Incidente] = []

            for fila in filas:
                incidente = Incidente(
                    alquiler=None,   # podés cargarlo luego con AlquilerRepository
                    empleado=None,
                    tipo_incidente=None,
                    estado_incidente=None,
                    fecha=fila["fecha"],
                    descripcion=fila["descripcion"],
                    costo=fila["costo"],
                    alquiler_id=fila["alquiler_id"],
                    empleado_id=fila["empleado_id"],
                    tipo_incidente_id=fila["tipo_incidente_id"],
                    estado_incidente_id=fila["estado_incidente_id"],
                    id_incidente=fila["id_incidente"],
                )
                incidentes.append(incidente)

            return incidentes
