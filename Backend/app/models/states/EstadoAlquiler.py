class EstadoAlquiler:
    def __init__(self, codigo, id_estado_alquiler=None):
        self.id_estado_alquiler = id_estado_alquiler
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