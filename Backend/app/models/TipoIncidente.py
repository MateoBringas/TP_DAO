class TipoIncidente:
    def __init__( self, codigo, requiere_monto, afecta_seguro, activo=True, id_tipo_incidente=None ):
        self.id_tipo_incidente = id_tipo_incidente
        self.codigo = codigo
        self.requiere_monto = requiere_monto
        self.afecta_seguro = afecta_seguro
        self.activo = activo

    def to_dict(self):
        return {
            "id_tipo_incidente": self.id_tipo_incidente,
            "codigo": self.codigo,
            "requiere_monto": self.requiere_monto,
            "afecta_seguro": self.afecta_seguro,
            "activo": self.activo,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            codigo=data.get("codigo"),
            requiere_monto=data.get("requiere_monto"),
            afecta_seguro=data.get("afecta_seguro"),
            activo=data.get("activo", True),
            id_tipo_incidente=data.get("id_tipo_incidente"),
        )
