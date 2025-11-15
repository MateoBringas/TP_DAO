from app.database.database import get_connection
from app.models.TipoIncidente import TipoIncidente

class TipoIncidenteRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def crear(self, tipo_incidente: TipoIncidente) -> TipoIncidente:
        query = """
            INSERT INTO tipos_incidente (codigo, cubre_seguro)
            VALUES (?, ?)
        """
        valores = (
            tipo_incidente.codigo,
            int(tipo_incidente.cubre_seguro),
        )
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            tipo_incidente.id_tipo_incidente = cursor.lastrowid
            return tipo_incidente

    def obtener_todos(self) -> list[TipoIncidente]:
        query = "SELECT * FROM tipos_incidente"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            tipo_incidentes = []
            for fila in filas:
                tipo_incidente = TipoIncidente(
                    id_tipo_incidente=fila["id_tipo_incidente"],
                    codigo=fila["codigo"],
                    cubre_seguro=bool(fila["cubre_seguro"]),
                )
                tipo_incidentes.append(tipo_incidente)
            return tipo_incidentes
