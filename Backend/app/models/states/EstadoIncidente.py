class EstadoIncidente:
    def __init__(self, codigo, id_estado_incidente=None):
        self.id_estado_incidente = id_estado_incidente
        self.codigo = codigo

    def to_dict(self):
        return {
            "codigo": self.codigo,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            codigo=data.get("codigo"),
        )