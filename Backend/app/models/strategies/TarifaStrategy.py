"""
Módulo que implementa el patrón Strategy para cálculo de tarifas.

Conceptos de POO aplicados:
- Strategy Pattern: Diferentes estrategias de cálculo
- Polimorfismo: Cada estrategia implementa calcular() de manera diferente
- Abstracción: Clase abstracta TarifaStrategy
- Composición: Las estrategias se componen con el servicio de alquiler
"""

from abc import ABC, abstractmethod
from datetime import datetime


class TarifaStrategy(ABC):
    """
    Clase abstracta que define la interfaz para estrategias de cálculo de tarifa.

    PATRÓN STRATEGY: Define una familia de algoritmos intercambiables.
    """

    @abstractmethod
    def calcular(self, tarifa_base: float, fecha_inicio: datetime, fecha_fin: datetime, km_recorridos: int = 0) -> float:
        """
        Calcula el monto total del alquiler.

        Args:
            tarifa_base: Tarifa base por día del vehículo
            fecha_inicio: Fecha de inicio del alquiler
            fecha_fin: Fecha de fin del alquiler
            km_recorridos: Kilómetros recorridos (opcional)

        Returns:
            Monto total calculado
        """
        pass


class TarifaSimple(TarifaStrategy):
    """
    Estrategia de tarifa simple: tarifa_base * días.

    POLIMORFISMO: Implementación específica del método calcular()
    """

    def calcular(self, tarifa_base: float, fecha_inicio: datetime, fecha_fin: datetime, km_recorridos: int = 0) -> float:
        """Calcula tarifa multiplicando tarifa base por días."""
        dias = (fecha_fin - fecha_inicio).days
        if dias == 0:
            dias = 1  # Mínimo 1 día
        return tarifa_base * dias


class TarifaConDescuentoSemanal(TarifaStrategy):
    """
    Estrategia con descuento del 10% si el alquiler es de 7 días o más.

    POLIMORFISMO: Implementación diferente del mismo método.
    """

    def calcular(self, tarifa_base: float, fecha_inicio: datetime, fecha_fin: datetime, km_recorridos: int = 0) -> float:
        """Calcula tarifa con descuento semanal."""
        dias = (fecha_fin - fecha_inicio).days
        if dias == 0:
            dias = 1

        monto = tarifa_base * dias

        # Descuento del 10% para alquileres de 7 días o más
        if dias >= 7:
            monto = monto * 0.90  # 10% de descuento

        return round(monto, 2)


class TarifaPorKilometraje(TarifaStrategy):
    """
    Estrategia que incluye costo por kilómetro recorrido.

    POLIMORFISMO: Otra implementación del método calcular()
    """

    def __init__(self, costo_por_km: float = 50.0):
        """
        Constructor de la estrategia.

        Args:
            costo_por_km: Costo adicional por kilómetro recorrido
        """
        self.costo_por_km = costo_por_km

    def calcular(self, tarifa_base: float, fecha_inicio: datetime, fecha_fin: datetime, km_recorridos: int = 0) -> float:
        """Calcula tarifa incluyendo kilometraje."""
        dias = (fecha_fin - fecha_inicio).days
        if dias == 0:
            dias = 1

        # Tarifa base por días
        monto_base = tarifa_base * dias

        # Costo adicional por kilometraje
        costo_km = km_recorridos * self.costo_por_km

        return round(monto_base + costo_km, 2)


class TarifaPremium(TarifaStrategy):
    """
    Estrategia premium: combina descuento semanal + costo por km.

    COMPOSICIÓN: Utiliza lógica de otras estrategias.
    """

    def __init__(self, costo_por_km: float = 30.0):
        """
        Constructor de la estrategia premium.

        Args:
            costo_por_km: Costo por kilómetro (reducido para premium)
        """
        self.costo_por_km = costo_por_km

    def calcular(self, tarifa_base: float, fecha_inicio: datetime, fecha_fin: datetime, km_recorridos: int = 0) -> float:
        """Calcula tarifa premium con todos los beneficios."""
        dias = (fecha_fin - fecha_inicio).days
        if dias == 0:
            dias = 1

        # Tarifa base
        monto = tarifa_base * dias

        # Descuento semanal
        if dias >= 7:
            monto = monto * 0.85  # 15% de descuento (mejor que la estándar)

        # Costo por kilometraje (reducido)
        if km_recorridos > 0:
            monto += km_recorridos * self.costo_por_km

        return round(monto, 2)


class CalculadoraTarifa:
    """
    Contexto que utiliza las estrategias de tarifa.

    PATRÓN STRATEGY: Contexto que delega el cálculo a la estrategia.
    COMPOSICIÓN: Contiene una instancia de TarifaStrategy.
    """

    def __init__(self, estrategia: TarifaStrategy):
        """
        Constructor del calculador.

        Args:
            estrategia: Estrategia de cálculo a utilizar
        """
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: TarifaStrategy):
        """
        Cambia la estrategia de cálculo en tiempo de ejecución.

        POLIMORFISMO: Puede recibir cualquier estrategia que herede de TarifaStrategy.

        Args:
            estrategia: Nueva estrategia a utilizar
        """
        self._estrategia = estrategia

    def calcular_monto(self, tarifa_base: float, fecha_inicio: datetime, fecha_fin: datetime, km_recorridos: int = 0) -> float:
        """
        Calcula el monto usando la estrategia actual.

        Args:
            tarifa_base: Tarifa base del vehículo
            fecha_inicio: Fecha de inicio
            fecha_fin: Fecha de fin
            km_recorridos: Kilómetros recorridos

        Returns:
            Monto calculado por la estrategia
        """
        return self._estrategia.calcular(tarifa_base, fecha_inicio, fecha_fin, km_recorridos)
