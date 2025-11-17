"""
Ejemplos prácticos de uso de conceptos de POO implementados.

Este archivo demuestra cómo usar los patrones y conceptos de POO
aplicados en el sistema de gestión de alquileres.
"""

from datetime import datetime, timedelta
from app.models.strategies.TarifaStrategy import (
    TarifaSimple,
    TarifaConDescuentoSemanal,
    TarifaPorKilometraje,
    TarifaPremium,
    CalculadoraTarifa
)
from app.models.factories.TarifaFactory import TarifaFactory


def ejemplo_strategy_pattern():
    """
    Demuestra el uso del Strategy Pattern para cálculo de tarifas.

    CONCEPTO POO: Strategy Pattern + Polimorfismo
    """
    print("\n" + "="*60)
    print("EJEMPLO 1: STRATEGY PATTERN - Cálculo de Tarifas")
    print("="*60)

    # Datos del alquiler
    tarifa_base = 8000  # $8000 por día
    fecha_inicio = datetime(2025, 1, 15)
    fecha_fin = datetime(2025, 1, 25)  # 10 días
    km_recorridos = 500

    print(f"\nDatos del alquiler:")
    print(f"  - Tarifa base: ${tarifa_base}/día")
    print(f"  - Duración: 10 días")
    print(f"  - Kilómetros recorridos: {km_recorridos} km")

    # 1. Estrategia Simple
    print("\n--- Estrategia Simple ---")
    calculadora = CalculadoraTarifa(TarifaSimple())
    monto = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin)
    print(f"Monto: ${monto}")

    # 2. Estrategia con Descuento Semanal
    print("\n--- Estrategia con Descuento Semanal (10% off) ---")
    calculadora.cambiar_estrategia(TarifaConDescuentoSemanal())
    monto = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin)
    print(f"Monto: ${monto}")

    # 3. Estrategia por Kilometraje
    print("\n--- Estrategia por Kilometraje ($50/km) ---")
    calculadora.cambiar_estrategia(TarifaPorKilometraje(costo_por_km=50))
    monto = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, km_recorridos)
    print(f"Monto: ${monto}")

    # 4. Estrategia Premium
    print("\n--- Estrategia Premium (15% off + $30/km) ---")
    calculadora.cambiar_estrategia(TarifaPremium(costo_por_km=30))
    monto = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, km_recorridos)
    print(f"Monto: ${monto}")

    print("\nPOLIMORFISMO: Misma interfaz calcular(), diferentes implementaciones")


def ejemplo_factory_pattern():
    """
    Demuestra el uso del Factory Pattern.

    CONCEPTO POO: Factory Pattern + Encapsulamiento
    """
    print("\n" + "="*60)
    print("EJEMPLO 2: FACTORY PATTERN - Creación de Estrategias")
    print("="*60)

    # Datos
    tarifa_base = 5000
    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=5)

    print(f"\nCreando estrategias usando el Factory:")

    # Crear estrategias mediante el factory
    tipos = ['simple', 'semanal', 'kilometraje', 'premium']

    for tipo in tipos:
        estrategia = TarifaFactory.crear_estrategia(tipo, costo_por_km=40)
        calculadora = CalculadoraTarifa(estrategia)
        monto = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, 300)
        print(f"  {tipo.capitalize()}: ${monto}")

    print(f"\nTipos disponibles: {TarifaFactory.tipos_disponibles()}")
    print("\nENCAPSULAMIENTO: La lógica de creación está oculta en el Factory")


def ejemplo_polimorfismo():
    """
    Demuestra polimorfismo con diferentes estrategias.

    CONCEPTO POO: Polimorfismo
    """
    print("\n" + "="*60)
    print("EJEMPLO 3: POLIMORFISMO - Diferentes Comportamientos")
    print("="*60)

    # Lista de estrategias diferentes
    estrategias = [
        ("Simple", TarifaSimple()),
        ("Descuento Semanal", TarifaConDescuentoSemanal()),
        ("Por Kilometraje", TarifaPorKilometraje(costo_por_km=45)),
        ("Premium", TarifaPremium(costo_por_km=35))
    ]

    tarifa_base = 6000
    fecha_inicio = datetime(2025, 2, 1)
    fecha_fin = datetime(2025, 2, 8)  # 7 días
    km = 400

    print(f"\nProcesando con diferentes estrategias:")
    print(f"(Mismo método calcular(), resultados diferentes)")

    for nombre, estrategia in estrategias:
        monto = estrategia.calcular(tarifa_base, fecha_inicio, fecha_fin, km)
        print(f"  {nombre:20} => ${monto:,.2f}")

    print("\nPOLIMORFISMO: Todas responden a calcular() pero con lógica diferente")


