from app.database.database import get_connection
from app.models.Vehiculo import Vehiculo


class VehiculoRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def crear(self, vehiculo: Vehiculo) -> Vehiculo:
        query = """
            INSERT INTO vehiculos (
                patente,
                marca,
                modelo,
                anio,
                tarifa_base_dia,
                km_actual,
                habilitado,
                seguro_venc,
                vtv_venc,
                km_service_cada,
                km_ultimo_service,
                fecha_ultimo_service,
                foto_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            vehiculo.patente,
            vehiculo.marca,
            vehiculo.modelo,
            vehiculo.anio,
            vehiculo.tarifa_base_dia,
            vehiculo.km_actual,
            int(vehiculo.habilitado),
            vehiculo.seguro_venc,
            vehiculo.vtv_venc,
            vehiculo.km_service_cada,
            vehiculo.km_ultimo_service,
            vehiculo.fecha_ultimo_service,
            vehiculo.foto_url,
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            vehiculo.id_vehiculo = cursor.lastrowid  # guardar el ID generado
            return vehiculo

    def obtener_todos(self) -> list[Vehiculo]:
        query = "SELECT * FROM vehiculos"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            vehiculos: list[Vehiculo] = []
            for fila in filas:
                vehiculo = Vehiculo(
                    id_vehiculo=fila["id_vehiculo"],
                    patente=fila["patente"],
                    marca=fila["marca"],
                    modelo=fila["modelo"],
                    anio=fila["anio"],
                    tarifa_base_dia=fila["tarifa_base_dia"],
                    km_actual=fila["km_actual"],
                    habilitado=bool(fila["habilitado"]),
                    seguro_venc=fila["seguro_venc"],
                    vtv_venc=fila["vtv_venc"],
                    km_service_cada=fila["km_service_cada"],
                    km_ultimo_service=fila["km_ultimo_service"],
                    fecha_ultimo_service=fila["fecha_ultimo_service"],
                    foto_url=fila["foto_url"],
                )
                vehiculos.append(vehiculo)
            return vehiculos

    def obtener_por_id(self, id_vehiculo: int) -> Vehiculo:
        query = "SELECT * FROM vehiculos WHERE id_vehiculo = ?"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id_vehiculo,))
            fila = cursor.fetchone()

            if not fila:
                return None

            return Vehiculo(
                id_vehiculo=fila["id_vehiculo"],
                patente=fila["patente"],
                marca=fila["marca"],
                modelo=fila["modelo"],
                anio=fila["anio"],
                tarifa_base_dia=fila["tarifa_base_dia"],
                km_actual=fila["km_actual"],
                habilitado=bool(fila["habilitado"]),
                seguro_venc=fila["seguro_venc"],
                vtv_venc=fila["vtv_venc"],
                km_service_cada=fila["km_service_cada"],
                km_ultimo_service=fila["km_ultimo_service"],
                fecha_ultimo_service=fila["fecha_ultimo_service"],
                foto_url=fila["foto_url"],
            )

    def actualizar(self, vehiculo: Vehiculo) -> Vehiculo:
        query = """
            UPDATE vehiculos
            SET patente = ?,
                marca = ?,
                modelo = ?,
                anio = ?,
                tarifa_base_dia = ?,
                km_actual = ?,
                habilitado = ?,
                seguro_venc = ?,
                vtv_venc = ?,
                km_service_cada = ?,
                km_ultimo_service = ?,
                fecha_ultimo_service = ?,
                foto_url = ?
            WHERE id_vehiculo = ?
        """
        valores = (
            vehiculo.patente,
            vehiculo.marca,
            vehiculo.modelo,
            vehiculo.anio,
            vehiculo.tarifa_base_dia,
            vehiculo.km_actual,
            int(vehiculo.habilitado),
            vehiculo.seguro_venc,
            vehiculo.vtv_venc,
            vehiculo.km_service_cada,
            vehiculo.km_ultimo_service,
            vehiculo.fecha_ultimo_service,
            vehiculo.foto_url,
            vehiculo.id_vehiculo,
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            return vehiculo

    def obtener_todos_con_estado(self) -> list[dict]:
        """Obtiene todos los vehículos con su estado actual (disponible/alquilado/reservado/mantenimiento)"""
        query = """
            SELECT
                v.*,
                CASE
                    WHEN EXISTS (
                        SELECT 1 FROM mantenimientos m
                        WHERE m.vehiculo_id = v.id_vehiculo
                        AND m.estado_mantenimiento IN ('PROGRAMADO', 'EN_PROGRESO')
                        AND (m.fecha_realizada IS NULL OR date(m.fecha_realizada) >= date('now'))
                    ) THEN 'mantenimiento'
                    WHEN EXISTS (
                        SELECT 1 FROM alquileres a
                        WHERE a.vehiculo_id = v.id_vehiculo
                        AND a.estado_alquiler_id IN (1, 2)
                        AND date(a.fecha_inicio) <= date('now')
                        AND (date(a.fecha_prevista) >= date('now') OR a.fecha_entrega IS NULL)
                    ) THEN 'alquilado'
                    WHEN EXISTS (
                        SELECT 1 FROM reservas r
                        WHERE r.vehiculo_id = v.id_vehiculo
                        AND r.estado_reserva_id IN (1, 2)
                        AND date(r.fecha_alquiler) >= date('now')
                    ) THEN 'reservado'
                    ELSE 'disponible'
                END as estado_actual
            FROM vehiculos v
        """
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            vehiculos_con_estado = []
            for fila in filas:
                vehiculo_dict = {
                    "id_vehiculo": fila["id_vehiculo"],
                    "patente": fila["patente"],
                    "marca": fila["marca"],
                    "modelo": fila["modelo"],
                    "anio": fila["anio"],
                    "tarifa_base_dia": fila["tarifa_base_dia"],
                    "km_actual": fila["km_actual"],
                    "habilitado": bool(fila["habilitado"]),
                    "seguro_venc": fila["seguro_venc"],
                    "vtv_venc": fila["vtv_venc"],
                    "km_service_cada": fila["km_service_cada"],
                    "km_ultimo_service": fila["km_ultimo_service"],
                    "fecha_ultimo_service": fila["fecha_ultimo_service"],
                    "foto_url": fila["foto_url"],
                    "estado_actual": fila["estado_actual"]
                }
                vehiculos_con_estado.append(vehiculo_dict)
            return vehiculos_con_estado
