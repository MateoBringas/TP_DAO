class EstadoMantenimiento:
    def __init__(self, codigo, id_estado_mantenimiento=None):
        self.id_estado_mantenimiento = id_estado_mantenimiento
        self.codigo = codigo

    def to_dict(self):
        return {
            "codigo": self.codigo,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            codigo=data.get("codigo")
        )