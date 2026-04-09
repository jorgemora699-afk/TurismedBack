"""
Questionnaire Repository Interface
===================================

Define las operaciones relacionadas con el cuestionario.
"""

from abc import ABC, abstractmethod
from Domain.Entities.question import Question
from Domain.Entities.category import Category
from Domain.Entities.user_answer import UserAnswer
from typing import List, Optional


class QuestionnaireRepository(ABC):
    """
    Interfaz del repositorio del cuestionario
    """

    @abstractmethod
    def get_all_questions(self) -> List[Question]:
        """
        Obtiene todas las preguntas ordenadas

        Returns:
            List[Question]: Lista de preguntas
        """
        pass

    @abstractmethod
    def save_user_answers(self, answers: List[UserAnswer]) -> bool:
        """
        Guarda las respuestas de un usuario

        Args:
            answers: Lista de respuestas del usuario

        Returns:
            bool: True si se guardaron correctamente
        """
        pass

    @abstractmethod
    def get_user_answers(self, user_id: int) -> List[UserAnswer]:
        """
        Obtiene las respuestas de un usuario

        Args:
            user_id: ID del usuario

        Returns:
            List[UserAnswer]: Lista de respuestas del usuario
        """
        pass

    @abstractmethod
    def delete_user_answers(self, user_id: int) -> bool:
        """
        Elimina las respuestas anteriores de un usuario
        (Para poder responder de nuevo)

        Args:
            user_id: ID del usuario

        Returns:
            bool: True si se eliminaron
        """
        pass

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        """
        Obtiene todas las categorías

        Returns:
            List[Category]: Lista de categorías
        """
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """
        Obtiene una categoría por ID

        Args:
            category_id: ID de la categoría

        Returns:
            Category si existe, None si no
        """
        pass
