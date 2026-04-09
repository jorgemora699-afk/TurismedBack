"""
Entity: Category
================

Representa una categoría de usuario.
"""


class Category:
    """
    Entidad que representa una categoría de usuario
    """

    def __init__(self, category_id: int, name: str, description: str = None):
        """
        Constructor

        Args:
            category_id: ID de la categoría
            name: Nombre de la categoría
            description: Descripción de la categoría
        """
        self.id = category_id
        self.name = name
        self.description = description

    def to_dict(self):
        """
        Convierte la entidad a diccionario

        Returns:
            dict: Diccionario con los datos de la categoría
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"
