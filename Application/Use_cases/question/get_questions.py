"""
Use Case: Get Questions
========================

Caso de uso para obtener todas las preguntas del cuestionario.
"""

from Infrastructure.Repositories.questionnaire_repository import QuestionnaireRepository
from Domain.Entities.question import Question
from typing import List


class GetQuestionsUseCase:
    """
    Caso de uso: Obtener las preguntas del cuestionario
    """

    def __init__(self, questionnaire_repository: QuestionnaireRepository):
        """
        Constructor

        Args:
            questionnaire_repository: Repositorio del cuestionario
        """
        self.questionnaire_repository = questionnaire_repository

    def execute(self) -> List[Question]:
        """
        Ejecuta el caso de uso: obtener preguntas

        Returns:
            List[Question]: Lista de preguntas ordenadas
        """

        # Obtener todas las preguntas del repositorio
        questions = self.questionnaire_repository.get_all_questions()

        # Verificar que existan preguntas
        if not questions or len(questions) == 0:
            raise Exception("No questions found in the system")

        return questions
