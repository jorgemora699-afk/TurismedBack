"""
Use Case: Get User Answers
===========================

Caso de uso para obtener las respuestas de un usuario.
"""

from Infrastructure.Repositories.questionnaire_repository import QuestionnaireRepository
from Domain.Entities.user_answer import UserAnswer
from typing import List


class GetUserAnswersUseCase:
    """
    Caso de uso: Obtener respuestas de un usuario
    """

    def __init__(self, questionnaire_repository: QuestionnaireRepository):
        """
        Constructor

        Args:
            questionnaire_repository: Repositorio del cuestionario
        """
        self.questionnaire_repository = questionnaire_repository

    def execute(self, user_id: int) -> List[UserAnswer]:
        """
        Ejecuta el caso de uso: obtener respuestas

        Args:
            user_id: ID del usuario

        Returns:
            List[UserAnswer]: Lista de respuestas del usuario

        Raises:
            ValueError: Si el ID es inválido
        """

        # Validar ID
        if not user_id or user_id <= 0:
            raise ValueError("Invalid user ID")

        # Obtener respuestas
        answers = self.questionnaire_repository.get_user_answers(user_id)

        return answers
