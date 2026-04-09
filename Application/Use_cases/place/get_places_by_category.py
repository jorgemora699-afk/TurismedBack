"""
Use Case: Get Places By Category
=================================

Caso de uso para obtener lugares filtrados por categoría.
"""

from Domain.Entities.place import Place
from Infrastructure.Repositories.place_repository import PlaceRepository
from typing import List


class GetPlacesByCategoryUseCase:
    """
    Caso de uso: Obtener lugares por categoría
    """

    def __init__(self, place_repository: PlaceRepository):
        """
        Constructor

        Args:
            place_repository: Repositorio de lugares
        """
        self.place_repository = place_repository

    def execute(self, category_id: int) -> List[Place]:
        """
        Ejecuta el caso de uso: obtener lugares por categoría

        Args:
            category_id: ID de la categoría

        Returns:
            List[Place]: Lista de lugares de esa categoría

        Raises:
            ValueError: Si el ID es inválido
        """

        # Validar ID
        if not category_id or category_id <= 0:
            raise ValueError("Invalid category ID")

        # Obtener lugares de la categoría
        places = self.place_repository.find_by_category(category_id)

        return places
