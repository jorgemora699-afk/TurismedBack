"""
Use Case: Get Place By ID
==========================

Caso de uso para obtener un lugar por su ID.
"""

from Domain.Entities.place import Place
from Infrastructure.Repositories.place_repository import PlaceRepository


class GetPlaceByIdUseCase:
    """
    Caso de uso: Obtener lugar por ID
    """

    def __init__(self, place_repository: PlaceRepository):
        """
        Constructor

        Args:
            place_repository: Repositorio de lugares
        """
        self.place_repository = place_repository

    def execute(self, place_id: int) -> Place:
        """
        Ejecuta el caso de uso: obtener lugar por ID

        Args:
            place_id: ID del lugar

        Returns:
            Place: Lugar encontrado

        Raises:
            ValueError: Si el ID es inválido
            Exception: Si el lugar no existe
        """

        # Validar ID
        if not place_id or place_id <= 0:
            raise ValueError("Invalid place ID")

        # Buscar el lugar
        place = self.place_repository.find_by_id(place_id)

        if not place:
            raise Exception(f"Place with ID {place_id} not found")

        return place
