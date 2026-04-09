"""
Entity: Redemption
==================

Representa la redención de una promoción por un usuario.
"""

from datetime import datetime


class Redemption:
    """
    Entidad que representa una redención
    """

    def __init__(self, redemption_id: int = None, user_id: int = None,
                 promotion_id: int = None, redeemed_at: datetime = None):
        """
        Constructor

        Args:
            redemption_id: ID de la redención
            user_id: ID del usuario
            promotion_id: ID de la promoción
            redeemed_at: Fecha de redención
        """
        self.id = redemption_id
        self.user_id = user_id
        self.promotion_id = promotion_id
        self.redeemed_at = redeemed_at

    def to_dict(self):
        """
        Convierte la entidad a diccionario

        Returns:
            dict: Diccionario con los datos de la redención
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'promotion_id': self.promotion_id,
            'redeemed_at': self.redeemed_at.isoformat() if self.redeemed_at else None
        }

    def __repr__(self):
        return f"Redemption(id={self.id}, user_id={self.user_id}, promotion_id={self.promotion_id})"
