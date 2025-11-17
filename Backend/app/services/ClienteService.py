from app.models.Cliente import Cliente
from app.repository.ClienteRepository import ClienteRepository

# Reglas de negocio relacionadas con Cliente

def crear_cliente_service(data: dict):
    """Crea un nuevo cliente a partir de un diccionario con sus datos."""
    required_fields = ["nombre", "apellido", "email", "telefono", "licencia_num", "licencia_venc"]

    # Validación básica
    for campo in required_fields:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    # Crear instancia de Cliente
    cliente = Cliente(
        dni=data.get("dni"),
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        telefono=data["telefono"],
        direccion=data.get("direccion"),
        licencia_num=data["licencia_num"],
        licencia_venc=data["licencia_venc"],
        habilitado=data.get("habilitado", True)
    )

    # Insertar en la base
    repo = ClienteRepository()
    return repo.crear(cliente)


def obtener_todos_clientes_service():
    """Devuelve todos los clientes."""
    repo = ClienteRepository()
    return repo.obtener_todos()


def obtener_cliente_por_id_service(id_cliente: int):
    """Obtiene un cliente por su ID."""
    repo = ClienteRepository()
    return repo.obtener_por_id(id_cliente)


def actualizar_cliente_service(id_cliente: int, data: dict):
    """Actualiza un cliente existente."""
    required_fields = ["nombre", "apellido", "email", "telefono", "licencia_num", "licencia_venc"]

    for campo in required_fields:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    cliente = Cliente(
        dni=data.get("dni"),
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        telefono=data["telefono"],
        direccion=data.get("direccion"),
        licencia_num=data["licencia_num"],
        licencia_venc=data["licencia_venc"],
        habilitado=data.get("habilitado", True)
    )

    repo = ClienteRepository()
    return repo.actualizar(id_cliente, cliente)


def eliminar_cliente_service(id_cliente: int):
    """Elimina un cliente por su ID."""
    repo = ClienteRepository()
    return repo.eliminar(id_cliente)
