"""
Use Case: Delete Place
======================

Caso de uso para eliminar (desactivar) un lugar.
"""

from Infrastructure.Repositories.place_repository import PlaceRepository


class DeletePlaceUseCase:
    """
    Caso de uso: Eliminar un lugar
    """

    def __init__(self, place_repository: PlaceRepository):
        """
        Constructor

        Args:
            place_repository: Repositorio de lugares
        """
        self.place_repository = place_repository

    def execute(self, place_id: int) -> bool:
        """
        Ejecuta el caso de uso: eliminar lugar

        Args:
            place_id: ID del lugar a eliminar

        Returns:
            bool: True si se eliminó correctamente

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

        # Desactivar el lugar (soft delete)
        self.place_repository.delete(place_id)

        return True
