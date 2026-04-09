"""
Role Checker
============

Funciones para verificar permisos según el rol del usuario.
"""

from flask import jsonify


def is_admin(current_user: dict) -> bool:
    """
    Verifica si el usuario es administrador

    Args:
        current_user: Usuario del token JWT

    Returns:
        bool: True si es admin
    """
    return current_user.get('role') == 'admin'


def can_modify_user(current_user: dict, target_user_id: int) -> bool:
    """
    Verifica si el usuario puede modificar a otro usuario

    Reglas:
    - Admin: Puede modificar a cualquiera
    - Usuario normal: Solo puede modificarse a sí mismo

    Args:
        current_user: Usuario del token JWT
        target_user_id: ID del usuario a modificar

    Returns:
        bool: True si puede modificar
    """
    # Admin puede modificar a cualquiera
    if is_admin(current_user):
        return True

    # Usuario solo puede modificarse a sí mismo
    return current_user['user_id'] == target_user_id


def can_delete_user(current_user: dict, target_user_id: int) -> bool:
    """
    Verifica si el usuario puede ELIMINAR a otro usuario

    Reglas:
    - Admin: Puede eliminar a cualquiera
    - Usuario normal: NO puede eliminar (ni siquiera a sí mismo)

    Args:
        current_user: Usuario del token JWT
        target_user_id: ID del usuario a eliminar

    Returns:
        bool: True si puede eliminar
    """
    # Solo admin puede eliminar usuarios
    return is_admin(current_user)


def require_admin(current_user: dict):
    """
    Verifica que el usuario sea admin o retorna error 403

    Args:
        current_user: Usuario del token JWT

    Returns:
        tuple: (error_response, 403) si no es admin, None si es admin
    """
    if not is_admin(current_user):
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': 'Admin privileges required'
        }), 403

    return None
