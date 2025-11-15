from app.database.database import get_connection
from app.models.Pago import Pago


class PagoRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    # CREATE
    def crear(self, pago: Pago) -> Pago:
        query = """
            INSERT INTO pagos (
                alquiler_id,
                empleado_id,
                metodo,
                fecha_pago,
                monto,
                descripcion,
                actualizado_en
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            pago.alquiler.id_alquiler if pago.alquiler else None,
            pago.empleado.id_empleado if pago.empleado else None,
            pago.metodo,
            pago.fecha,
            pago.monto,
            pago.descripcion,
            pago.actualizado_en,
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            pago.id_pago = cursor.lastrowid  # guardar el ID generado
            return pago

    # READ: obtener todos
    def obtener_todos(self) -> list[Pago]:
        query = "SELECT * FROM pagos"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            pagos: list[Pago] = []

            for fila in filas:
                pago = Pago(
                    id_pago=fila["id_pago"],
                    alquiler=None,   # luego podés cargar el alquiler con otro repo
                    empleado=None,   # idem empleado
                    metodo=fila["metodo"],
                    fecha=fila["fecha_pago"],
                    monto=fila["monto"],
                    descripcion=fila["descripcion"],
                    actualizado_en=fila["actualizado_en"],
                )
                pagos.append(pago)

            return pagos
