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
        Asigna categoría según las nuevas opciones del cuestionario.

        Categorías:
        1 - Foodies
        2 - Fiesteros  
        3 - Románticos
        4 - Casuales
        5 - Gourmet Nocturnos
        """

        categories = self.questionnaire_repository.get_all_categories()
        answers_text = " ".join([a.answer_text.lower() for a in answers])

        scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        # --- FOODIES (1) ---
        # Le importa la comida y el ambiente tranquilo
        if any(w in answers_text for w in ['restaurante casual', 'cocina internacional', 'alta cocina']):
            scores[1] += 2
        if 'tranquilo y relajado' in answers_text:
            scores[1] += 2
        if any(w in answers_text for w in ['solo', 'en pareja']):
            scores[1] += 1

        # --- FIESTEROS (2) ---
        # Música animada, ambiente de fiesta, noche
        if any(w in answers_text for w in ['reggaetón / urbana', 'salsa / bachata']):
            scores[2] += 2
        if 'ambiente de fiesta' in answers_text:
            scores[2] += 3
        if 'modo noche' in answers_text:
            scores[2] += 2
        if 'con amigos' in answers_text:
            scores[2] += 1

        # --- ROMÁNTICOS (3) ---
        # Ambiente romántico + en pareja
        if 'romántico' in answers_text:
            scores[3] += 3
        if 'en pareja' in answers_text:
            scores[3] += 3
        if any(w in answers_text for w in ['medio', 'alto']):
            scores[3] += 1
        if 'durante la tarde' in answers_text:
            scores[3] += 1

        # --- CASUALES (4) ---
        # Relajados, con amigos o familia, presupuesto bajo
        if 'a cualquier hora, sin reglas' in answers_text:
            scores[4] += 2
        if any(w in answers_text for w in ['con amigos', 'en familia']):
            scores[4] += 2
        if 'bajo' in answers_text:
            scores[4] += 2
        if 'variada' in answers_text:
            scores[4] += 1

        # --- GOURMET NOCTURNOS (5) ---
        # Buena comida + noche + presupuesto alto
        if any(w in answers_text for w in ['alta cocina', 'cocina internacional']):
            scores[5] += 2
        if any(w in answers_text for w in ['rock', 'variada']):
            scores[5] += 1
        if 'modo noche' in answers_text:
            scores[5] += 2
        if 'alto' in answers_text:
            scores[5] += 3

        # Asignar categoría con mayor puntaje
        max_score = max(scores.values())
        assigned_category_id = 4 if max_score == 0 else max(scores, key=scores.get)

        assigned_category = next(
            (cat for cat in categories if cat.id == assigned_category_id),
            categories[3]
        )

        return assigned_category
