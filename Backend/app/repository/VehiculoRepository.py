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
