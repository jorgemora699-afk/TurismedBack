"""
Use Case: Delete User
=====================

Caso de uso para eliminar un usuario del sistema.

Responsabilidades:
1. Buscar al usuario por ID
2. Verificar que el usuario exista
3. Eliminar el usuario
"""

from Infrastructure.Repositories.user_repository import UserRepository


class DeleteUserUseCase:
    """
    Caso de uso: Eliminar un usuario
    """

    def __init__(self, user_repository: UserRepository):
        """
        Constructor

        Args:
            user_repository: Repositorio para buscar/eliminar usuarios
        """
        self.user_repository = user_repository

    def execute(self, user_id: int) -> bool:
        """
        Ejecuta el caso de uso: eliminar usuario

        Pasos:
        1. Validar que el ID sea válido
        2. Buscar el usuario
        3. Verificar que el usuario exista
        4. Eliminar el usuario
        5. Retornar confirmación

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente

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

        # Paso 4: Eliminar el usuario
        self.user_repository.delete(user_id)

        # Paso 5: Retornar confirmación
        return True
