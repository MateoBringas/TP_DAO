class Reserva:
    def __init__(self, cliente, vehiculo, empleado, estado_reserva, fecha_reserva, fecha_alquiler, senia_monto=0, actualizado_en=None, id_reserva=None):
        self.id_reserva = id_reserva
        self.cliente_id = cliente
        self.vehiculo_id = vehiculo
        self.empleado_id = empleado
        self.estado_reserva_id = estado_reserva
        self.fecha_reserva = fecha_reserva
        self.fecha_alquiler = fecha_alquiler
        self.senia_monto = senia_monto
        self.actualizado_en = actualizado_en

    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "cliente_id": self.cliente_id,
            "vehiculo_id": self.vehiculo_id,
            "empleado_id": self.empleado_id,
            "estado_reserva_id": self.estado_reserva_id,
            "fecha_reserva": self.fecha_reserva,
            "fecha_alquiler": self.fecha_alquiler,
            "senia_monto": self.senia_monto,
            "actualizado_en": self.actualizado_en,
        }
    
    @classmethod
    def from_dict(cls, data, cliente=None, vehiculo=None, empleado=None, estado_reserva=None):
        return cls(
            cliente=cliente,
            vehiculo=vehiculo,
            empleado=empleado,
            estado_reserva=estado_reserva,
            fecha_reserva=data.get("fecha_reserva"),
            fecha_alquiler=data.get("fecha_alquiler"),
            senia_monto=data.get("senia_monto", 0),
            actualizado_en=data.get("actualizado_en"),
            id_reserva=data.get("id_reserva")
        )
