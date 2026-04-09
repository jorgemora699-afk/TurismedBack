"""
Place Controller
================

Controlador para manejar las peticiones HTTP de lugares.
"""

from flask import request, jsonify
from Application.Use_cases.place.create_place import CreatePlaceUseCase
from Application.Use_cases.place.get_place_by_id import GetPlaceByIdUseCase
from Application.Use_cases.place.get_all_places import GetAllPlacesUseCase
from Application.Use_cases.place.get_places_by_category import GetPlacesByCategoryUseCase
from Application.Use_cases.place.update_place import UpdatePlaceUseCase
from Application.Use_cases.place.delete_place import DeletePlaceUseCase
from Infrastructure.Repositories.place_repository import PlaceRepository
from Infrastructure.auth.role_checker import require_admin


class PlaceController:
    """
    Controlador de lugares
    """

    def __init__(self, place_repository: PlaceRepository):
        """
        Constructor

        Args:
            place_repository: Repositorio de lugares
        """
        # Crear los Use Cases
        self.create_place_use_case = CreatePlaceUseCase(place_repository)
        self.get_place_by_id_use_case = GetPlaceByIdUseCase(place_repository)
        self.get_all_places_use_case = GetAllPlacesUseCase(place_repository)
        self.get_places_by_category_use_case = GetPlacesByCategoryUseCase(
            place_repository)
        self.update_place_use_case = UpdatePlaceUseCase(place_repository)
        self.delete_place_use_case = DeletePlaceUseCase(place_repository)
        self.place_repository = place_repository

    def create_place(self, current_user):
        """
        POST /places

        Crea un nuevo lugar
        SOLO ADMIN puede crear lugares

        Args:
            current_user: Usuario del token JWT

        Request JSON esperado:
        {
            "name": "La Trattoria",
            "description": "Auténtica cocina italiana",
            "address": "Calle 10 #5-25",
            "phone": "3001234567",
            "category_id": 1,
            "place_type": "restaurant",
            "price_range": 2,
            "rating": 4.5,
            "image_url": "https://...",
            "opening_hours": "Lun-Dom 12:00-22:00"
        }

        Returns:
            JSON response con el lugar creado
        """
        try:
            # ✅ VERIFICAR QUE SEA ADMIN
            error = require_admin(current_user)
            if error:
                return error

            # Obtener datos del request
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided',
                    'message': 'Request body is empty'
                }), 400

            # Extraer campos (solo name es obligatorio)
            name = data.get('name')

            if not name:
                return jsonify({
                    'success': False,
                    'error': 'Missing name',
                    'message': 'Place name is required'
                }), 400

            # Llamar al Use Case
            place = self.create_place_use_case.execute(
                name=name,
                description=data.get('description'),
                address=data.get('address'),
                phone=data.get('phone'),
                category_id=data.get('category_id'),
                place_type=data.get('place_type'),
                price_range=data.get('price_range'),
                rating=data.get('rating'),
                image_url=data.get('image_url'),
                opening_hours=data.get('opening_hours')
            )

            return jsonify({
                'success': True,
                'message': 'Place created successfully',
                'data': place.to_dict()
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

    def get_place(self, place_id):
        """
        GET /places/:id

        Obtiene un lugar por ID

        Args:
            place_id: ID del lugar

        Returns:
            JSON response con el lugar
        """
        try:
            # Validar que el ID sea número
            try:
                place_id_int = int(place_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid ID format',
                    'message': 'Place ID must be a number'
                }), 400

            # Llamar al Use Case
            place = self.get_place_by_id_use_case.execute(place_id_int)

            return jsonify({
                'success': True,
                'data': place.to_dict()
            }), 200

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
                    'error': 'Place not found',
                    'message': error_message
                }), 404

            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500

    def get_all_places(self):
        """
        GET /places

        Obtiene todos los lugares activos

        Query params opcionales:
        - category_id: Filtrar por categoría
        - type: Filtrar por tipo (restaurant, nightclub, cafe, bar)
        - search: Buscar por nombre

        Returns:
            JSON response con lista de lugares
        """
        try:
            # Obtener parámetros de query
            category_id = request.args.get('category_id')
            place_type = request.args.get('type')
            search = request.args.get('search')

            # Filtrar según parámetros
            if category_id:
                try:
                    category_id_int = int(category_id)
                    places = self.get_places_by_category_use_case.execute(
                        category_id_int)
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid category_id',
                        'message': 'Category ID must be a number'
                    }), 400

            elif place_type:
                places = self.place_repository.find_by_type(place_type)

            elif search:
                places = self.place_repository.search_by_name(search)

            else:
                # Sin filtros, obtener todos
                places = self.get_all_places_use_case.execute()

            # Convertir a diccionarios
            places_dict = [p.to_dict() for p in places]

            return jsonify({
                'success': True,
                'data': {
                    'places': places_dict,
                    'total': len(places_dict)
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

    def update_place(self, current_user, place_id):
        """
        PATCH /places/:id

        Actualiza un lugar
        REQUIERE SER ADMIN

        Args:
            current_user: Usuario del token JWT
            place_id: ID del lugar

        Returns:
            JSON response con el lugar actualizado
        """
        try:
            # ✅ VERIFICAR QUE SEA ADMIN
            error = require_admin(current_user)
            if error:
                return error

            # Validar que el ID sea número
            try:
                place_id_int = int(place_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid ID format',
                    'message': 'Place ID must be a number'
                }), 400

            # Obtener datos del request
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided',
                    'message': 'Provide at least one field to update'
                }), 400

            # Llamar al Use Case
            place = self.update_place_use_case.execute(
                place_id=place_id_int,
                name=data.get('name'),
                description=data.get('description'),
                address=data.get('address'),
                phone=data.get('phone'),
                category_id=data.get('category_id'),
                place_type=data.get('place_type'),
                price_range=data.get('price_range'),
                rating=data.get('rating'),
                image_url=data.get('image_url'),
                opening_hours=data.get('opening_hours')
            )

            return jsonify({
                'success': True,
                'message': 'Place updated successfully',
                'data': place.to_dict()
            }), 200

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
                    'error': 'Place not found',
                    'message': error_message
                }), 404

            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500

    def delete_place(self, current_user, place_id):
        """
        DELETE /places/:id

        Elimina  un lugar
        REQUIERE SER ADMIN

        Args:
            current_user: Usuario del token JWT
            place_id: ID del lugar

        Returns:
            JSON response con confirmación
        """
        try:
            # ✅ VERIFICAR QUE SEA ADMIN
            error = require_admin(current_user)
            if error:
                return error

            # Validar que el ID sea número
            try:
                place_id_int = int(place_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid ID format',
                    'message': 'Place ID must be a number'
                }), 400

            self.place_repository.remove_place_reference(place_id_int)
            
            # Llamar al Use Case
            self.delete_place_use_case.execute(place_id_int)

            return jsonify({
                'success': True,
                'message': f'Place with ID {place_id_int} deleted successfully'
            }), 200

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
                    'error': 'Place not found',
                    'message': error_message
                }), 404

            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500
