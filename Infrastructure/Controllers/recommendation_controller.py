"""
Recommendation Controller
=========================

Controlador para manejar las peticiones HTTP de recomendaciones.
"""

from flask import jsonify
from Application.Use_cases.recommendation.get_recommendations import GetRecommendationsUseCase
from Infrastructure.Repositories.user_repository import UserRepository
from Infrastructure.Repositories.place_repository import PlaceRepository


class RecommendationController:
    """
    Controlador de recomendaciones
    """

    def __init__(self, user_repository, place_repository, questionnaire_repository):
        self.get_recommendations_use_case = GetRecommendationsUseCase(
            user_repository,
            place_repository,
            questionnaire_repository
        )
        """
        Constructor

        Args:
            user_repository: Repositorio de usuarios
            place_repository: Repositorio de lugares
        """
        # Crear el Use Case
        self.get_recommendations_use_case = GetRecommendationsUseCase(
            user_repository,
            place_repository,
            questionnaire_repository  # ← nuevo
        )

    def get_recommendations(self, user_id):
        """
        GET /recommendations/:user_id

        Obtiene recomendaciones de lugares para un usuario

        Args:
            user_id: ID del usuario

        Returns:
            JSON response con las recomendaciones
        """
        try:
            # Validar que el ID sea número
            try:
                user_id_int = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid ID format',
                    'message': 'User ID must be a number'
                }), 400

            # Llamar al Use Case
            result = self.get_recommendations_use_case.execute(user_id_int)

            # Convertir lugares a diccionarios
            recommendations_dict = [place.to_dict()
                                    for place in result['recommendations']]

            # Retornar respuesta
            return jsonify({
                'success': True,
                'data': {
                    'user': {
                        'id': result['user'].id,
                        'name': result['user'].name,
                        'email': result['user'].email,
                        'category_id': result['category_id']
                    },
                    'recommendations': recommendations_dict,
                    'total': result['total']
                }
            }), 200

        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400

        except Exception as e:
            error_message = str(e)

            # Usuario no existe
            if 'not found' in error_message.lower():
                return jsonify({
                    'success': False,
                    'error': 'User not found',
                    'message': error_message
                }), 404

            # No ha completado cuestionario
            if 'not completed the questionnaire' in error_message.lower():
                return jsonify({
                    'success': False,
                    'error': 'Questionnaire not completed',
                    'message': error_message
                }), 400

            # Otro error
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500
