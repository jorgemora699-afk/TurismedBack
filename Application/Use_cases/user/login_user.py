"""
Use Case: Login User
=====================

Caso de uso para autenticar (hacer login) a un usuario.

Responsabilidades:
1. Buscar al usuario por email
2. Verificar que el usuario exista
3. Verificar que la contraseña sea correcta
4. Retornar el usuario autenticado
"""

import bcrypt
from Domain.Entities.user import User
from Infrastructure.Repositories.user_repository import UserRepository
from typing import Optional


class LoginUserUseCase:
    """
    Caso de uso: Autenticar un usuario
    """

    def __init__(self, user_repository: UserRepository):
        """
        Constructor

        Args:
            user_repository: Repositorio para buscar usuarios
        """
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> User:
        """
        Ejecuta el caso de uso: hacer login

        Pasos:
        1. Normalizar el email (lowercase, trim)
        2. Buscar el usuario por email
        3. Verificar que el usuario exista
        4. Verificar que la contraseña sea correcta
        5. Retornar el usuario autenticado

        Args:
            email: Email del usuario
            password: Contraseña en texto plano

        Returns:
            User: Usuario autenticado

        Raises:
            Exception: Si las credenciales son inválidas
        """

        # Paso 1: Normalizar el email
        email_normalized = email.strip().lower()

        # Paso 2 y 3: Buscar el usuario y verificar que exista
        user = self.user_repository.find_by_email(email_normalized)

        if not user:
            # NO decir "email no existe" por seguridad
            # Alguien podría usar esto para descubrir emails registrados
            raise Exception("Invalid email or password")

        # Paso 4: Verificar la contraseña
        # bcrypt.checkpw compara:
        # - password: contraseña en texto plano que el usuario ingresó
        # - user.password: contraseña encriptada guardada en BD
        stored_password = user.password.encode('utf-8')
        password_bytes = password.encode('utf-8')

        is_password_correct = bcrypt.checkpw(password_bytes, stored_password)

        if not is_password_correct:
            # Mismo mensaje que arriba por seguridad
            raise Exception("Invalid email or password")

        # Paso 5: Retornar el usuario autenticado
        # IMPORTANTE: Antes de retornar, limpiar la contraseña
        # para que no se envíe al frontend
        user.password = None  # Nunca enviar la contraseña encriptada

        return user
