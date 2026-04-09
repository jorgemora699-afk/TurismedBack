"""
Place Repository Interface
==========================

Define las operaciones relacionadas con lugares.
"""

from abc import ABC, abstractmethod
from Domain.Entities.place import Place
from typing import List, Optional


class PlaceRepository(ABC):
    """
    Interfaz del repositorio de lugares
    """

    @abstractmethod
    def create(self, place: Place) -> Place:
        """
        Crea un nuevo lugar

        Args:
            place: Lugar a crear

        Returns:
            Place: Lugar creado con ID
        """
        pass

    @abstractmethod
    def find_by_id(self, place_id: int) -> Optional[Place]:
        """
        Busca un lugar por ID

        Args:
            place_id: ID del lugar

        Returns:
            Place si existe, None si no
        """
        pass

    @abstractmethod
    def get_all_active(self) -> List[Place]:
        """
        Obtiene todos los lugares activos

        Returns:
            List[Place]: Lista de lugares activos
        """
        pass

    @abstractmethod
    def find_by_category(self, category_id: int) -> List[Place]:
        """
        Busca lugares por categoría

        Args:
            category_id: ID de la categoría

        Returns:
            List[Place]: Lista de lugares de esa categoría
        """
        pass

    @abstractmethod
    def find_by_type(self, place_type: str) -> List[Place]:
        """
        Busca lugares por tipo

        Args:
            place_type: Tipo de lugar (restaurant, nightclub, cafe, bar)

        Returns:
            List[Place]: Lista de lugares de ese tipo
        """
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Place]:
        """
        Busca lugares por nombre (búsqueda parcial)

        Args:
            name: Texto a buscar en el nombre

        Returns:
            List[Place]: Lista de lugares que coinciden
        """
        pass

    @abstractmethod
    def update(self, place: Place) -> Place:
        """
        Actualiza un lugar

        Args:
            place: Lugar con datos actualizados

        Returns:
            Place: Lugar actualizado
        """
        pass

    @abstractmethod
    def deactivate(self, place_id: int) -> bool:
        """
        Desactiva un lugar (soft delete)

        Args:
            place_id: ID del lugar

        Returns:
            bool: True si se desactivó
        """
        pass

    @abstractmethod
    def delete(self, place_id: int) -> bool:
        """
        Elimina un lugar permanentemente (hard delete)

        Args:
            place_id: ID del lugar

        Returns:
            bool: True si se eliminó
        """
        pass
