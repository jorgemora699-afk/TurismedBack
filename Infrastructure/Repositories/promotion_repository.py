"""
Promotion Repository Interface
===============================

Define las operaciones relacionadas con promociones.
"""

from abc import ABC, abstractmethod
from Domain.Entities.promotion import Promotion
from Domain.Entities.redemption import Redemption
from typing import List, Optional


class PromotionRepository(ABC):
    """
    Interfaz del repositorio de promociones
    """

    @abstractmethod
    def create(self, promotion: Promotion) -> Promotion:
        """
        Crea una nueva promoción

        Args:
            promotion: Promoción a crear

        Returns:
            Promotion: Promoción creada con ID
        """
        pass

    @abstractmethod
    def find_by_id(self, promotion_id: int) -> Optional[Promotion]:
        """
        Busca una promoción por ID

        Args:
            promotion_id: ID de la promoción

        Returns:
            Promotion si existe, None si no
        """
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Promotion]:
        """
        Busca una promoción por código

        Args:
            code: Código de la promoción

        Returns:
            Promotion si existe, None si no
        """
        pass

    @abstractmethod
    def get_all_active(self) -> List[Promotion]:
        """
        Obtiene todas las promociones activas

        Returns:
            List[Promotion]: Lista de promociones activas
        """
        pass

    @abstractmethod
    def update(self, promotion: Promotion) -> Promotion:
        """
        Actualiza una promoción

        Args:
            promotion: Promoción con datos actualizados

        Returns:
            Promotion: Promoción actualizada
        """
        pass

    @abstractmethod
    def deactivate(self, promotion_id: int) -> bool:
        """
        Desactiva una promoción

        Args:
            promotion_id: ID de la promoción

        Returns:
            bool: True si se desactivó
        """
        pass

    @abstractmethod
    def redeem(self, user_id: int, promotion_id: int) -> Redemption:
        """
        Redime una promoción para un usuario

        Args:
            user_id: ID del usuario
            promotion_id: ID de la promoción

        Returns:
            Redemption: Registro de redención creado
        """
        pass

    @abstractmethod
    def user_has_redeemed(self, user_id: int, promotion_id: int) -> bool:
        """
        Verifica si un usuario ya redimió una promoción

        Args:
            user_id: ID del usuario
            promotion_id: ID de la promoción

        Returns:
            bool: True si ya la redimió
        """
        pass

    @abstractmethod
    def get_user_redemptions(self, user_id: int) -> List[dict]:
        """
        Obtiene las redenciones de un usuario

        Args:
            user_id: ID del usuario

        Returns:
            List[dict]: Lista de redenciones con datos de la promoción
        """
        pass
