"""
Use Case: Register User
========================

Este es un CASO DE USO (Use Case).

¿Qué es un Use Case?
- Define UNA funcionalidad específica del sistema
- Contiene la LÓGICA DE NEGOCIO de esa funcionalidad
- Coordina entre Entities y Repositories
- NO conoce nada sobre HTTP, JSON, Flask, PostgreSQL (detalles técnicos)

Este Use Case específico:
- Registra un nuevo usuario en el sistema
- Valida que los datos sean correctos
- Verifica que el email no exista
- Encripta la contraseña
- Guarda el usuario
"""

import bcrypt
from Domain.Entities.user import User
from Infrastructure.Repositories.user_repository import UserRepository
from config import ADMIN_EMAILS


class RegisterUserUseCase:
    """
    Caso de uso: Registrar un nuevo usuario
    """

    def __init__(self, user_repository: UserRepository):
        """
        Constructor

        Args:
            user_repository: Repositorio para guardar/buscar usuarios
                            (NO sabe si es PostgreSQL, MongoDB, etc.)
        """
        self.user_repository = user_repository

    def execute(self, name: str, email: str, password: str, phone: str = None) -> User:
        """
        Ejecuta el caso de uso: registrar un usuario

        Pasos:
        1. Crear la entidad User con los datos proporcionados
        2. Validar que el usuario cumpla las reglas de negocio
        3. Verificar que el email no exista en el sistema
        4. Encriptar la contraseña
        5. Guardar el usuario
        6. Retornar el usuario guardado

        Args:
            name: Nombre del usuario
            email: Email del usuario
            password: Contraseña en texto plano
            phone: Teléfono (opcional)

        Returns:
            User: Usuario registrado (con ID asignado)

        Raises:
            ValueError: Si los datos son inválidos
            Exception: Si el email ya existe
        """

        # ✅ PASO 1: VALIDAR QUE EL EMAIL NO EXISTA
        existing_user = self.user_repository.find_by_email(email)

        if existing_user:
            raise ValueError(f"Email '{email}' is already registered")

        role = 'admin' if email in ADMIN_EMAILS else 'user'

        # Paso 1: Crear la entidad
        user = User(
            name=name.strip(),
            email=email.strip().lower(),
            password=password,
            phone=phone.strip() if phone else None,
            role=role
        )

        # Paso 2: Validar la entidad (reglas de negocio)
        user.validate()

        # Paso 3: Verificar que el email no exista
        if self.user_repository.email_exists(user.email):
            raise Exception(f"Email '{user.email}' is already registered")

        # Paso 4: Encriptar la contraseña
        # IMPORTANTE: NUNCA guardar contraseñas en texto plano
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
        user.password = hashed_password.decode('utf-8')

        # Paso 5: Guardar el usuario en el repositorio
        # (NO sabemos si es PostgreSQL, MongoDB, etc.)
        saved_user = self.user_repository.save(user)

        # Paso 6: Retornar el usuario guardado
        return saved_user
