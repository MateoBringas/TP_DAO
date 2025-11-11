class Reserva:
    def __init__(self, cliente, vehiculo, empleado, estado_reserva, fecha_reserva, fecha_carga=None, senia_monto=0, actualizado_en=None, id_reserva=None):
        self.id_reserva = id_reserva
        self.cliente_id = cliente
        self.vehiculo_id = vehiculo
        self.empleado_id = empleado
        self.estado_reserva_id = estado_reserva
        self.fecha_reserva = fecha_reserva
        self.fecha_carga = fecha_carga
        self.senia_monto = senia_monto
        self.actualizado_en = actualizado_en

    def to_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "cliente_id": self.cliente.id_cliente if self.cliente else None,
            "vehiculo_id": self.vehiculo.id_vehiculo if self.vehiculo else None,
            "empleado_id": self.empleado.id_empleado if self.empleado else None,
            "estado_reserva": self.estado_reserva if self.estado_reserva else None,
            "fecha_reserva": self.fecha_reserva,
            "fecha_carga": self.fecha_carga,
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
            fecha_carga=data.get("fecha_carga"),
            senia_monto=data.get("senia_monto", 0),
            actualizado_en=data.get("actualizado_en"),
            id_reserva=data.get("id_reserva")
        )
