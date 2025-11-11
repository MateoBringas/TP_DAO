class Mantenimiento:
    def __init__(self, vehiculo, empleado, estado_mantenimiento, tipo, fecha_programada=None, fecha_realizada=None, km=0, costo=0, notas=None, id_mantenimiento=None):
        self.id_mantenimiento = id_mantenimiento
        self.vehiculo = vehiculo
        self.empleado = empleado
        self.estado_mantenimiento = estado_mantenimiento
        self.tipo = tipo
        self.fecha_programada = fecha_programada
        self.fecha_realizada = fecha_realizada
        self.km = km
        self.costo = costo
        self.notas = notas

    def to_dict(self):
        return {
            "id_mantenimiento": self.id_mantenimiento,
            "vehiculo_id": self.vehiculo.id_vehiculo if self.vehiculo else None,
            "empleado_id": self.empleado.id_empleado if self.empleado else None,
            "estado_mantenimiento": self.estado_mantenimiento if self.estado_mantenimiento else None,
            "tipo": self.tipo,
            "fecha_programada": self.fecha_programada,
            "fecha_realizada": self.fecha_realizada,
            "km": self.km,
            "costo": self.costo,
            "notas": self.notas,
        }

    @classmethod
    def from_dict(cls, data, vehiculo=None, empleado=None, estado_mantenimiento=None):
        return cls(
            vehiculo=vehiculo,
            empleado=empleado,
            estado_mantenimiento=estado_mantenimiento,
            tipo=data.get("tipo"),
            fecha_programada=data.get("fecha_programada"),
            fecha_realizada=data.get("fecha_realizada"),
            km=data.get("km", 0),
            costo=data.get("costo", 0),
            notas=data.get("notas"),
            id_mantenimiento=data.get("id_mantenimiento")
        )
