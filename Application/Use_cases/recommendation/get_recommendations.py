"""
Use Case: Get Recommendations
==============================

Caso de uso para obtener recomendaciones de lugares según la categoría del usuario.
"""

from Domain.Entities.place import Place
from Infrastructure.Repositories.user_repository import UserRepository
from Infrastructure.Repositories.place_repository import PlaceRepository
from typing import List


class GetRecommendationsUseCase:
    """
    Caso de uso: Obtener recomendaciones para un usuario
    """

    def __init__(self, user_repository: UserRepository,
                 place_repository: PlaceRepository):
        """
        Constructor

        Args:
            user_repository: Repositorio de usuarios
            place_repository: Repositorio de lugares
        """
        self.user_repository = user_repository
        self.place_repository = place_repository

    def execute(self, user_id: int) -> dict:
        """
        Ejecuta el caso de uso: obtener recomendaciones

        Pasos:
        1. Buscar al usuario
        2. Verificar que exista
        3. Verificar que haya completado el cuestionario
        4. Obtener su categoría
        5. Buscar lugares de esa categoría
        6. Retornar recomendaciones ordenadas por rating

        Args:
            user_id: ID del usuario

        Returns:
            dict: {
                'user': User,
                'category': Category,
                'recommendations': List[Place],
                'total': int
            }

        Raises:
            ValueError: Si el ID es inválido
            Exception: Si el usuario no existe o no ha completado el cuestionario
        """

        # Paso 1: Validar que el ID sea válido
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")

        # Paso 2: Buscar al usuario
        user = self.user_repository.find_by_id(user_id)

        if not user:
            raise Exception(f"User with ID {user_id} not found")

        # Paso 3: Verificar que haya completado el cuestionario
        if not user.has_completed_questionnaire:
            raise Exception(
                "User has not completed the questionnaire. Please complete it first.")

        # Paso 4: Verificar que tenga categoría asignada
        if not user.category_id:
            raise Exception("User does not have an assigned category")

        # Paso 5: Buscar lugares de su categoría
        places = self.place_repository.find_by_category(user.category_id)

        # Paso 6: Los lugares ya vienen ordenados por rating (desde el repository)
        # pero podríamos aplicar filtros adicionales aquí si queremos

        # Paso 7: Retornar resultado estructurado
        return {
            'user': user,
            'category_id': user.category_id,
            'recommendations': places,
            'total': len(places)
        }
