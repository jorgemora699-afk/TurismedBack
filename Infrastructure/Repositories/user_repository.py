"""
User Repository Interface (Contrato/Interfaz)
==============================================

Esto es una INTERFAZ (contrato).

¿Qué es una interfaz?
- Define QUÉ operaciones se pueden hacer (guardar, buscar, etc.)
- NO define CÓMO se hacen (eso lo hace la implementación)
- Es como un "contrato" que dice: "quien me implemente, debe tener estos métodos"

¿Por qué usar interfaces?
- Los Use Cases NO conocen si usas PostgreSQL, MongoDB, o archivos
- Solo saben: "necesito guardar un usuario en ALGÚN LUGAR"
- Mañana cambias de PostgreSQL a MongoDB, y los Use Cases siguen igual
"""

from abc import ABC, abstractmethod
from Domain.Entities.user import User
from typing import Optional


class UserRepository(ABC):
    """
    Interfaz del repositorio de usuarios

    Define las operaciones que se pueden hacer con usuarios,
    pero NO dice cómo hacerlas (eso es responsabilidad de la implementación)
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """
        Guarda un usuario en el sistema de persistencia

        Args:
            user: Usuario a guardar

        Returns:
            User: El usuario guardado (con ID asignado si es nuevo)
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por su email

        Args:
            email: Email a buscar

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por su ID

        Args:
            user_id: ID del usuario

        Returns:
            User si existe, None si no existe
        """
        pass

    @abstractmethod
    def email_exists(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado

        Args:
            email: Email a verificar

        Returns:
            True si existe, False si no existe
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Actualiza un usuario existente

        Args:
            user: Usuario con los datos actualizados

        Returns:
            User: Usuario actualizado
        """
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario del sistema

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente
        """
        pass
