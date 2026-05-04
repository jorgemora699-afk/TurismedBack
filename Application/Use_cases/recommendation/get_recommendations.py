"""
Use Case: Get Recommendations
==============================
Filtra lugares por categoría + respuestas individuales del usuario.
"""

from Infrastructure.Repositories.user_repository import UserRepository
from Infrastructure.Repositories.place_repository import PlaceRepository
from Infrastructure.Repositories.questionnaire_repository import QuestionnaireRepository
from typing import List


class GetRecommendationsUseCase:

    def __init__(self, user_repository: UserRepository,
                 place_repository: PlaceRepository,
                 questionnaire_repository: QuestionnaireRepository):
        self.user_repository = user_repository
        self.place_repository = place_repository
        self.questionnaire_repository = questionnaire_repository

    def execute(self, user_id: int) -> dict:

        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")

        # Buscar usuario
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise Exception(f"User with ID {user_id} not found")

        if not user.has_completed_questionnaire:
            raise Exception(
                "User has not completed the questionnaire. Please complete it first.")

        if not user.category_id:
            raise Exception("User does not have an assigned category")

        # Traer lugares de su categoría
        places = self.place_repository.find_by_category(user.category_id)

        # Traer respuestas del usuario para filtrar
        user_answers = self.questionnaire_repository.get_user_answers(user_id)
        answers_map = {a.question_id: a.answer_text.lower() for a in user_answers}

        # Extraer preferencias clave
        # Q6 = presupuesto, Q4 = horario
        budget = answers_map.get(6, '')
        schedule = answers_map.get(4, '')

        # Mapear presupuesto a price_range de la DB
        budget_filter = None
        if 'bajo' in budget:
            budget_filter = 'low'
        elif 'medio' in budget:
            budget_filter = 'medium'
        elif 'alto' in budget:
            budget_filter = 'high'

        # Mapear horario a opening_hours de la DB
        schedule_filter = None
        if 'temprano' in schedule:
            schedule_filter = 'day'
        elif 'tarde' in schedule:
            schedule_filter = 'afternoon'
        elif 'noche' in schedule:
            schedule_filter = 'night'

        # Aplicar filtros si hay coincidencias
        filtered = []
        for place in places:
            price_ok = (
                budget_filter is None or
                place.price_range is None or
                place.price_range.lower() == budget_filter
            )
            schedule_ok = (
                schedule_filter is None or
                place.opening_hours is None or
                schedule_filter in place.opening_hours.lower()
            )
            if price_ok and schedule_ok:
                filtered.append(place)

        # Si los filtros dejaron muy pocos lugares, usar todos los de la categoría
        recommendations = filtered if len(filtered) >= 3 else places

        return {
            'user': user,
            'category_id': user.category_id,
            'recommendations': recommendations,
            'total': len(recommendations)
        }