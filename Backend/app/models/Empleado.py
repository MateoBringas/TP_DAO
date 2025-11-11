class Empleado:
    def __init__(self, nombre, apellido, dni, email, telefono, habilitado=True, id_empleado=None):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.habilitado = habilitado

    def to_dict(self):
        return {
            "id_empleado": self.id_empleado,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "email": self.email,
            "telefono": self.telefono,
            "habilitado": self.habilitado
        }