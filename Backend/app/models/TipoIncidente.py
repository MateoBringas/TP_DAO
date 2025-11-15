class TipoIncidente:
    def __init__( self, codigo, cubre_seguro, id_tipo_incidente=None ):
        self.id_tipo_incidente = id_tipo_incidente
        self.codigo = codigo
        self.cubre_seguro = cubre_seguro

    def to_dict(self):
        return {
            "id_tipo_incidente": self.id_tipo_incidente,
            "codigo": self.codigo,
            "cubre_seguro": self.cubre_seguro,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            codigo=data.get("codigo"),
            cubre_seguro=data.get("cubre_seguro"),
            id_tipo_incidente=data.get("id_tipo_incidente"),
        )
