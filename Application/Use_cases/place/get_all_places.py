"""
Use Case: Get All Places
=========================

Caso de uso para obtener todos los lugares activos.
"""

from Domain.Entities.place import Place
from Infrastructure.Repositories.place_repository import PlaceRepository
from typing import List


class GetAllPlacesUseCase:
    """
    Caso de uso: Obtener todos los lugares
    """

    def __init__(self, place_repository: PlaceRepository):
        """
        Constructor

        Args:
            place_repository: Repositorio de lugares
        """
        self.place_repository = place_repository

    def execute(self) -> List[Place]:
        """
        Ejecuta el caso de uso: obtener todos los lugares activos

        Returns:
            List[Place]: Lista de lugares
        """

        # Obtener todos los lugares activos
        places = self.place_repository.get_all_active()

        return places
