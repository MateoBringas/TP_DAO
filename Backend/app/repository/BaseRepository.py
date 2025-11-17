"""
Módulo que implementa el patrón Repository Base Abstracto.

Conceptos de POO aplicados:
- Herencia: Clase base para todos los repositorios
- Abstracción: Métodos abstractos que deben implementar las subclases
- Polimorfismo: Cada subclase implementa los métodos de manera específica
- Encapsulamiento: La conexión a BD está encapsulada
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from app.database.database import get_connection

T = TypeVar('T')  # Tipo genérico para el modelo


class BaseRepository(ABC, Generic[T]):
    """
    Clase abstracta base para todos los repositorios.

    Implementa el patrón Repository + Herencia.
    Las subclases deben implementar los métodos abstractos.
    """

    def __init__(self, connection_factory=get_connection):
        """
        Constructor que inicializa la factory de conexiones.

        Args:
            connection_factory: Factory para crear conexiones a la BD
        """
        self._connection_factory = connection_factory

    @abstractmethod
    def crear(self, entidad: T) -> T:
        """
        Crea una nueva entidad en la base de datos.

        Args:
            entidad: Objeto del modelo a crear

        Returns:
            La entidad creada con su ID asignado
        """
        pass

    @abstractmethod
    def obtener_todos(self) -> List[T]:
        """
        Obtiene todas las entidades de la base de datos.

        Returns:
            Lista de entidades
        """
        pass

    @abstractmethod
    def obtener_por_id(self, id_entidad: int) -> Optional[T]:
        """
        Obtiene una entidad por su ID.

        Args:
            id_entidad: ID de la entidad a buscar

        Returns:
            La entidad encontrada o None si no existe
        """
        pass

    @abstractmethod
    def actualizar(self, id_entidad: int, entidad: T) -> T:
        """
        Actualiza una entidad existente.

        Args:
            id_entidad: ID de la entidad a actualizar
            entidad: Objeto con los nuevos datos

        Returns:
            La entidad actualizada
        """
        pass

    @abstractmethod
    def eliminar(self, id_entidad: int) -> bool:
        """
        Elimina una entidad por su ID.

        Args:
            id_entidad: ID de la entidad a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass

    def ejecutar_query(self, query: str, parametros: tuple = None):
        """
        Método auxiliar para ejecutar queries.
        Demuestra encapsulamiento de la lógica de conexión.

        Args:
            query: SQL query a ejecutar
            parametros: Parámetros de la query

        Returns:
            Cursor con los resultados
        """
        with self._connection_factory() as conn:
            cursor = conn.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            return cursor
