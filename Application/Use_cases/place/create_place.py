"""
Use Case: Create Place
======================

Caso de uso para crear un nuevo lugar.
"""

from Domain.Entities.place import Place
from Infrastructure.Repositories.place_repository import PlaceRepository


class CreatePlaceUseCase:
    """
    Caso de uso: Crear un lugar
    """

    def __init__(self, place_repository: PlaceRepository):
        """
        Constructor

        Args:
            place_repository: Repositorio de lugares
        """
        self.place_repository = place_repository

    def execute(self, name: str, description: str = None, address: str = None,
                phone: str = None, category_id: int = None, place_type: str = None,
                price_range: int = None, rating: float = None,
                image_url: str = None, opening_hours: str = None) -> Place:
        """
        Ejecuta el caso de uso: crear lugar

        Args:
            name: Nombre del lugar
            description: Descripción
            address: Dirección
            phone: Teléfono
            category_id: ID de la categoría
            place_type: Tipo de lugar
            price_range: Rango de precio(1-3)
            rating: Calificación(0-5)
            image_url: URL de la imagen
            opening_hours: Horario

        Returns:
            Place: Lugar creado

        Raises:
            ValueError: Si la validación falla
        """

        existing_places = self.place_repository.search_by_name(name)

        for existing in existing_places:
            # Mismo nombre Y misma dirección = duplicado
            if (existing.name.lower() == name.lower() and
                existing.address and address and
                    existing.address.lower() == address.lower()):
                raise ValueError(
                    f"A place with name '{name}' at address '{address}' already exists")

        # Crear entidad Place
        place = Place(
            name=name,
            description=description,
            address=address,
            phone=phone,
            category_id=category_id,
            place_type=place_type,
            price_range=price_range,
            rating=rating,
            image_url=image_url,
            opening_hours=opening_hours,
            is_active=True
        )

        # Validar
        place.validate()

        # Guardar en la base de datos
        created_place = self.place_repository.create(place)

        return created_place