def ejemplo_composicion():
    """
    Demuestra composición con CalculadoraTarifa.

    CONCEPTO POO: Composición (HAS-A)
    """
    print("\n" + "="*60)
    print("EJEMPLO 4: COMPOSICIÓN - CalculadoraTarifa")
    print("="*60)

    print("\nCalculadoraTarifa TIENE-UN TarifaStrategy (composición)")
    print("No ES-UN TarifaStrategy (herencia)")

    # Crear calculadora con estrategia inicial
    calculadora = CalculadoraTarifa(TarifaSimple())
    print(f"\nCalculadora creada con estrategia: TarifaSimple")

    # Cambiar estrategia en tiempo de ejecución
    print("Cambiando estrategia dinámicamente...")
    calculadora.cambiar_estrategia(TarifaPremium())
    print("Nueva estrategia: TarifaPremium")

    print("\nVentaja: Flexibilidad para cambiar comportamiento sin herencia")


def ejemplo_comparacion_alquileres():
    """
    Ejemplo práctico: comparar costos de diferentes tipos de alquiler.

    CONCEPTO POO: Aplicación práctica de todos los patrones
    """
    print("\n" + "="*60)
    print("EJEMPLO 5: CASO PRÁCTICO - Comparación de Alquileres")
    print("="*60)

    # Escenario 1: Alquiler corto (3 días)
    print("\n--- Escenario 1: Alquiler Corto (3 días) ---")
    fecha_inicio = datetime(2025, 3, 1)
    fecha_fin = datetime(2025, 3, 4)
    tarifa_base = 7000
    km = 150

    calculadora = CalculadoraTarifa(TarifaFactory.crear_estrategia('simple'))
    simple = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, km)

    calculadora.cambiar_estrategia(TarifaFactory.crear_estrategia('kilometraje'))
    km_cost = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, km)

    print(f"Tarifa Simple: ${simple:,.2f}")
    print(f"Con Kilometraje: ${km_cost:,.2f}")
    print(f"Diferencia: ${abs(simple - km_cost):,.2f}")

    # Escenario 2: Alquiler largo (10 días)
    print("\n--- Escenario 2: Alquiler Largo (10 días) ---")
    fecha_fin = datetime(2025, 3, 11)
    km = 800

    calculadora.cambiar_estrategia(TarifaFactory.crear_estrategia('simple'))
    simple = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, km)

    calculadora.cambiar_estrategia(TarifaFactory.crear_estrategia('semanal'))
    semanal = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, km)

    calculadora.cambiar_estrategia(TarifaFactory.crear_estrategia('premium'))
    premium = calculadora.calcular_monto(tarifa_base, fecha_inicio, fecha_fin, km)

    print(f"Tarifa Simple: ${simple:,.2f}")
    print(f"Con Descuento Semanal: ${semanal:,.2f} (ahorro: ${simple - semanal:,.2f})")
    print(f"Premium: ${premium:,.2f}")

    print("\nRECOMENDACIÓN: Para 10 días, usar tarifa Premium")


def main():
    """Ejecuta todos los ejemplos."""
    print("\n" + "="*60)
    print("   EJEMPLOS DE CONCEPTOS DE POO - Sistema de Alquileres")
    print("   Materia: Desarrollo de Aplicaciones con Objetos")
    print("="*60)

    ejemplo_strategy_pattern()
    ejemplo_factory_pattern()
    ejemplo_polimorfismo()
    ejemplo_composicion()
    ejemplo_comparacion_alquileres()

    print("\n" + "="*60)
    print("CONCEPTOS DEMOSTRADOS:")
    print("="*60)
    print("[OK] Strategy Pattern")
    print("[OK] Factory Pattern")
    print("[OK] Polimorfismo")
    print("[OK] Composicion (HAS-A)")
    print("[OK] Encapsulamiento")
    print("[OK] Abstraccion (clases abstractas)")
    print("\nPara mas detalles, ver: CONCEPTOS_POO.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
