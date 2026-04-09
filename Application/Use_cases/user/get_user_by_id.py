"""
Use Case: Get User By ID
=========================

Caso de uso para obtener un usuario por su ID.

Responsabilidades:
1. Buscar al usuario por ID
2. Verificar que el usuario exista
3. Retornar el usuario encontrado
"""

from Domain.Entities.user import User
from Infrastructure.Repositories.user_repository import UserRepository


class GetUserByIdUseCase:
    """
    Caso de uso: Obtener un usuario por ID
    """

    def __init__(self, user_repository: UserRepository):
        """
        Constructor

        Args:
            user_repository: Repositorio para buscar usuarios
        """
        self.user_repository = user_repository

    def execute(self, user_id: int) -> User:
        """
        Ejecuta el caso de uso: obtener usuario por ID

        Pasos:
        1. Validar que el ID sea válido
        2. Buscar el usuario en el repositorio
        3. Verificar que el usuario exista
        4. Limpiar información sensible (contraseña)
        5. Retornar el usuario

        Args:
            user_id: ID del usuario a buscar

        Returns:
            User: Usuario encontrado

        Raises:
            ValueError: Si el ID es inválido
            Exception: Si el usuario no existe
        """

        # Paso 1: Validar que el ID sea válido
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")

        # Paso 2: Buscar el usuario
        user = self.user_repository.find_by_id(user_id)

        # Paso 3: Verificar que exista
        if not user:
            raise Exception(f"User with ID {user_id} not found")

        # Paso 4: Limpiar información sensible
        user.password = None

        # Paso 5: Retornar el usuario
        return user
