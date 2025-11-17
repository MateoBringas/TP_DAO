"""
Módulo que implementa el patrón Factory para crear estrategias de tarifa.

Conceptos de POO aplicados:
- Factory Pattern: Crea objetos sin exponer la lógica de creación
- Encapsulamiento: La lógica de creación está centralizada
- Polimorfismo: Retorna diferentes estrategias según el tipo
"""

from app.models.strategies.TarifaStrategy import (
    TarifaStrategy,
    TarifaSimple,
    TarifaConDescuentoSemanal,
    TarifaPorKilometraje,
    TarifaPremium
)


class TarifaFactory:
    """
    Factory para crear estrategias de tarifa.

    PATRÓN FACTORY: Centraliza la creación de objetos de estrategias.
    """

    @staticmethod
    def crear_estrategia(tipo_tarifa: str, **kwargs) -> TarifaStrategy:
        """
        Crea una estrategia de tarifa según el tipo especificado.

        FACTORY METHOD: Crea diferentes objetos según el parámetro.
        POLIMORFISMO: Todas las estrategias cumplen la misma interfaz.

        Args:
            tipo_tarifa: Tipo de estrategia ('simple', 'semanal', 'kilometraje', 'premium')
            **kwargs: Parámetros adicionales para la estrategia

        Returns:
            Instancia de TarifaStrategy

        Raises:
            ValueError: Si el tipo de tarifa no es válido
        """
        tipo_tarifa = tipo_tarifa.lower()

        if tipo_tarifa == 'simple':
            return TarifaSimple()

        elif tipo_tarifa == 'semanal':
            return TarifaConDescuentoSemanal()

        elif tipo_tarifa == 'kilometraje':
            costo_km = kwargs.get('costo_por_km', 50.0)
            return TarifaPorKilometraje(costo_por_km=costo_km)

        elif tipo_tarifa == 'premium':
            costo_km = kwargs.get('costo_por_km', 30.0)
            return TarifaPremium(costo_por_km=costo_km)

        else:
            raise ValueError(f"Tipo de tarifa '{tipo_tarifa}' no válido. "
                           f"Opciones: simple, semanal, kilometraje, premium")

    @staticmethod
    def tipos_disponibles() -> list:
        """
        Retorna los tipos de tarifa disponibles.

        Returns:
            Lista con los nombres de estrategias disponibles
        """
        return ['simple', 'semanal', 'kilometraje', 'premium']


class RepositoryFactory:
    """
    Factory para crear repositorios.

    PATRÓN FACTORY: Centraliza la creación de repositorios.
    """

    @staticmethod
    def crear_repository(tipo_entidad: str):
        """
        Crea un repository según el tipo de entidad.

        Args:
            tipo_entidad: Tipo de entidad ('vehiculo', 'cliente', 'alquiler', etc.)

        Returns:
            Instancia del repository correspondiente

        Raises:
            ValueError: Si el tipo no es válido
        """
        tipo_entidad = tipo_entidad.lower()

        if tipo_entidad == 'vehiculo':
            from app.repository.VehiculoRepository import VehiculoRepository
            return VehiculoRepository()

        elif tipo_entidad == 'cliente':
            from app.repository.ClienteRepository import ClienteRepository
            return ClienteRepository()

        elif tipo_entidad == 'alquiler':
            from app.repository.Alquiler import AlquilerRepository
            return AlquilerRepository()

        elif tipo_entidad == 'reserva':
            from app.repository.ReservaRepository import ReservaRepository
            return ReservaRepository()

        elif tipo_entidad == 'mantenimiento':
            from app.repository.MantenimientoRepository import MantenimientoRepository
            return MantenimientoRepository()

        else:
            raise ValueError(f"Tipo de entidad '{tipo_entidad}' no válido")
