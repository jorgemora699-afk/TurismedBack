"""
Entity: Place
=============

Representa un lugar (restaurante, discoteca, café, bar).
"""


class Place:
    """
    Entidad que representa un lugar
    """

    def __init__(self, place_id: int = None, name: str = None,
                 description: str = None, address: str = None,
                 phone: str = None, category_id: int = None,
                 place_type: str = None, price_range: int = None,
                 rating: float = None, image_url: str = None,
                 opening_hours: str = None, is_active: bool = True,
                 created_at=None):
        """
        Constructor

        Args:
            place_id: ID del lugar
            name: Nombre del lugar
            description: Descripción
            address: Dirección
            phone: Teléfono
            category_id: ID de la categoría asociada
            place_type: Tipo (restaurant, nightclub, cafe, bar)
            price_range: Rango de precio (1=$, 2=$$, 3=$$$)
            rating: Calificación (0-5)
            image_url: URL de la imagen
            opening_hours: Horario de apertura
            is_active: Si está activo
            created_at: Fecha de creación
        """
        self.id = place_id
        self.name = name
        self.description = description
        self.address = address
        self.phone = phone
        self.category_id = category_id
        self.place_type = place_type
        self.price_range = price_range
        self.rating = rating
        self.image_url = image_url
        self.opening_hours = opening_hours
        self.is_active = is_active
        self.created_at = created_at

    def validate(self):
        """
        Valida que el lugar sea válido

        Raises:
            ValueError: Si la validación falla
        """
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Place name cannot be empty")

        if len(self.name) > 200:
            raise ValueError("Place name cannot exceed 200 characters")

        if self.place_type and self.place_type not in ['restaurant', 'nightclub', 'cafe', 'bar']:
            raise ValueError(
                "Invalid place type. Must be: restaurant, nightclub, cafe, or bar")

        if self.price_range is not None:
            if self.price_range < 1 or self.price_range > 3:
                raise ValueError("Price range must be between 1 and 3")

        if self.rating is not None:
            if self.rating < 0 or self.rating > 5:
                raise ValueError("Rating must be between 0 and 5")

    def get_price_symbol(self) -> str:
        """
        Retorna el símbolo de precio según el rango

        Returns:
            str: '$', '$$', o '$$$'
        """
        if self.price_range == 1:
            return '$'
        elif self.price_range == 2:
            return '$$'
        elif self.price_range == 3:
            return '$$$'
        return ''

    def to_dict(self):
        """
        Convierte la entidad a diccionario

        Returns:
            dict: Diccionario con los datos del lugar
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'phone': self.phone,
            'category_id': self.category_id,
            'place_type': self.place_type,
            'price_range': self.price_range,
            'price_symbol': self.get_price_symbol(),
            'rating': float(self.rating) if self.rating else None,
            'image_url': self.image_url,
            'opening_hours': self.opening_hours,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"Place(id={self.id}, name={self.name}, type={self.place_type})"
