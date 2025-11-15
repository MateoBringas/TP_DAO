from app.database.database import get_connection
from app.models.Cliente import Cliente


class ClienteRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def crear(self, cliente: Cliente) -> Cliente:
        query = """
            INSERT INTO clientes (
                dni,
                nombre,
                apellido,
                email,
                telefono,
                direccion,
                licencia_num,
                licencia_venc,
                habilitado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            cliente.dni,
            cliente.nombre,
            cliente.apellido,
            cliente.email,
            cliente.telefono,
            cliente.direccion,
            cliente.licencia_num,
            cliente.licencia_venc,
            int(cliente.habilitado),
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            cliente.id_cliente = cursor.lastrowid
            return cliente

    def obtener_todos(self) -> list[Cliente]:
        query = "SELECT * FROM clientes"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            clientes: list[Cliente] = []

            for fila in filas:
                cliente = Cliente(
                    id_cliente=fila["id_cliente"],
                    dni=fila["dni"],
                    nombre=fila["nombre"],
                    apellido=fila["apellido"],
                    email=fila["email"],
                    telefono=fila["telefono"],
                    direccion=fila["direccion"],
                    licencia_num=fila["licencia_num"],
                    licencia_venc=fila["licencia_venc"],
                    habilitado=bool(fila["habilitado"]),
                )
                clientes.append(cliente)

            return clientes
