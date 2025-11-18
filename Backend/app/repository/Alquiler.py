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
                estado_alquiler_id,
                fecha_inicio,
                fecha_prevista,
                fecha_entrega,
                km_salida,
                km_entrada,
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
            data["estado_alquiler_id"],
            data["fecha_inicio"],
            data["fecha_prevista"],
            data["fecha_entrega"],
            data["km_salida"],
            data["km_entrada"],
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

    def obtener_todos(self) -> list[dict]:
        """Obtiene todos los alquileres con información completa de cliente y vehículo"""
        query = """
            SELECT
                a.*,
                c.nombre as cliente_nombre,
                c.apellido as cliente_apellido,
                c.dni as cliente_dni,
                v.patente as vehiculo_patente,
                v.marca as vehiculo_marca,
                v.modelo as vehiculo_modelo,
                ea.codigo as estado_nombre
            FROM alquileres a
            LEFT JOIN clientes c ON a.cliente_id = c.id_cliente
            LEFT JOIN vehiculos v ON a.vehiculo_id = v.id_vehiculo
            LEFT JOIN estados_alquiler ea ON a.estado_alquiler_id = ea.id_estado_alquiler
            ORDER BY a.fecha_inicio DESC
        """
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            alquileres = []

            for fila in filas:
                alquiler_dict = {
                    "id_alquiler": fila["id_alquiler"],
                    "cliente_id": fila["cliente_id"],
                    "cliente_nombre_completo": f"{fila['cliente_nombre']} {fila['cliente_apellido']}" if fila['cliente_nombre'] else "N/A",
                    "cliente_dni": fila["cliente_dni"],
                    "vehiculo_id": fila["vehiculo_id"],
                    "vehiculo_descripcion": f"{fila['vehiculo_marca']} {fila['vehiculo_modelo']} - {fila['vehiculo_patente']}" if fila['vehiculo_marca'] else "N/A",
                    "empleado_id": fila["empleado_id"],
                    "estado_alquiler_id": fila["estado_alquiler_id"],
                    "estado_nombre": fila["estado_nombre"],
                    "reserva_id": fila["reserva_id"],
                    "fecha_inicio": fila["fecha_inicio"],
                    "fecha_prevista": fila["fecha_prevista"],
                    "fecha_entrega": fila["fecha_entrega"],
                    "km_salida": fila["km_salida"],
                    "km_entrada": fila["km_entrada"],
                    "observaciones": fila["observaciones"],
                    "creado_en": fila["creado_en"],
                    "actualizado_en": fila["actualizado_en"]
                }
                alquileres.append(alquiler_dict)

            return alquileres

    def obtener_por_id(self, id_alquiler: int):
        query = "SELECT * FROM alquileres WHERE id_alquiler = ?"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_alquiler,))
            fila = cursor.fetchone()

            if not fila:
                return None

            return Alquiler(
                cliente=fila["cliente_id"],
                vehiculo=fila["vehiculo_id"],
                empleado=fila["empleado_id"],
                estado_alquiler=fila["estado_alquiler_id"],
                creado_en=fila["creado_en"],
                reserva=fila["reserva_id"],
                fecha_inicio=fila["fecha_inicio"],
                fecha_prevista=fila["fecha_prevista"],
                fecha_entrega=fila["fecha_entrega"],
                km_salida=fila["km_salida"],
                km_entrada=fila["km_entrada"],
                observaciones=fila["observaciones"],
                actualizado_en=fila["actualizado_en"],
                id_alquiler=fila["id_alquiler"],
            )

    def actualizar(self, id_alquiler: int, alquiler: Alquiler):
        data = alquiler.to_dict()
        query = """
            UPDATE alquileres SET
                cliente_id = ?,
                vehiculo_id = ?,
                empleado_id = ?,
                estado_alquiler_id = ?,
                fecha_inicio = ?,
                fecha_prevista = ?,
                fecha_entrega = ?,
                km_salida = ?,
                km_entrada = ?,
                observaciones = ?,
                actualizado_en = CURRENT_TIMESTAMP
            WHERE id_alquiler = ?
        """
        valores = (
            data["cliente_id"],
            data["vehiculo_id"],
            data["empleado_id"],
            data["estado_alquiler_id"],
            data["fecha_inicio"],
            data["fecha_prevista"],
            data["fecha_entrega"],
            data["km_salida"],
            data["km_entrada"],
            data["observaciones"],
            id_alquiler
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            alquiler.id_alquiler = id_alquiler
            return alquiler

    def eliminar(self, id_alquiler: int) -> bool:
        query = "DELETE FROM alquileres WHERE id_alquiler = ?"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_alquiler,))
            conn.commit()
            return cursor.rowcount > 0

    def verificar_disponibilidad(self, vehiculo_id: int, fecha_inicio: str, fecha_prevista: str, excluir_alquiler_id: int = None) -> bool:
        """
        Verifica si un vehículo está disponible en un rango de fechas.
        Retorna True si está disponible, False si ya está alquilado.
        """
        query = """
            SELECT COUNT(*) as count FROM alquileres
            WHERE vehiculo_id = ?
            AND (
                -- El nuevo período se solapa con alquileres existentes
                (fecha_inicio <= ? AND (fecha_entrega IS NULL OR fecha_entrega >= ?))
                OR (fecha_inicio >= ? AND fecha_inicio <= ?)
            )
            AND estado_alquiler_id IN (1, 2)  -- PENDIENTE o ACTIVO
        """

        params = [vehiculo_id, fecha_prevista, fecha_inicio, fecha_inicio, fecha_prevista]

        # Si estamos actualizando un alquiler, excluir ese registro de la verificación
        if excluir_alquiler_id:
            query += " AND id_alquiler != ?"
            params.append(excluir_alquiler_id)

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result["count"] == 0  # True si no hay conflictos
