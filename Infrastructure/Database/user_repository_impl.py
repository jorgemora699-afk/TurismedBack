"""
PostgreSQL User Repository Implementation
==========================================

Esta es la IMPLEMENTACIÓN del contrato UserRepository.

Aquí SÍ conocemos PostgreSQL, SQL, psycopg2, etc.
Esta capa es la ÚNICA que habla con la base de datos.

Si mañana cambias a MongoDB, solo cambias este archivo
(y las demás capas siguen igual).
"""

from Infrastructure.Repositories.user_repository import UserRepository
from Domain.Entities.user import User
from Infrastructure.Database.connection import get_db_connection, close_db_connection
from typing import Optional


class PostgreSQLUserRepository(UserRepository):
    """
    Implementación del repositorio de usuarios para PostgreSQL

    Implementa todos los métodos definidos en UserRepository
    """

    def save(self, user: User) -> User:
        """
        Guarda un usuario en PostgreSQL

        Args:
            user: Usuario a guardar

        Returns:
            User: Usuario guardado con ID asignado
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            # Ejecutar INSERT en PostgreSQL
            cursor.execute(
                """
                INSERT INTO users (name, email, password, phone, has_completed_questionnaire, role) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                RETURNING id, name, email, phone, category_id, has_completed_questionnaire, created_at, role
                """,
                (user.name, user.email, user.password,
                 user.phone, user.has_completed_questionnaire, user.role)
            )

            # Obtener el usuario recién creado (con ID asignado por PostgreSQL)
            saved_user_data = cursor.fetchone()

            # Confirmar la transacción
            conn.commit()

            # Convertir el resultado de PostgreSQL a una entidad User
            saved_user = User(
                user_id=saved_user_data['id'],
                name=saved_user_data['name'],
                email=saved_user_data['email'],
                password=user.password,
                phone=saved_user_data['phone'],
                category_id=saved_user_data['category_id'],
                has_completed_questionnaire=saved_user_data['has_completed_questionnaire'],
                role=saved_user_data['role']
            )

            close_db_connection(conn, cursor)

            return saved_user

        except Exception as error:
            # Si hay error, revertir cambios
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error saving user: {str(error)}")

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por email en PostgreSQL

        Args:
            email: Email a buscar

        Returns:
            User si existe, None si no existe
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            # Ejecutar SELECT en PostgreSQL
            cursor.execute(
                """
                SELECT id, name, email, password, phone, category_id, has_completed_questionnaire, role 
                FROM users 
                WHERE email = %s
                """,
                (email,)
            )

            user_data = cursor.fetchone()

            close_db_connection(conn, cursor)

            # Si no existe, retornar None
            if not user_data:
                return None

            # Convertir el resultado de PostgreSQL a una entidad User
            user = User(
                user_id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                phone=user_data['phone'],
                category_id=user_data['category_id'],
                has_completed_questionnaire=user_data['has_completed_questionnaire'],
                role=user_data['role']
            )

            return user

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error finding user by email: {str(error)}")

    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por ID en PostgreSQL

        Args:
            user_id: ID del usuario

        Returns:
            User si existe, None si no existe
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, email, password, phone, category_id, has_completed_questionnaire, role 
                FROM users 
                WHERE id = %s
                """,
                (user_id,)
            )

            user_data = cursor.fetchone()

            close_db_connection(conn, cursor)

            if not user_data:
                return None

            user = User(
                user_id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                phone=user_data['phone'],
                category_id=user_data['category_id'],
                has_completed_questionnaire=user_data['has_completed_questionnaire'],
                role=user_data['role']
            )

            return user

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error finding user by ID: {str(error)}")

    def email_exists(self, email: str) -> bool:
        """
        Verifica si un email existe en PostgreSQL

        Args:
            email: Email a verificar

        Returns:
            True si existe, False si no existe
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)",
                (email,)
            )

            result = cursor.fetchone()

            close_db_connection(conn, cursor)

            # result es algo como: {'exists': True} o {'exists': False}
            return result['exists']

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error checking if email exists: {str(error)}")
        
    def get_all(self):
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT id, name, email, phone, role, category_id, 
                    has_completed_questionnaire, created_at 
                FROM users 
                ORDER BY created_at DESC
                """
            )
            users_data = cursor.fetchall()
            close_db_connection(conn, cursor)
            users = []
            for u in users_data:
                users.append(User(
                    user_id=u['id'],
                    name=u['name'],
                    email=u['email'],
                    password='',
                    phone=u['phone'],
                    category_id=u['category_id'],
                    has_completed_questionnaire=u['has_completed_questionnaire'],
                    role=u['role']
                ))
            return users
        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting users: {str(error)}")

    def update(self, user: User) -> User:
        """
        Actualiza un usuario en PostgreSQL

        Args:
            user: Usuario con los datos actualizados

        Returns:
            User: Usuario actualizado
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            # Ejecutar UPDATE en PostgreSQL
            # Actualizamos: nombre, email, teléfono, categoría y estado del cuestionario
            cursor.execute(
                """
                UPDATE users 
                SET name = %s, 
                    email = %s,
                    phone = %s, 
                    category_id = %s, 
                    has_completed_questionnaire = %s
                WHERE id = %s
                RETURNING id, name, email, password, phone, category_id,
                      has_completed_questionnaire, created_at, role
            """,
                (user.name, user.email, user.phone, user.category_id,
                 user.has_completed_questionnaire, user.id)
            )

            # Obtener el usuario actualizado
            updated_user_data = cursor.fetchone()

            # Confirmar la transacción
            conn.commit()

            # Convertir el resultado a entidad User
            updated_user = User(
                user_id=updated_user_data['id'],
                name=updated_user_data['name'],
                email=updated_user_data['email'],
                password=user.password,  # Mantener la contraseña que ya tenía
                phone=updated_user_data['phone'],
                category_id=updated_user_data['category_id'],
                has_completed_questionnaire=updated_user_data['has_completed_questionnaire'],
                role=updated_user_data['role']
            )

            close_db_connection(conn, cursor)

            return updated_user

        except Exception as error:
            # Si hay error, revertir cambios
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error updating user: {str(error)}")

    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario de PostgreSQL

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            # Ejecutar DELETE en PostgreSQL
            cursor.execute(
                "DELETE FROM users WHERE id = %s",
                (user_id,)
            )

            # Verificar cuántas filas se eliminaron
            rows_deleted = cursor.rowcount

            # Confirmar la transacción
            conn.commit()

            close_db_connection(conn, cursor)

            # Si no se eliminó ninguna fila, el usuario no existía
            if rows_deleted == 0:
                raise Exception(f"User with ID {user_id} not found")

            return True

        except Exception as error:
            # Si hay error, revertir cambios
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error deleting user: {str(error)}")
