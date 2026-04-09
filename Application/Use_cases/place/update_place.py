"""
Use Case: Update Place
=======================

Caso de uso para actualizar un lugar.
"""

from Domain.Entities.place import Place
from Infrastructure.Repositories.place_repository import PlaceRepository


class UpdatePlaceUseCase:
    """
    Caso de uso: Actualizar un lugar
    """

    def __init__(self, place_repository: PlaceRepository):
        """
        Constructor

        Args:
            place_repository: Repositorio de lugares
        """
        self.place_repository = place_repository

    def execute(self, place_id: int, name: str = None, description: str = None,
                address: str = None, phone: str = None, category_id: int = None,
                place_type: str = None, price_range: int = None, rating: float = None,
                image_url: str = None, opening_hours: str = None) -> Place:
        """
        Ejecuta el caso de uso: actualizar lugar

        Args:
            place_id: ID del lugar a actualizar
            name: Nuevo nombre (opcional)
            description: Nueva descripción (opcional)
            ... (otros campos opcionales)

        Returns:
            Place: Lugar actualizado

        Raises:
            ValueError: Si el ID es inválido
            Exception: Si el lugar no existe
        """

        # Validar ID
        if not place_id or place_id <= 0:
            raise ValueError("Invalid place ID")

        # Buscar el lugar existente
        place = self.place_repository.find_by_id(place_id)

        if not place:
            raise Exception(f"Place with ID {place_id} not found")

        # Actualizar solo los campos proporcionados
        if name is not None:
            place.name = name
        if description is not None:
            place.description = description
        if address is not None:
            place.address = address
        if phone is not None:
            place.phone = phone
        if category_id is not None:
            place.category_id = category_id
        if place_type is not None:
            place.place_type = place_type
        if price_range is not None:
            place.price_range = price_range
        if rating is not None:
            place.rating = rating
        if image_url is not None:
            place.image_url = image_url
        if opening_hours is not None:
            place.opening_hours = opening_hours

        # Validar los nuevos datos
        place.validate()

        # Actualizar en el repositorio
        updated_place = self.place_repository.update(place)

        return updated_place
