"""
Use Case: Validate Promotion
=============================

Caso de uso para validar si un código promocional es válido.
"""

from Domain.Entities.promotion import Promotion
from Infrastructure.Repositories.promotion_repository import PromotionRepository


class ValidatePromotionUseCase:
    """
    Caso de uso: Validar una promoción
    """

    def __init__(self, promotion_repository: PromotionRepository):
        """
        Constructor

        Args:
            promotion_repository: Repositorio de promociones
        """
        self.promotion_repository = promotion_repository

    def execute(self, code: str) -> dict:
        """
        Ejecuta el caso de uso: validar promoción

        Args:
            code: Código de la promoción

        Returns:
            dict: {
                'valid': bool,
                'promotion': Promotion | None,
                'message': str
            }
        """

        # Buscar la promoción
        promotion = self.promotion_repository.find_by_code(
            code.upper().strip())

        if not promotion:
            return {
                'valid': False,
                'promotion': None,
                'message': 'Promotion code not found'
            }

        # Verificar si es válida
        if not promotion.is_valid():
            if not promotion.is_active:
                message = 'Promotion is no longer active'
            elif promotion.current_uses >= promotion.max_uses:
                message = 'Promotion has reached maximum uses'
            else:
                message = 'Promotion has expired'

            return {
                'valid': False,
                'promotion': promotion,
                'message': message
            }

        # Promoción válida
        return {
            'valid': True,
            'promotion': promotion,
            'message': 'Promotion is valid'
        }
