"""
Authentication Middleware
=========================

Decorador que protege rutas que requieren autenticación.

¿Qué hace?
Es un "guardián" que verifica el token ANTES de permitir acceso a una ruta.

Uso:
    @app.route('/ruta-protegida')
    @token_required  ← Este decorador protege la ruta
    def ruta_protegida(current_user):
        # Solo se ejecuta si el token es válido
        return {'user_id': current_user['user_id']}
"""

from functools import wraps
from flask import request, jsonify
from Infrastructure.auth.jwt_handler import JWTHandler


def token_required(f):
    """
    Decorador que verifica el token JWT en las peticiones

    ¿Cómo funciona?
    1. Se ejecuta ANTES de la función protegida
    2. Busca el token en el header "Authorization"
    3. Verifica que el token sea válido
    4. Si es válido → permite acceso
    5. Si NO es válido → bloquea con error 401
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # PASO 1: Buscar el token en los headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']

            # Formato esperado: "Bearer TOKEN_AQUI"
            # Ejemplo: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            try:
                # Separar "Bearer" del token
                parts = auth_header.split(" ")
                if len(parts) == 2 and parts[0] == "Bearer":
                    token = parts[1]
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid token format',
                        'message': 'Token format must be: Bearer <token>'
                    }), 401
            except IndexError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid token format',
                    'message': 'Token format must be: Bearer <token>'
                }), 401

        # PASO 2: Verificar que el token exista
        if not token:
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'message': 'Token is missing. Please provide a token in Authorization header.'
            }), 401

        # PASO 3: Verificar que el token sea válido
        try:
            # Desencriptar y verificar el token
            payload = JWTHandler.verify_token(token)
            current_user = payload

        except Exception as e:
            # Token inválido o expirado
            return jsonify({
                'success': False,
                'error': 'Authentication failed',
                'message': str(e)
            }), 401

        # PASO 4: Token válido → Pasar el usuario a la función
        # Ahora la función puede acceder a current_user
        return f(current_user, *args, **kwargs)

    return decorated
