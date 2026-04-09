"""
Entity: User
============
Esta es una ENTIDAD PURA de negocio.

¿Qué es una entidad?
- Representa un concepto del negocio (en este caso, un Usuario)
- Contiene las REGLAS DE NEGOCIO fundamentales
- NO conoce nada sobre bases de datos, APIs, Flask, etc.
- Es lo más estable del sistema (rara vez cambia)

Responsabilidades:
1. Definir qué ES un usuario (sus atributos)
2. Validar que un usuario sea válido según las reglas de negocio
3. Encapsular lógica relacionada con usuarios
"""


class User:
    """
    Representa un usuario en el sistema de recomendaciones
    """

    def __init__(self, name: str, email: str, password: str, phone: str = None,
                 user_id: int = None, category_id: int = None,
                 has_completed_questionnaire: bool = False, role: str = 'user'):
        """
        Constructor de la entidad User

        Args:
            name: Nombre completo del usuario
            email: Email del usuario (único en el sistema)
            password: Contraseña (puede estar encriptada o no)
            phone: Teléfono (opcional)
            user_id: ID del usuario (None si aún no está guardado en BD)
            category_id: ID de la categoría asignada (None si no ha completado cuestionario)
            has_completed_questionnaire: Si completó el cuestionario o no
        """
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.category_id = category_id
        self.has_completed_questionnaire = has_completed_questionnaire
        self.role = role

    def validate(self):
        """
        Valida que el usuario cumpla con las reglas de negocio

        Reglas de negocio para un usuario:
        1. El nombre debe tener al menos 3 caracteres
        2. El email debe tener formato válido (contener @ y .)
        3. La contraseña debe tener al menos 6 caracteres

        Raises:
            ValueError: Si alguna validación falla
        """
        # Validar nombre
        if not self.name or len(self.name.strip()) < 3:
            raise ValueError("Name must be at least 3 characters")

        if len(self.name.strip()) > 100:
            raise ValueError("Name cannot exceed 100 characters")

        # Validar email
        if not self.email:
            raise ValueError("Email is required")

        email_lower = self.email.lower().strip()
        if '@' not in email_lower or '.' not in email_lower:
            raise ValueError("Email must be a valid email address")

        # Validar contraseña (solo si está presente y NO está hasheada)
        if not self.password:
            raise ValueError("Password is required")

        # Solo validar formato si la contraseña NO está hasheada (bcrypt empieza con $2b$)
        if not self.password.startswith('$2b$'):
            # Validar longitud mínima
            if len(self.password) < 8:
                raise ValueError("Password must be at least 8 characters")

            # Validar que tenga al menos una mayúscula
            if not any(char.isupper() for char in self.password):
                raise ValueError(
                    "Password must contain at least one uppercase letter")

            # Validar que tenga al menos una minúscula
            if not any(char.islower() for char in self.password):
                raise ValueError(
                    "Password must contain at least one lowercase letter")

            # Validar que tenga al menos un número
            if not any(char.isdigit() for char in self.password):
                raise ValueError("Password must contain at least one number")

            # Validar que tenga al menos un carácter especial
            special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(char in special_characters for char in self.password):
                raise ValueError(
                    "Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")

    def to_dict(self):
        """
        Convierte la entidad a un diccionario

        Útil para:
        - Enviar datos en respuestas JSON
        - Debugging
        - Testing

        IMPORTANTE: NO incluir la contraseña (información sensible)

        Returns:
            dict: Diccionario con los datos del usuario
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'category_id': self.category_id,
            'has_completed_questionnaire': self.has_completed_questionnaire,
            'role': self.role
            # NO incluir 'password' por seguridad
        }

    def __repr__(self):
        """
        Representación en string del usuario (para debugging)
        """
        return f"User(id={self.id}, email={self.email}, name={self.name})"
