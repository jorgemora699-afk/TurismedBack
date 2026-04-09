"""
User Controller
===============

El CONTROLLER es el punto de entrada HTTP.

Responsabilidades:
1. Recibir peticiones HTTP (request)
2. Extraer los datos del JSON
3. Validar que vengan los datos necesarios
4. Llamar al Use Case correspondiente
5. Convertir el resultado a JSON (response)
6. Manejar errores y retornar códigos HTTP correctos

El controller NO tiene lógica de negocio.
Solo coordina entre HTTP y Use Cases.
"""

from flask import request, jsonify
from Application.Use_cases.user.register_user import RegisterUserUseCase
from Application.Use_cases.user.login_user import LoginUserUseCase
from Application.Use_cases.user.get_user_by_id import GetUserByIdUseCase
from Application.Use_cases.user.update_user import UpdateUserUseCase
from Application.Use_cases.user.delete_user import DeleteUserUseCase
from Infrastructure.Repositories.user_repository import UserRepository
from Infrastructure.auth.jwt_handler import JWTHandler
from Infrastructure.auth.role_checker import can_modify_user, can_delete_user
from Application.Use_cases.user.get_all_users import GetAllUsersUseCase


class UserController:
    """
    Controlador de usuarios

    Maneja las peticiones HTTP relacionadas con usuarios
    """

    def __init__(self, user_repository: UserRepository):
        """
        Constructor

        Args:
            user_repository: Repositorio de usuarios (inyectado)
        """
        # Crear los Use Cases con el repositorio inyectado
        self.register_use_case = RegisterUserUseCase(user_repository)
        self.login_use_case = LoginUserUseCase(user_repository)
        self.get_user_by_id_use_case = GetUserByIdUseCase(user_repository)
        self.update_user_use_case = UpdateUserUseCase(user_repository)
        self.delete_user_use_case = DeleteUserUseCase(user_repository)
        self.get_all_users_use_case = GetAllUsersUseCase(user_repository)

    def register(self):
        """
        POST /users/register

        Maneja la petición de registro de usuario

        Request JSON esperado:
            {
                "name": "María López",
                "email": "maria@email.com",
                "password": "123456",
                "phone": "3001234567"  (opcional)
            }

        Returns:
            JSON response con el usuario creado o error
        """
        try:
            # Paso 1: Obtener los datos del request
            data = request.get_json()

            # Paso 2: Validar que vengan los campos requeridos
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided',
                    'message': 'Request body is empty'
                }), 400

            # Extraer campos
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')

            # Validar campos requeridos
            if not name or not email or not password:
                return jsonify({
                    'success': False,
                    'error': 'Missing required fields',
                    'message': 'Name, email and password are required'
                }), 400

            # Paso 3: Llamar al Use Case
            user = self.register_use_case.execute(
                name=name,
                email=email,
                password=password,
                phone=phone
            )

            # Paso 4: Convertir el resultado a JSON y retornar
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'data': user.to_dict()
            }), 201  # 201 = Created

        except ValueError as e:
            # Errores de validación (de la entidad User)
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'message': str(e)
            }), 400  # 400 = Bad Request

        except Exception as e:
            # Cualquier otro error (email duplicado, error de BD, etc.)
            error_message = str(e)

            # Si es error de email duplicado, retornar 409 (Conflict)
            if 'already registered' in error_message.lower():
                return jsonify({
                    'success': False,
                    'error': 'Email already exists',
                    'message': error_message
                }), 409  # 409 = Conflict

            # Error genérico del servidor
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500  # 500 = Internal Server Error

    def login(self):
        """
        POST /users/login

        Maneja la petición de login

        Request JSON esperado:
        {
            "email": "maria@email.com",
            "password": "123456"
        }

        Returns:
            JSON response con los datos del usuario o error
        """
        try:
            # Paso 1: Obtener los datos del request
            data = request.get_json()

            # Paso 2: Validar que vengan los campos requeridos
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'No data provided',
                    'message': 'Request body is empty'
                }), 400

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return jsonify({
                    'success': False,
                    'error': 'Missing credentials',
                    'message': 'Email and password are required'
                }), 400

            # Paso 3: Llamar al Use Case
            user = self.login_use_case.execute(
                email=email,
                password=password
            )

            # Paso 4: Generar token JWT (NUEVO)
            token = JWTHandler.generate_token(user.id, user.email, user.role)

            # Paso 5: Retornar usuario Y token
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'user': user.to_dict(),
                    'token': token  # ← NUEVO: Incluye el token
                }
            }), 200

        except Exception as e:
            # Error de credenciales inválidas
            error_message = str(e)

            if 'invalid' in error_message.lower():
                return jsonify({
                    'success': False,
                    'error': 'Invalid credentials',
                    'message': error_message
                }), 401  # 401 = Unauthorized

            # Error genérico
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500

    def get_user_by_id(self, user_id):
        """
        GET /users/:id

        Obtiene un usuario por su ID

        Args:
            user_id: ID del usuario a buscar

        Returns:
            JSON response con los datos del usuario o error
        """
        try:
            # Paso 1: Validar que el ID sea un número
            try:
                user_id_int = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid ID format',
                    'message': 'User ID must be a number'
                }), 400

            # Paso 2: Llamar al Use Case
            user = self.get_user_by_id_use_case.execute(user_id_int)

            # Paso 3: Retornar el usuario
            return jsonify({
                'success': True,
                'data': user.to_dict()
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
                }), 404  # 404 = Not Found

            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500

    def get_all_users(self, current_user):
        try:
            # Verificar si current_user es dict o objeto
            role = current_user.get('role') if isinstance(current_user, dict) else current_user.role
            
            if role != 'admin':
                return jsonify({
                    'success': False,
                    'error': 'Forbidden',
                    'message': 'Only administrators can list users'
                }), 403

            users = self.get_all_users_use_case.execute()

            return jsonify({
                'success': True,
                'data': [u.to_dict() for u in users]
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': str(e)
            }), 500
    
    def update_user(self, current_user, user_id):
        """
        PATCH /users/:id

        Actualiza información de un usuario

        Request JSON esperado:
        {
            "name": "Juan Pérez Actualizado",  (opcional)
            "email": "nuevo@email.com",        (opcional)
            "phone": "3009876543"              (opcional)
        }

        Args:
            user_id: ID del usuario a actualizar

        Returns:
            JSON response con el usuario actualizado o error
        """
        try:
            # Paso 1: Validar que el ID sea un número
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
                    'message': 'You can only update your own account (unless you are admin)'
                }), 403

            # Paso 2: Obtener los datos del request
            data = request.get_json()

            # Validar que venga al menos un campo para actualizar
            if not data or (not data.get('name') and not data.get('email') and not data.get('phone')):
                return jsonify({
                    'success': False,
                    'error': 'No data to update',
                    'message': 'Provide at least name or phone to update'
                }), 400

            # Extraer campos opcionales
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')

            # Paso 3: Llamar al Use Case
            user = self.update_user_use_case.execute(
                user_id=user_id_int,
                name=name,
                email=email,
                phone=phone
            )

            # Paso 4: Retornar el usuario actualizado
            return jsonify({
                'success': True,
                'message': 'User updated successfully',
                'data': user.to_dict()
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

    def delete_user(self, current_user, user_id):
        """
        DELETE /users/:id

        Elimina un usuario del sistema
        SOLO ADMIN puede eliminar usuarios

        Args:
            current_user: Usuario del token JWT
            user_id: ID del usuario a eliminar

        Returns:
            JSON response con confirmación o error
        """
        try:
            # Paso 1: Validar que el ID sea un número
            try:
                user_id_int = int(user_id)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid ID format',
                    'message': 'User ID must be a number'
                }), 400

            # Paso 2: VERIFICAR PERMISOS (SOLO ADMIN)
            if not can_delete_user(current_user, user_id_int):
                return jsonify({
                    'success': False,
                    'error': 'Forbidden',
                    'message': 'Only administrators can delete users'
                }), 403

            # Paso 3: Llamar al Use Case
            self.delete_user_use_case.execute(user_id_int)

            # Paso 4: Retornar confirmación
            return jsonify({
                'success': True,
                'message': f'User with ID {user_id_int} deleted successfully'
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
                    'error': 'User not found',
                    'message': error_message
                }), 404

            return jsonify({
                'success': False,
                'error': 'Server error',
                'message': error_message
            }), 500
