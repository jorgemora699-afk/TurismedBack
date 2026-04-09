"""
Use Case: Redeem Promotion
===========================

Caso de uso para redimir un código promocional.
"""

from Domain.Entities.promotion import Promotion
from Domain.Entities.redemption import Redemption
from Infrastructure.Repositories.promotion_repository import PromotionRepository
from Infrastructure.Repositories.user_repository import UserRepository


class RedeemPromotionUseCase:
    """
    Caso de uso: Redimir una promoción
    """

    def __init__(self, promotion_repository: PromotionRepository,
                 user_repository: UserRepository):
        """
        Constructor

        Args:
            promotion_repository: Repositorio de promociones
            user_repository: Repositorio de usuarios
        """
        self.promotion_repository = promotion_repository
        self.user_repository = user_repository

    def execute(self, user_id: int, code: str) -> dict:
        """
        Ejecuta el caso de uso: redimir promoción

        Args:
            user_id: ID del usuario
            code: Código de la promoción

        Returns:
            dict: {
                'success': bool,
                'promotion': Promotion | None,
                'redemption': Redemption | None,
                'message': str
            }

        Raises:
            ValueError: Si los parámetros son inválidos
            Exception: Si el usuario no existe
        """

        # Validar que el usuario exista
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise Exception(f"User with ID {user_id} not found")

        # Buscar la promoción
        promotion = self.promotion_repository.find_by_code(
            code.upper().strip())

        if not promotion:
            return {
                'success': False,
                'promotion': None,
                'redemption': None,
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
                'success': False,
                'promotion': promotion,
                'redemption': None,
                'message': message
            }

        # Verificar si el usuario ya redimió esta promoción
        already_redeemed = self.promotion_repository.user_has_redeemed(
            user_id, promotion.id)

        if already_redeemed:
            return {
                'success': False,
                'promotion': promotion,
                'redemption': None,
                'message': 'You have already redeemed this promotion'
            }

        # Redimir la promoción
        redemption = self.promotion_repository.redeem(user_id, promotion.id)

        # Obtener la promoción actualizada
        updated_promotion = self.promotion_repository.find_by_id(promotion.id)

        return {
            'success': True,
            'promotion': updated_promotion,
            'redemption': redemption,
            'message': 'Promotion redeemed successfully'
        }
