class Incidente:
    def __init__( self, alquiler, empleado, tipo_incidente, estado_incidente, fecha, descripcion, costo=0, id_incidente=None):
        self.id_incidente = id_incidente
        self.alquiler = alquiler
        self.empleado = empleado
        self.tipo_incidente = tipo_incidente
        self.estado_incidente = estado_incidente
        self.fecha = fecha
        self.descripcion = descripcion
        self.costo = costo

    def to_dict(self):
        return {
            "id_incidente": self.id_incidente,
            "alquiler_id": self.alquiler.id_alquiler if self.alquiler else None,
            "empleado_id": self.empleado.id_empleado if self.empleado else None,
            "tipo_incidente": self.tipo_incidente.id_tipo_incidente if self.tipo_incidente else None,
            "estado_incidente": self.estado_incidente if self.estado_incidente else None,
            "fecha": self.fecha,
            "descripcion": self.descripcion,
            "costo": self.costo,
        }

    @classmethod
    def from_dict(cls, data, alquiler=None, empleado=None, tipo_incidente=None, estado_incidente=None):
        return cls(
            alquiler=alquiler,
            empleado=empleado,
            tipo_incidente=tipo_incidente,
            estado_incidente=estado_incidente,
            fecha=data.get("fecha"),
            descripcion=data.get("descripcion"),
            costo=data.get("costo", 0),
            id_incidente=data.get("id_incidente"),
        )
