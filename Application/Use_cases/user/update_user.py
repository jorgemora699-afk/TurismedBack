"""
Use Case: Update User
======================

Caso de uso para actualizar información de un usuario.

Responsabilidades:
1. Buscar al usuario por ID
2. Verificar que el usuario exista
3. Actualizar solo los campos permitidos
4. Validar los nuevos datos
5. Guardar los cambios
"""

from Domain.Entities.user import User
from Infrastructure.Repositories.user_repository import UserRepository


class UpdateUserUseCase:
    """
    Caso de uso: Actualizar un usuario
    """

    def __init__(self, user_repository: UserRepository):
        """
        Constructor

        Args:
            user_repository: Repositorio para buscar/actualizar usuarios
        """
        self.user_repository = user_repository

    def execute(self, user_id: int, name: str = None, email: str = None, phone: str = None) -> User:
        """
        Ejecuta el caso de uso: actualizar usuario

        Pasos:
        1. Validar que el ID sea válido
        2. Buscar el usuario existente
        3. Verificar que el usuario exista
        4. Actualizar los campos proporcionados
        5. Validar los nuevos datos
        6. Guardar los cambios
        7. Retornar el usuario actualizado

        Args:   
            user_id: ID del usuario a actualizar
            name: Nuevo nombre (opcional)
            Email: Nuevo Email (opcional)
            phone: Nuevo teléfono (opcional)

        Returns:
            User: Usuario actualizado

        Raises:
            ValueError: Si el ID es inválido o los datos no son válidos
            Exception: Si el usuario no existe

        Nota:
        - NO se permite cambiar email (es único e inmutable)
        - NO se permite cambiar contraseña (usar endpoint específico)
        """

        # Paso 1: Validar que el ID sea válido
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")

        # Paso 2: Buscar el usuario existente
        user = self.user_repository.find_by_id(user_id)

        # Paso 3: Verificar que exista
        if not user:
            raise Exception(f"User with ID {user_id} not found")

        # Paso 4: Actualizar solo los campos proporcionados
        # Si no se proporciona un campo, mantener el valor actual
        if name is not None:
            user.name = name.strip()

        if email is not None:
            email_clean = email.strip()

            existing_user = self.user_repository.find_by_email(email_clean)

            if existing_user and existing_user.id != user_id:
                raise ValueError(
                    f"Email '{email}' is already in use by another user")

            user.email = email_clean

        if phone is not None:
            user.phone = phone.strip() if phone else None

        user.validate()

        # Paso 6: Actualizar en el repositorio
        updated_user = self.user_repository.update(user)

        # Paso 7: Limpiar información sensible y retornar
        updated_user.password = None

        return updated_user
