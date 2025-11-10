class Vehiculo:
    def __init__(self, patente, marca, modelo, anio, tarifa_base_dia, km_actual=0, habilitado=True, id_vehiculo=None, seguro_venc=None, vtv_venc=None, km_service_cada=None, km_ultimo_service=None, fecha_ultimo_service=None):
        self.id_vehiculo = id_vehiculo
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tarifa_base_dia = tarifa_base_dia
        self.km_actual = km_actual
        self.habilitado = habilitado
        self.seguro_venc = seguro_venc
        self.vtv_venc = vtv_venc
        self.km_service_cada = km_service_cada
        self.km_ultimo_service = km_ultimo_service
        self.fecha_ultimo_service = fecha_ultimo_service

    def to_dict(self):
        return {
            "id_vehiculo": self.id_vehiculo,
            "patente": self.patente,
            "marca": self.marca,
            "modelo": self.modelo,
            "anio": self.anio,
            "tarifa_base_dia": self.tarifa_base_dia,
            "km_actual": self.km_actual,
            "habilitado": self.habilitado,
            "seguro_venc": self.seguro_venc,
            "vtv_venc": self.vtv_venc,
            "km_service_cada": self.km_service_cada,
            "km_ultimo_service": self.km_ultimo_service,
            "fecha_ultimo_service": self.fecha_ultimo_service
        }