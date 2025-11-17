"""
Módulo que implementa jerarquía de clases con herencia.

Conceptos de POO aplicados:
- Herencia: Cliente y Empleado heredan de Persona
- Polimorfismo: Método to_dict() se sobrescribe en cada clase
- Encapsulamiento: Atributos privados con getters/setters
- Abstracción: Clase base Persona con atributos comunes
"""

from abc import ABC, abstractmethod


class Persona(ABC):
    """
    Clase abstracta base para representar una persona.

    HERENCIA: Clase padre de Cliente y Empleado
    ABSTRACCIÓN: No se puede instanciar directamente
    ENCAPSULAMIENTO: Atributos protegidos con _
    """

    def __init__(self, nombre: str, apellido: str, dni: str = None, email: str = None,
                 telefono: str = None, habilitado: bool = True):
        """
        Constructor de Persona.

        Args:
            nombre: Nombre de la persona
            apellido: Apellido de la persona
            dni: DNI (opcional)
            email: Email (opcional)
            telefono: Teléfono (opcional)
            habilitado: Si la persona está habilitada en el sistema
        """
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self._email = email
        self._telefono = telefono
        self._habilitado = habilitado

    # ENCAPSULAMIENTO: Getters y Setters
    @property
    def nombre(self) -> str:
        """Getter del nombre."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Setter del nombre con validación."""
        if not valor or valor.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def apellido(self) -> str:
        """Getter del apellido."""
        return self._apellido

    @apellido.setter
    def apellido(self, valor: str):
        """Setter del apellido con validación."""
        if not valor or valor.strip() == "":
            raise ValueError("El apellido no puede estar vacío")
        self._apellido = valor.strip()

    @property
    def dni(self) -> str:
        """Getter del DNI."""
        return self._dni

    @property
    def email(self) -> str:
        """Getter del email."""
        return self._email

    @property
    def telefono(self) -> str:
        """Getter del teléfono."""
        return self._telefono

    @property
    def habilitado(self) -> bool:
        """Getter de habilitado."""
        return self._habilitado

    def get_nombre_completo(self) -> str:
        """
        Retorna el nombre completo de la persona.

        Returns:
            Nombre completo (nombre + apellido)
        """
        return f"{self._nombre} {self._apellido}"

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Convierte la persona a diccionario.

        POLIMORFISMO: Cada subclase implementa su versión.

        Returns:
            Diccionario con los datos de la persona
        """
        pass

    @abstractmethod
    def get_tipo(self) -> str:
        """
        Retorna el tipo de persona.

        POLIMORFISMO: Cada subclase retorna su tipo específico.

        Returns:
            Tipo de persona ('Cliente', 'Empleado', etc.)
        """
        pass

    def __str__(self) -> str:
        """
        Representación en string de la persona.

        Returns:
            String descriptivo
        """
        return f"{self.get_tipo()}: {self.get_nombre_completo()}"

    def __repr__(self) -> str:
        """
        Representación técnica de la persona.

        Returns:
            String con información técnica
        """
        return f"<{self.get_tipo()} {self._nombre} {self._apellido}>"
