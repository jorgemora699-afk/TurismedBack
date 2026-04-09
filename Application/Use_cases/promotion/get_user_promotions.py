"""
Use Case: Get User Promotions
==============================

Caso de uso para obtener las promociones redimidas por un usuario.
"""

from Infrastructure.Repositories.promotion_repository import PromotionRepository
from typing import List


class GetUserPromotionsUseCase:
    """
    Caso de uso: Obtener promociones de un usuario
    """

    def __init__(self, promotion_repository: PromotionRepository):
        """
        Constructor

        Args:
            promotion_repository: Repositorio de promociones
        """
        self.promotion_repository = promotion_repository

    def execute(self, user_id: int) -> List[dict]:
        """
        Ejecuta el caso de uso: obtener promociones del usuario

        Args:
            user_id: ID del usuario

        Returns:
            List[dict]: Lista de promociones redimidas con sus datos
        """

        # Validar ID
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")

        # Obtener promociones redimidas
        redemptions = self.promotion_repository.get_user_redemptions(user_id)

        return redemptions
