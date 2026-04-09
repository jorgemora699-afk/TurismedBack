"""
Questionnaire Controller
========================

Controlador para manejar las peticiones HTTP del cuestionario.
"""

from flask import request, jsonify
from Application.Use_cases.question.get_questions import GetQuestionsUseCase
from Application.Use_cases.question.submit_questionnaire import SubmitQuestionnaireUseCase
from Application.Use_cases.question.get_user_answers import GetUserAnswersUseCase
from Infrastructure.Repositories.questionnaire_repository import QuestionnaireRepository
from Infrastructure.Repositories.user_repository import UserRepository
from Infrastructure.auth.role_checker import can_modify_user


class QuestionnaireController:
    """
    Controlador del cuestionario
    """

    def __init__(self, questionnaire_repository: QuestionnaireRepository,
                 user_repository: UserRepository):
        """
        Constructor

        Args:
            questionnaire_repository: Repositorio del cuestionario
            user_repository: Repositorio de usuarios
        """
        # Crear los Use Cases
        self.get_questions_use_case = GetQuestionsUseCase(
            questionnaire_repository)
        self.submit_questionnaire_use_case = SubmitQuestionnaireUseCase(
            questionnaire_repository,
            user_repository
        )
        self.get_user_answers_use_case = GetUserAnswersUseCase(
            questionnaire_repository)

    def get_questions(self):
        """
        GET /questionnaire/questions

        Obtiene todas las preguntas del cuestionario

        Returns:
            JSON response con las preguntas
        """
        try:
            # Llamar al Use Case
            questions = self.get_questions_use_case.execute()

            # Convertir a diccionarios
            questions_dict = [q.to_dict() for q in questions]

            return jsonify({
                'success': True,
                'data': {
                    'questions': questions_dict,
                    'total': len(questions_dict)
                }
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': str(e)
            }), 500

    def submit_questionnaire(self):
        """
        POST /questionnaire/submit

        Envía respuestas del cuestionario y asigna categoría

        Request JSON esperado:
        {
            "user_id": 1,
            "answers": [
                {"question_id": 1, "answer": "Rock"},
                {"question_id": 2, "answer": "Tranquilo"},
                {"question_id": 3, "answer": "Italiana"},
                {"question_id": 4, "answer": "Fin de semana"},
                {"question_id": 5, "answer": "En pareja"},
                {"question_id": 6, "answer": "Medio"}
            ]
        }

        Returns:
            JSON response con la categoría asignada
        """
        try:
            # Obtener datos del request
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided',
                    'message': 'Request body is empty'
                }), 400

            # Validar campos requeridos
            user_id = data.get('user_id')
            answers = data.get('answers')

            if not user_id:
                return jsonify({
                    'success': False,
                    'error': 'Missing user_id',
                    'message': 'user_id is required'
                }), 400

            if not answers:
                return jsonify({
                    'success': False,
                    'error': 'Missing answers',
                    'message': 'answers array is required'
                }), 400

            # Validar que user_id sea número
            try:
                user_id_int = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid user_id',
                    'message': 'user_id must be a number'
                }), 400

            # Llamar al Use Case
            assigned_category = self.submit_questionnaire_use_case.execute(
                user_id=user_id_int,
                answers=answers
            )

            return jsonify({
                'success': True,
                'message': 'Questionnaire submitted successfully',
                'data': {
                    'assigned_category': assigned_category.to_dict()
                }
            }), 200

        except ValueError as e:
            # Error de validación
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400

        except Exception as e:
            # Usuario no encontrado u otro error
            error_message = str(e)

            if 'not found' in error_message.lower():
                return jsonify({
                    'success': False,
                    'error': 'User not found',
                    'message': error_message
                }), 404

            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500

    def get_user_answers(self, current_user, user_id):
        """
        GET /questionnaire/user/:user_id

        Obtiene las respuestas de un usuario

        Args:
            user_id: ID del usuario

        Returns:
            JSON response con las respuestas del usuario
        """
        try:
            # Validar que el ID sea un número
            try:
                user_id_int = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid ID format',
                    'message': 'User ID must be a number'
                }), 400

            # ✅ VERIFICAR PERMISOS (admin o mismo usuario)
            if not can_modify_user(current_user, user_id_int):
                return jsonify({
                    'success': False,
                    'error': 'Forbidden',
                    'message': 'You can only delete your own account (unless you are admin)'
                }), 403

            # Llamar al Use Case
            answers = self.get_user_answers_use_case.execute(user_id_int)

            # Convertir a diccionarios
            answers_dict = [a.to_dict() for a in answers]

            return jsonify({
                'success': True,
                'data': {
                    'user_id': user_id_int,
                    'answers': answers_dict,
                    'total': len(answers_dict)
                }
            }), 200

        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400

        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': str(e)
            }), 500
