class Alquiler: #Posible mejora: Crear una clase Abstracta para manejar los create y actualizado.
    def __init__(self, cliente, vehiculo, empleado, estado_alquiler, creado_en, reserva=None, fecha_inicio=None, fecha_fin=None, km_inicio=0, km_fin=None, monto_total=0, observaciones=None, actualizado_en=None, id_alquiler=None ):
        self.id_alquiler = id_alquiler
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.empleado = empleado
        self.reserva = reserva
        self.estado_alquiler = estado_alquiler
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.km_inicio = km_inicio
        self.km_fin = km_fin
        self.monto_total = monto_total #Tener en cuenta las infracciones si no las cubre el seguro.
        self.observaciones = observaciones,
        self.creado_en = creado_en,
        self.actualizado_en = actualizado_en

    def to_dict(self):
        return {
            "id_alquiler": self.id_alquiler,
            "cliente_id": self.cliente.id_cliente if self.cliente else None,
            "vehiculo_id": self.vehiculo.id_vehiculo if self.vehiculo else None,
            "empleado_id": self.empleado.id_empleado if self.empleado else None,
            "reserva_id": self.reserva.id_reserva if self.reserva else None,
            "estado_alquiler": self.estado_alquiler if self.estado_alquiler else None,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "km_inicio": self.km_inicio,
            "km_fin": self.km_fin,
            "monto_total": self.monto_total,
            "observaciones": self.observaciones,
            "creado_en": self.creado_en,
            "actualizado_en": self.actualizado_en,
        }

    @classmethod
    def from_dict(cls, data, cliente=None, vehiculo=None, empleado=None, reserva=None):
        return cls(
            cliente=cliente,
            vehiculo=vehiculo,
            empleado=empleado,
            reserva=reserva,
            estado_alquiler_id=data.get("estado_alquiler_id"),
            fecha_inicio=data.get("fecha_inicio"),
            fecha_fin=data.get("fecha_fin"),
            km_inicio=data.get("km_inicio", 0),
            km_fin=data.get("km_fin"),
            monto_total=data.get("monto_total", 0),
            observaciones=data.get("observaciones"),
            creado_en=data.get("creado_en"),
            actualizado_en=data.get("actualizado_en"),
            id_alquiler=data.get("id_alquiler"),
        )
