class Pago:
    def __init__( self, alquiler, empleado, metodo, fecha_pago, monto, descripcion=None, actualizado_en=None, id_pago=None ):
        self.id_pago = id_pago
        self.alquiler = alquiler
        self.empleado = empleado
        self.metodo = metodo
        self.fecha_pago = fecha_pago
        self.monto = monto
        self.descripcion = descripcion
        self.actualizado_en = actualizado_en

    def to_dict(self):
        return {
            "id_pago": self.id_pago,
            "alquiler_id": self.alquiler.id_alquiler if self.alquiler else None,
            "empleado_id": self.empleado.id_empleado if self.empleado else None,
            "metodo": self.metodo,
            "fecha_pago": self.fecha_pago,
            "monto": self.monto,
            "descripcion": self.descripcion,
            "actualizado_en": self.actualizado_en,
        }

    @classmethod
    def from_dict(cls, data, alquiler=None, empleado=None):
        return cls(
            alquiler=alquiler,
            empleado=empleado,
            metodo=data.get("metodo"),
            fecha_pago=data.get("fecha_pago"),
            monto=data.get("monto"),
            descripcion=data.get("descripcion"),
            actualizado_en=data.get("actualizado_en"),
            id_pago=data.get("id_pago"),
        )
