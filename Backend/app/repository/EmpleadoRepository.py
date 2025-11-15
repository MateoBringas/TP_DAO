from app.database.database import get_connection
from app.models.Empleado import Empleado


class EmpleadoRepository:
    def __init__(self, connection_factory=get_connection):
        self._connection_factory = connection_factory

    def crear(self, empleado: Empleado) -> Empleado:
        query = """
            INSERT INTO empleados (
                nombre,
                apellido,
                dni,
                email,
                telefono,
                habilitado
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        valores = (
            empleado.nombre,
            empleado.apellido,
            empleado.dni,
            empleado.email,
            empleado.telefono,
            int(empleado.habilitado),
        )

        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            empleado.id_empleado = cursor.lastrowid
            return empleado

    def obtener_todos(self) -> list[Empleado]:
        query = "SELECT * FROM empleados"
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            filas = cursor.fetchall()
            empleados: list[Empleado] = []

            for fila in filas:
                empleado = Empleado(
                    id_empleado=fila["id_empleado"],
                    nombre=fila["nombre"],
                    apellido=fila["apellido"],
                    dni=fila["dni"],
                    email=fila["email"],
                    telefono=fila["telefono"],
                    habilitado=bool(fila["habilitado"]),
                )
                empleados.append(empleado)

            return empleados
