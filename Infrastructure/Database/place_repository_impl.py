"""
PostgreSQL Place Repository Implementation
===========================================

Implementación del repositorio de lugares para PostgreSQL.
"""

from Infrastructure.Repositories.place_repository import PlaceRepository
from Domain.Entities.place import Place
from Infrastructure.Database.connection import get_db_connection, close_db_connection
from typing import List, Optional


class PostgreSQLPlaceRepository(PlaceRepository):
    """
    Implementación del repositorio de lugares para PostgreSQL
    """

    def create(self, place: Place) -> Place:
        """
        Crea un nuevo lugar en PostgreSQL
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO places 
                (name, description, address, phone, category_id, place_type, 
                 price_range, rating, image_url, opening_hours, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name, description, address, phone, category_id, 
                          place_type, price_range, rating, image_url, 
                          opening_hours, is_active, created_at
                """,
                (place.name, place.description, place.address, place.phone,
                 place.category_id, place.place_type, place.price_range,
                 place.rating, place.image_url, place.opening_hours, place.is_active)
            )

            place_data = cursor.fetchone()
            conn.commit()
            close_db_connection(conn, cursor)

            return self._map_to_place(place_data)

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error creating place: {str(error)}")

    def find_by_id(self, place_id: int) -> Optional[Place]:
        """
        Busca un lugar por ID
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description, address, phone, category_id,
                       place_type, price_range, rating, image_url,
                       opening_hours, is_active, created_at
                FROM places
                WHERE id = %s
                """,
                (place_id,)
            )

            place_data = cursor.fetchone()
            close_db_connection(conn, cursor)

            if not place_data:
                return None

            return self._map_to_place(place_data)

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error finding place: {str(error)}")

    def get_all_active(self) -> List[Place]:
        """
        Obtiene todos los lugares activos
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description, address, phone, category_id,
                       place_type, price_range, rating, image_url,
                       opening_hours, is_active, created_at
                FROM places
                WHERE is_active = TRUE
                ORDER BY rating DESC, name
                """
            )

            places_data = cursor.fetchall()
            close_db_connection(conn, cursor)

            places = []
            for p_data in places_data:
                places.append(self._map_to_place(p_data))

            return places

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting active places: {str(error)}")

    def find_by_category(self, category_id: int) -> List[Place]:
        """
        Busca lugares por categoría
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description, address, phone, category_id,
                       place_type, price_range, rating, image_url,
                       opening_hours, is_active, created_at
                FROM places
                WHERE category_id = %s AND is_active = TRUE
                ORDER BY rating DESC, name
                """,
                (category_id,)
            )

            places_data = cursor.fetchall()
            close_db_connection(conn, cursor)

            places = []
            for p_data in places_data:
                places.append(self._map_to_place(p_data))

            return places

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error finding places by category: {str(error)}")

    def find_by_type(self, place_type: str) -> List[Place]:
        """
        Busca lugares por tipo
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description, address, phone, category_id,
                       place_type, price_range, rating, image_url,
                       opening_hours, is_active, created_at
                FROM places
                WHERE place_type = %s AND is_active = TRUE
                ORDER BY rating DESC, name
                """,
                (place_type,)
            )

            places_data = cursor.fetchall()
            close_db_connection(conn, cursor)

            places = []
            for p_data in places_data:
                places.append(self._map_to_place(p_data))

            return places

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error finding places by type: {str(error)}")
        
    def remove_place_reference(self, place_id: int):
        """
        Quita la referencia al lugar en todas las promociones
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE promotions SET place_id = NULL WHERE place_id = %s",
                (place_id,)
            )
            conn.commit()
            close_db_connection(conn, cursor)
        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error removing place reference: {str(error)}")

    def search_by_name(self, name: str) -> List[Place]:
        """
        Busca lugares por nombre (búsqueda parcial)
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description, address, phone, category_id,
                       place_type, price_range, rating, image_url,
                       opening_hours, is_active, created_at
                FROM places
                WHERE name ILIKE %s AND is_active = TRUE
                ORDER BY rating DESC, name
                """,
                (f"%{name}%",)  # ILIKE = case-insensitive LIKE
            )

            places_data = cursor.fetchall()
            close_db_connection(conn, cursor)

            places = []
            for p_data in places_data:
                places.append(self._map_to_place(p_data))

            return places

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error searching places by name: {str(error)}")

    def update(self, place: Place) -> Place:
        """
        Actualiza un lugar
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE places
                SET name = %s,
                    description = %s,
                    address = %s,
                    phone = %s,
                    category_id = %s,
                    place_type = %s,
                    price_range = %s,
                    rating = %s,
                    image_url = %s,
                    opening_hours = %s
                WHERE id = %s
                RETURNING id, name, description, address, phone, category_id,
                          place_type, price_range, rating, image_url,
                          opening_hours, is_active, created_at
                """,
                (place.name, place.description, place.address, place.phone,
                 place.category_id, place.place_type, place.price_range,
                 place.rating, place.image_url, place.opening_hours, place.id)
            )

            place_data = cursor.fetchone()
            conn.commit()
            close_db_connection(conn, cursor)

            return self._map_to_place(place_data)

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error updating place: {str(error)}")

    def deactivate(self, place_id: int) -> bool:
        """
        Desactiva un lugar (soft delete)
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE places SET is_active = FALSE WHERE id = %s",
                (place_id,)
            )

            conn.commit()
            close_db_connection(conn, cursor)

            return True

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error deactivating place: {str(error)}")

    def delete(self, place_id: int) -> bool:
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")
        cursor = conn.cursor()
        try:
            # Primero quitar referencias en promociones
            cursor.execute(
                "UPDATE promotions SET place_id = NULL WHERE place_id = %s",
                (place_id,)
            )
            # Luego eliminar el lugar
            cursor.execute(
                "DELETE FROM places WHERE id = %s",
                (place_id,)
            )
            rows_deleted = cursor.rowcount
            conn.commit()
            close_db_connection(conn, cursor)
            if rows_deleted == 0:
                raise Exception(f"Place with ID {place_id} not found")
            return True
        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error deleting place: {str(error)}")

    def _map_to_place(self, data: dict) -> Place:
        """
        Mapea datos de la BD a entidad Place
        """
        return Place(
            place_id=data['id'],
            name=data['name'],
            description=data['description'],
            address=data['address'],
            phone=data['phone'],
            category_id=data['category_id'],
            place_type=data['place_type'],
            price_range=data['price_range'],
            rating=data['rating'],
            image_url=data['image_url'],
            opening_hours=data['opening_hours'],
            is_active=data['is_active'],
            created_at=data['created_at']
        )
