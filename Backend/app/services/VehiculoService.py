from app.models.Vehiculo import Vehiculo
from app.repository.VehiculoRepository import (
    crear_vehiculo,
    obtener_todos_vehiculos
)

#Reglas de negocio relacionadas con Vehiculo

def crear_vehiculo_service(data: dict):
    "Crea un nuevo vehículo a partir de un diccionario con sus datos."
    required_fields = ["patente", "marca", "modelo", "anio", "tarifa_base_dia", "km_actual", "habilitado", "seguro_venc", "vtv_venc", "km_service_cada", "km_ultimo_service", "fecha_ultimo_service"]

    # Validación básica
    for campo in required_fields:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    # Crear instancia de Vehiculo
    vehiculo = Vehiculo(
        patente=data["patente"],
        marca=data["marca"],
        modelo=data["modelo"],
        anio=data["anio"],
        tarifa_base_dia=data["tarifa_base_dia"],
        km_actual=data.get("km_actual", 0),
        habilitado=data.get("habilitado", True),
        seguro_venc=data.get("seguro_venc"),
        vtv_venc=data.get("vtv_venc"),
        km_service_cada=data.get("km_service_cada"),
        km_ultimo_service=data.get("km_ultimo_service"),
        fecha_ultimo_service=data.get("fecha_ultimo_service")
    )

    # Insertar en la base
    return crear_vehiculo(vehiculo)


def obtener_todos_vehiculos_service():
    "Devuelve todos los vehículos."
    vehiculos = obtener_todos_vehiculos()
    return vehiculos