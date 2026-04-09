"""
JWT Handler
===========

Maneja la creación y verificación de tokens JWT.

¿Qué hace este archivo?
1. Generar tokens JWT (cuando el usuario hace login)
2. Verificar tokens JWT (cuando el usuario accede a rutas protegidas)
"""

import jwt
import datetime
import sys
import os
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS


class JWTHandler:
    """
    Clase para manejar tokens JWT
    """

    @staticmethod
    def generate_token(user_id: int, email: str, role: str) -> str:
        """
        Genera un token JWT para un usuario

        ¿Qué hace?
        1. Recibe user_id y email
        2. Calcula fecha de expiración (ahora + 1 hora)
        3. Crea un paquete de información (payload)
        4. Encripta el payload con la clave secreta
        5. Retorna el token encriptado

        Args:
            user_id: ID del usuario
            email: Email del usuario
            role: Rol del usuario (user, admin)

        Returns:
            str: Token JWT (texto largo encriptado)

        Ejemplo:
            token = JWTHandler.generate_token(5, "juan@email.com")
            # Retorna: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        """

        # 1. Calcular cuándo expira el token (ahora + 24 horas)
        expiration_time = datetime.datetime.utcnow(
        ) + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)

        # 2. Crear el "paquete" de información (payload)
        payload = {
            'user_id': user_id,        # ID del usuario
            'email': email,            # Email del usuario
            'role': role,
            'exp': expiration_time,    # Cuándo expira
            'iat': datetime.datetime.utcnow()  # Cuándo se creó
        }

        # 3. Encriptar el payload con la clave secreta
        token = jwt.encode(
            payload,           # La información
            JWT_SECRET_KEY,    # La clave secreta (password)
            algorithm=JWT_ALGORITHM  # Método de encriptación
        )

        # 4. Retornar el token
        return token

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verifica si un token JWT es válido

        ¿Qué hace?
        1. Recibe el token encriptado
        2. Intenta desencriptarlo con la clave secreta
        3. Verifica que no haya expirado
        4. Retorna la información del usuario

        Args:
            token: Token JWT a verificar

        Returns:
            dict: Información del usuario (user_id, email)

        Raises:
            Exception: Si el token es inválido o expiró

        Ejemplo:
            payload = JWTHandler.verify_token("eyJhbGci...")
            # Retorna: {'user_id': 5, 'email': 'juan@email.com', ...}
        """

        try:
            # Intentar desencriptar el token
            payload = jwt.decode(
                token,              # El token encriptado
                JWT_SECRET_KEY,     # La clave secreta
                algorithms=[JWT_ALGORITHM]  # Método de encriptación
            )

            # Si llegó aquí, el token es válido
            return payload

        except jwt.ExpiredSignatureError:
            # El token expiró (pasaron más de 24 horas)
            raise Exception("Token expired. Please login again.")

        except jwt.InvalidTokenError:
            # El token es inválido (fue modificado o está corrupto)
            raise Exception("Invalid token. Please login again.")
