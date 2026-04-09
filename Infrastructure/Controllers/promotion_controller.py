"""
Promotion Controller
====================

Controlador para manejar las peticiones HTTP de promociones.
"""

from flask import request, jsonify
from Application.Use_cases.promotion.generate_promotion import GeneratePromotionUseCase
from Application.Use_cases.promotion.validate_promotion import ValidatePromotionUseCase
from Application.Use_cases.promotion.redeem_promotion import RedeemPromotionUseCase
from Application.Use_cases.promotion.get_user_promotions import GetUserPromotionsUseCase
from Infrastructure.Repositories.promotion_repository import PromotionRepository
from Infrastructure.Repositories.user_repository import UserRepository
from Infrastructure.auth.role_checker import require_admin


class PromotionController:
    """
    Controlador de promociones
    """

    def __init__(self, promotion_repository: PromotionRepository,
                 user_repository: UserRepository):
        """
        Constructor

        Args:
            promotion_repository: Repositorio de promociones
            user_repository: Repositorio de usuarios
        """
        # Crear los Use Cases
        self.generate_promotion_use_case = GeneratePromotionUseCase(
            promotion_repository)
        self.validate_promotion_use_case = ValidatePromotionUseCase(
            promotion_repository)
        self.redeem_promotion_use_case = RedeemPromotionUseCase(
            promotion_repository,
            user_repository
        )
        self.get_user_promotions_use_case = GetUserPromotionsUseCase(
            promotion_repository)
        self.promotion_repository = promotion_repository

    def generate_promotion(self, current_user):
        try:
            error = require_admin(current_user)
            if error:
                return error

            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided',
                    'message': 'Request body is empty'
                }), 400

            description = data.get('description')
            discount_percentage = data.get('discount_percentage')
            discount_amount = data.get('discount_amount')
            max_uses = data.get('max_uses', 1)
            expires_in_days = data.get('expires_in_days', 30)
            custom_code = data.get('code') or data.get('custom_code')  # ← acepta 'code' también
            place_id = data.get('place_id')  # ← NUEVO

            promotion = self.generate_promotion_use_case.execute(
                description=description,
                discount_percentage=discount_percentage,
                discount_amount=discount_amount,
                max_uses=max_uses,
                expires_in_days=expires_in_days,
                custom_code=custom_code,
                place_id=place_id  # ← NUEVO
            )

            return jsonify({
                'success': True,
                'message': 'Promotion generated successfully',
                'data': promotion.to_dict()
            }), 201

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
        
    def validate_promotion(self, code):
        """
        GET /promotions/validate/:code

        Valida si un código promocional es válido

        Args:
            code: Código de la promoción

        Returns:
            JSON response indicando si es válido
        """
        try:
            # Llamar al Use Case
            result = self.validate_promotion_use_case.execute(code)

            # Si el código no existe
            if result['promotion'] is None:
                return jsonify({
                    'success': False,
                    'data': {
                        'valid': False,
                        'message': result['message']
                    }
                }), 404  # ← NOT FOUND

            # Si el código existe pero no es válido
            if not result['valid']:
                return jsonify({
                    'success': False,
                    'data': {
                        'valid': False,
                        'message': result['message'],
                        'promotion': result['promotion'].to_dict()
                    }
                }), 400  # ← BAD REQUEST (código inválido/expirado/agotado)

            # Código válido
            return jsonify({
                'success': True,
                'data': {
                    'valid': True,
                    'message': result['message'],
                    'promotion': result['promotion'].to_dict()
                }
            }), 200  # ← OK

        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': str(e)
            }), 500  # ← SERVER ERROR

    def redeem_promotion(self):
        """
        POST /promotions/redeem

        Redime un código promocional
        SIN autenticación JWT

        Request JSON esperado:
        {
            "user_id": 5,
            "code": "BIENVENIDA2024"
        }

        Returns:
            JSON response con el resultado de la redención
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

            # Extraer user_id y code del body
            user_id = data.get('user_id')
            code = str(data.get('code')).strip()

            # Validar que vengan ambos campos
            if not user_id:
                return jsonify({
                    'success': False,
                    'error': 'Missing user_id',
                    'message': 'User ID is required'
                }), 400

            if not code:
                return jsonify({
                    'success': False,
                    'error': 'Missing code',
                    'message': 'Promotion code is required'
                }), 400

            # Validar que user_id sea número
            try:
                user_id = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid user_id',
                    'message': 'User ID must be a number'
                }), 400

            # Llamar al Use Case
            result = self.redeem_promotion_use_case.execute(user_id, code)

            if result['success']:
                response_data = {
                    'success': True,
                    'message': result['message'],
                    'data': {
                        'promotion': result['promotion'].to_dict(),
                        'redemption': result['redemption'].to_dict()
                    }
                }
                return jsonify(response_data), 200
            else:
                response_data = {
                    'success': False,
                    'error': 'Redemption failed',
                    'message': result['message']
                }

                if result['promotion']:
                    response_data['promotion'] = result['promotion'].to_dict()

                return jsonify(response_data), 400

        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400

        except Exception as e:
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
        
    def delete_promotion(self, current_user, promotion_id):
        try:
            error = require_admin(current_user)
            if error:
                return error

            try:
                promotion_id = int(promotion_id)
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid ID'}), 400

            self.promotion_repository.delete(promotion_id)

            return jsonify({
                'success': True,
                'message': f'Promotion {promotion_id} deleted successfully'
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': str(e)
            }), 500

    def get_user_promotions(self, current_user, user_id):
        """
        GET /promotions/user/:user_id

        Obtiene las promociones redimidas por un usuario

        Args:
            user_id: ID del usuario (viene de la URL)

        Returns:
            JSON response con las promociones redimidas
        """
        try:
            # Validar que user_id sea número
            try:
                user_id = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid user_id',
                    'message': 'User ID must be a number'
                }), 400

            # Llamar al Use Case
            redemptions = self.get_user_promotions_use_case.execute(user_id)

            return jsonify({
                'success': True,
                'data': {
                    'user_id': user_id,
                    'redemptions': redemptions,
                    'total': len(redemptions)
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

    def get_all_active(self):
        """
        GET /promotions/active

        Obtiene todas las promociones activas

        Returns:
            JSON response con las promociones activas
        """
        try:
            # Llamar al repositorio directamente
            promotions = self.promotion_repository.get_all_active()

            promotions_dict = [p.to_dict() for p in promotions]

            return jsonify({
                'success': True,
                'data': {
                    'promotions': promotions_dict,
                    'total': len(promotions_dict)
                }
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': str(e)
            }), 500
