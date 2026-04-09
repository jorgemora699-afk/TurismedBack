"""
Use Case: Submit Questionnaire
===============================

Caso de uso para enviar respuestas del cuestionario y asignar categoría.

Lógica de negocio:
1. Validar que el usuario exista
2. Validar que vengan 6 respuestas
3. Guardar las respuestas
4. Analizar las respuestas
5. Asignar una categoría
6. Actualizar el usuario
"""

from Infrastructure.Repositories.questionnaire_repository import QuestionnaireRepository
from Infrastructure.Repositories.user_repository import UserRepository
from Domain.Entities.user_answer import UserAnswer
from Domain.Entities.category import Category
from typing import List


class SubmitQuestionnaireUseCase:
    """
    Caso de uso: Enviar respuestas del cuestionario
    """

    def __init__(self, questionnaire_repository: QuestionnaireRepository,
                 user_repository: UserRepository):
        """
        Constructor

        Args:
            questionnaire_repository: Repositorio del cuestionario
            user_repository: Repositorio de usuarios
        """
        self.questionnaire_repository = questionnaire_repository
        self.user_repository = user_repository

    def execute(self, user_id: int, answers: List[dict]) -> Category:
        """
        Ejecuta el caso de uso: enviar respuestas

        Args:
            user_id: ID del usuario
            answers: Lista de respuestas en formato:
                    [
                        {"question_id": 1, "answer": "Rock"},
                        {"question_id": 2, "answer": "Tranquilo"},
                        ...
                    ]

        Returns:
            Category: Categoría asignada al usuario

        Raises:
            ValueError: Si las validaciones fallan
            Exception: Si el usuario no existe
        """

        # Paso 1: Validar que el usuario exista
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise Exception(f"User with ID {user_id} not found")

        # Paso 2: Validar que vengan exactamente 6 respuestas
        if not answers or len(answers) != 6:
            raise ValueError("You must answer all 6 questions")

        # Paso 3: Crear entidades UserAnswer y validarlas
        user_answers = []
        for answer_data in answers:
            question_id = answer_data.get('question_id')
            answer_text = answer_data.get('answer')

            if not question_id or not answer_text:
                raise ValueError(
                    "Each answer must have question_id and answer")

            user_answer = UserAnswer(
                user_id=user_id,
                question_id=question_id,
                answer_text=answer_text
            )
            user_answer.validate()
            user_answers.append(user_answer)

        # Paso 4: Eliminar respuestas anteriores (si existen)
        self.questionnaire_repository.delete_user_answers(user_id)

        # Paso 5: Guardar las nuevas respuestas
        self.questionnaire_repository.save_user_answers(user_answers)

        # Paso 6: Analizar respuestas y asignar categoría
        assigned_category = self._assign_category(user_answers)

        # Paso 7: Actualizar el usuario con la categoría asignada
        user.category_id = assigned_category.id
        user.has_completed_questionnaire = True
        self.user_repository.update(user)

        # Paso 8: Retornar la categoría asignada
        return assigned_category

    def _assign_category(self, answers: List[UserAnswer]) -> Category:
        """
        Lógica para asignar una categoría según las respuestas

        Esta es una lógica simplificada basada en palabras clave.
        En producción podrías usar ML, scoring más complejo, etc.

        Args:
            answers: Lista de respuestas del usuario

        Returns:
            Category: Categoría asignada
        """

        # Obtener todas las categorías disponibles
        categories = self.questionnaire_repository.get_all_categories()

        # Convertir respuestas a minúsculas para análisis
        answers_text = " ".join([a.answer_text.lower() for a in answers])

        # Sistema de puntuación por categoría
        scores = {
            1: 0,  # Foodies
            2: 0,  # Fiesteros
            3: 0,  # Románticos
            4: 0,  # Casuales
            5: 0   # Gourmet Nocturnos
        }

        # Reglas de puntuación basadas en palabras clave

        # FOODIES - Pregunta 3 (comida) + ambiente tranquilo
        if any(word in answers_text for word in ['italiana', 'asiática', 'gourmet', 'internacional']):
            scores[1] += 2
        if 'tranquilo' in answers_text:
            scores[1] += 1

        # FIESTEROS - Música animada + ambiente bullicioso + fin de semana
        if any(word in answers_text for word in ['electrónica', 'reggaeton', 'salsa']):
            scores[2] += 2
        if 'bullicioso' in answers_text or 'animado' in answers_text:
            scores[2] += 2
        if 'fin de semana' in answers_text:
            scores[2] += 1

        # ROMÁNTICOS - Ambiente romántico + en pareja
        if 'romántico' in answers_text:
            scores[3] += 3
        if 'pareja' in answers_text:
            scores[3] += 2
        # Presupuesto
        if any(word in answers_text for word in ['medio', 'alto']):
            scores[3] += 1

        # CASUALES - Cualquier día + con amigos + económico
        if 'cualquier' in answers_text:
            scores[4] += 2
        if 'amigos' in answers_text:
            scores[4] += 2
        if 'económico' in answers_text:
            scores[4] += 1

        # GOURMET NOCTURNOS - Buena comida + vida nocturna
        if any(word in answers_text for word in ['italiana', 'asiática', 'gourmet']):
            scores[5] += 1
        if any(word in answers_text for word in ['jazz', 'rock']):
            scores[5] += 1
        if 'bullicioso' in answers_text or 'animado' in answers_text:
            scores[5] += 1
        if 'alto' in answers_text:  # Presupuesto alto
            scores[5] += 2

        # Obtener la categoría con mayor puntuación
        max_score = max(scores.values())

        # Si todas tienen 0 puntos, asignar "Casuales" por defecto
        if max_score == 0:
            assigned_category_id = 4  # Casuales
        else:
            assigned_category_id = max(scores, key=scores.get)

        # Buscar la categoría en la lista
        assigned_category = next(
            (cat for cat in categories if cat.id == assigned_category_id),
            categories[3]  # Casuales por defecto si no se encuentra
        )

        return assigned_category
