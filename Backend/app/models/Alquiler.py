class Alquiler: #Posible mejora: Crear una clase Abstracta para manejar los create y actualizado.
    def __init__(self, cliente, vehiculo, empleado, estado_alquiler, creado_en, reserva=None, fecha_inicio=None, fecha_prevista=None, fecha_entrega=None, km_salida=0, km_entrada=None, observaciones=None, actualizado_en=None, id_alquiler=None):
        self.id_alquiler = id_alquiler
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.empleado = empleado
        self.reserva = reserva
        self.estado_alquiler = estado_alquiler
        self.fecha_inicio = fecha_inicio
        self.fecha_prevista = fecha_prevista  # Cambio según DER
        self.fecha_entrega = fecha_entrega    # Cambio según DER
        self.km_salida = km_salida            # Cambio según DER
        self.km_entrada = km_entrada          # Cambio según DER
        self.observaciones = observaciones
        self.creado_en = creado_en
        self.actualizado_en = actualizado_en

    def to_dict(self):
        return {
            "id_alquiler": self.id_alquiler,
            "cliente_id": self.cliente.id_cliente if hasattr(self.cliente, 'id_cliente') else self.cliente,
            "vehiculo_id": self.vehiculo.id_vehiculo if hasattr(self.vehiculo, 'id_vehiculo') else self.vehiculo,
            "empleado_id": self.empleado.id_empleado if hasattr(self.empleado, 'id_empleado') else self.empleado,
            "reserva_id": self.reserva.id_reserva if (self.reserva and hasattr(self.reserva, 'id_reserva')) else self.reserva,
            "estado_alquiler_id": self.estado_alquiler if self.estado_alquiler else None,
            "fecha_inicio": self.fecha_inicio,
            "fecha_prevista": self.fecha_prevista,
            "fecha_entrega": self.fecha_entrega,
            "km_salida": self.km_salida,
            "km_entrada": self.km_entrada,
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
            estado_alquiler=data.get("estado_alquiler_id"),
            fecha_inicio=data.get("fecha_inicio"),
            fecha_prevista=data.get("fecha_prevista"),
            fecha_entrega=data.get("fecha_entrega"),
            km_salida=data.get("km_salida", 0),
            km_entrada=data.get("km_entrada"),
            observaciones=data.get("observaciones"),
            creado_en=data.get("creado_en"),
            actualizado_en=data.get("actualizado_en"),
            id_alquiler=data.get("id_alquiler"),
        )
