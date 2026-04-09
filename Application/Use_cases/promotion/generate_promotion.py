"""
Use Case: Generate Promotion
=============================

Caso de uso para generar un nuevo código promocional.
"""

import random
import string
from datetime import datetime, timedelta
from Domain.Entities.promotion import Promotion
from Infrastructure.Repositories.promotion_repository import PromotionRepository


class GeneratePromotionUseCase:
    """
    Caso de uso: Generar una nueva promoción
    """

    def __init__(self, promotion_repository: PromotionRepository):
        """
        Constructor

        Args:
            promotion_repository: Repositorio de promociones
        """
        self.promotion_repository = promotion_repository

    def execute(self, description: str = None, discount_percentage: int = None,
            discount_amount: float = None, max_uses: int = 1,
            expires_in_days: int = 30, custom_code: str = None,
            place_id: int = None) -> Promotion:  # ← NUEVO place_id

        if discount_percentage is None and discount_amount is None:
            raise ValueError("Must provide either discount_percentage or discount_amount")

        if discount_percentage is not None:
            if discount_percentage < 0 or discount_percentage > 100:
                raise ValueError("Discount percentage must be between 0 and 100")

        if max_uses < 1:
            raise ValueError("Max uses must be at least 1")

        if custom_code:
            code = custom_code.upper().strip()
            existing = self.promotion_repository.find_by_code(code)
            if existing:
                raise ValueError(f"Promotion code '{code}' already exists")
        else:
            code = self._generate_unique_code()

        expires_at = datetime.now() + timedelta(days=expires_in_days)

        promotion = Promotion(
            code=code,
            description=description,
            discount_percentage=discount_percentage,
            discount_amount=discount_amount,
            max_uses=max_uses,
            current_uses=0,
            is_active=True,
            expires_at=expires_at,
            place_id=place_id  # ← NUEVO
        )

        promotion.validate()

        created_promotion = self.promotion_repository.create(promotion)

        return created_promotion

    def _generate_unique_code(self) -> str:
        """
        Genera un código único de 10 caracteres

        Returns:
            str: Código único
        """
        max_attempts = 10

        for _ in range(max_attempts):
            # Generar código aleatorio de 10 caracteres (letras y números)
            code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10))

            # Verificar que no exista
            existing = self.promotion_repository.find_by_code(code)
            if not existing:
                return code

        raise Exception(
            "Could not generate unique code after multiple attempts")
