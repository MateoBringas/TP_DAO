class Cliente:
    def __init__(self, dni, nombre, apellido, email, telefono, direccion, licencia_num, licencia_venc=None, habilitado=True, id_cliente=None):
        self.id_cliente = id_cliente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.licencia_num = licencia_num #Opcional
        self.licencia_venc = licencia_venc #Cuando quiera alquilar, hay que validar que no este vencida y que este habilitado.
        self.habilitado = habilitado

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "licencia_num": self.licencia_num,
            "licencia_venc": self.licencia_venc,
            "habilitado": self.habilitado
        }