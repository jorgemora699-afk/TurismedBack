"""
Entity: Promotion
=================

Representa una promoción/código de descuento.
"""

from datetime import datetime


class Promotion:
    """
    Entidad que representa una promoción
    """

    def __init__(self, promotion_id: int = None, code: str = None,
                description: str = None, discount_percentage: int = None,
                discount_amount: float = None, max_uses: int = 1,
                current_uses: int = 0, is_active: bool = True,
                expires_at: datetime = None, created_at: datetime = None,
                place_id: int = None, place_name: str = None):
        """
        Constructor

        Args:
            promotion_id: ID de la promoción
            code: Código único de la promoción
            description: Descripción de la promoción
            discount_percentage: Porcentaje de descuento (ej: 20 = 20%)
            discount_amount: Monto fijo de descuento
            max_uses: Máximo de usos permitidos
            current_uses: Usos actuales
            is_active: Si la promoción está activa
            expires_at: Fecha de expiración
            created_at: Fecha de creación
        """
        self.id = promotion_id
        self.code = code
        self.description = description
        self.discount_percentage = discount_percentage
        self.discount_amount = discount_amount
        self.max_uses = max_uses
        self.current_uses = current_uses
        self.is_active = is_active
        self.expires_at = expires_at
        self.created_at = created_at
        self.place_id = place_id     
        self.place_name = place_name 

    def validate(self):
        """
        Valida que la promoción sea válida

        Raises:
            ValueError: Si la validación falla
        """
        if not self.code or len(self.code.strip()) == 0:
            raise ValueError("Promotion code cannot be empty")

        if len(self.code) > 20:
            raise ValueError("Promotion code cannot exceed 20 characters")

        if self.discount_percentage is not None:
            if self.discount_percentage < 0 or self.discount_percentage > 100:
                raise ValueError(
                    "Discount percentage must be between 0 and 100")

        if self.max_uses is not None and self.max_uses < 1:
            raise ValueError("Max uses must be at least 1")

    def is_valid(self) -> bool:
        """
        Verifica si la promoción es válida para usar

        Returns:
            bool: True si es válida
        """
        # Verificar si está activa
        if not self.is_active:
            return False

        # Verificar si no ha expirado
        if self.expires_at and datetime.now() > self.expires_at:
            return False

        # Verificar si no ha alcanzado el máximo de usos
        if self.current_uses >= self.max_uses:
            return False

        return True

    def to_dict(self):
        """
        Convierte la entidad a diccionario

        Returns:
            dict: Diccionario con los datos de la promoción
        """
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'discount_percentage': self.discount_percentage,
            'discount_amount': float(self.discount_amount) if self.discount_amount else None,
            'max_uses': self.max_uses,
            'current_uses': self.current_uses,
            'is_active': self.is_active,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_valid': self.is_valid(),
            'place_id': self.place_id,
            'place_name': self.place_name,
        }

    def __repr__(self):
        return f"Promotion(id={self.id}, code={self.code})"
