"""
PostgreSQL Promotion Repository Implementation
===============================================

Implementación del repositorio de promociones para PostgreSQL.
"""

from Infrastructure.Repositories.promotion_repository import PromotionRepository
from Domain.Entities.promotion import Promotion
from Domain.Entities.redemption import Redemption
from Infrastructure.Database.connection import get_db_connection, close_db_connection
from typing import List, Optional


class PostgreSQLPromotionRepository(PromotionRepository):
    """
    Implementación del repositorio de promociones para PostgreSQL
    """

    def create(self, promotion: Promotion) -> Promotion:
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO promotions 
                (code, description, discount_percentage, discount_amount, 
                 max_uses, current_uses, is_active, expires_at, place_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, code, description, discount_percentage, discount_amount,
                          max_uses, current_uses, is_active, expires_at, created_at,
                          place_id
                """,
                (promotion.code, promotion.description, promotion.discount_percentage,
                 promotion.discount_amount, promotion.max_uses, promotion.current_uses,
                 promotion.is_active, promotion.expires_at, promotion.place_id)
            )

            promotion_data = cursor.fetchone()
            conn.commit()

            # Obtener el nombre del lugar si tiene place_id
            place_name = None
            if promotion_data['place_id']:
                cursor2 = conn.cursor()
                cursor2.execute("SELECT name FROM places WHERE id = %s", (promotion_data['place_id'],))
                place_data = cursor2.fetchone()
                if place_data:
                    place_name = place_data['name']
                cursor2.close()

            close_db_connection(conn, cursor)

            promo = self._map_to_promotion(promotion_data)
            promo.place_name = place_name
            return promo

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error creating promotion: {str(error)}")

    def find_by_id(self, promotion_id: int) -> Optional[Promotion]:
        """
        Busca una promoción por ID
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT p.id, p.code, p.description, p.discount_percentage, p.discount_amount,
                    p.max_uses, p.current_uses, p.is_active, p.expires_at, p.created_at,
                    p.place_id, pl.name as place_name
                FROM promotions AS p
                LEFT JOIN places AS pl ON p.place_id = pl.id
                WHERE p.id = %s
                """,
                (promotion_id,)
            )

            promotion_data = cursor.fetchone()
            close_db_connection(conn, cursor)

            if not promotion_data:
                return None

            return self._map_to_promotion(promotion_data)

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error finding promotion: {str(error)}")

    def find_by_code(self, code: str) -> Optional[Promotion]:
        """
        Busca una promoción por código
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT p.id, p.code, p.description, p.discount_percentage, p.discount_amount,
                    p.max_uses, p.current_uses, p.is_active, p.expires_at, p.created_at,
                    p.place_id, pl.name as place_name
                FROM promotions AS p
                LEFT JOIN places AS pl ON p.place_id = pl.id
                WHERE p.code = %s::varchar
                """,
                (code,)
            )

            promotion_data = cursor.fetchone()
            close_db_connection(conn, cursor)

            if not promotion_data:
                return None

            return self._map_to_promotion(promotion_data)

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error finding promotion: {str(error)}")

    def get_all_active(self) -> List[Promotion]:
        """
        Obtiene todas las promociones activas
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT p.id, p.code, p.description, p.discount_percentage, p.discount_amount,
                    p.max_uses, p.current_uses, p.is_active, p.expires_at, p.created_at,
                    p.place_id, pl.name as place_name
                FROM promotions p
                LEFT JOIN places pl ON p.place_id = pl.id
                WHERE p.is_active = TRUE
                ORDER BY p.created_at DESC
                """
            )

            promotions_data = cursor.fetchall()
            close_db_connection(conn, cursor)

            promotions = []
            for p_data in promotions_data:
                promotions.append(self._map_to_promotion(p_data))

            return promotions

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting active promotions: {str(error)}")

    def update(self, promotion: Promotion) -> Promotion:
        """
        Actualiza una promoción
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE promotions
                SET description = %s,
                    discount_percentage = %s,
                    discount_amount = %s,
                    max_uses = %s,
                    is_active = %s,
                    expires_at = %s
                WHERE id = %s
                RETURNING id, code, description, discount_percentage, discount_amount,
                        max_uses, current_uses, is_active, expires_at, created_at,
                        place_id
                """,
                (promotion.description, promotion.discount_percentage,
                promotion.discount_amount, promotion.max_uses, promotion.is_active,
                promotion.expires_at, promotion.id)
            )

            promotion_data = cursor.fetchone()
            conn.commit()
            close_db_connection(conn, cursor)

            return self._map_to_promotion(promotion_data)

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error updating promotion: {str(error)}")

    def deactivate(self, promotion_id: int) -> bool:
        """
        Desactiva una promoción
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE promotions SET is_active = FALSE WHERE id = %s",
                (promotion_id,)
            )

            conn.commit()
            close_db_connection(conn, cursor)

            return True

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error deactivating promotion: {str(error)}")
        
    def delete(self, promotion_id: int) -> bool:
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM promotions WHERE id = %s", (promotion_id,))
            rows_deleted = cursor.rowcount
            conn.commit()
            close_db_connection(conn, cursor)
            if rows_deleted == 0:
                raise Exception(f"Promotion with ID {promotion_id} not found")
            return True
        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error deleting promotion: {str(error)}")

    def redeem(self, user_id: int, promotion_id: int) -> Redemption:
        """
        Redime una promoción para un usuario
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            # 1. Insertar redención
            cursor.execute(
                """
                INSERT INTO redemptions (user_id, promotion_id)
                VALUES (%s, %s)
                RETURNING id, user_id, promotion_id, redeemed_at
                """,
                (user_id, promotion_id)
            )

            redemption_data = cursor.fetchone()

            # 2. Incrementar current_uses de la promoción
            cursor.execute(
                """
                UPDATE promotions
                SET current_uses = current_uses + 1
                WHERE id = %s
                """,
                (promotion_id,)
            )

            conn.commit()
            close_db_connection(conn, cursor)

            return Redemption(
                redemption_id=redemption_data['id'],
                user_id=redemption_data['user_id'],
                promotion_id=redemption_data['promotion_id'],
                redeemed_at=redemption_data['redeemed_at']
            )

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error redeeming promotion: {str(error)}")

    def user_has_redeemed(self, user_id: int, promotion_id: int) -> bool:
        """
        Verifica si un usuario ya redimió una promoción
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT COUNT(*) as count
                FROM redemptions
                WHERE user_id = %s AND promotion_id = %s
                """,
                (user_id, promotion_id)
            )

            result = cursor.fetchone()
            close_db_connection(conn, cursor)

            return result['count'] > 0

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error checking redemption: {str(error)}")

    def get_user_redemptions(self, user_id: int) -> List[dict]:
        """
        Obtiene las redenciones de un usuario con datos de la promoción
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT 
                    r.id as redemption_id,
                    r.redeemed_at,
                    p.id as promotion_id,
                    p.code,
                    p.description,
                    p.discount_percentage,
                    p.discount_amount
                FROM redemptions r
                JOIN promotions p ON r.promotion_id = p.id
                WHERE r.user_id = %s
                ORDER BY r.redeemed_at DESC
                """,
                (user_id,)
            )

            redemptions_data = cursor.fetchall()
            close_db_connection(conn, cursor)

            redemptions = []
            for r_data in redemptions_data:
                redemptions.append({
                    'redemption_id': r_data['redemption_id'],
                    'redeemed_at': r_data['redeemed_at'].isoformat(),
                    'promotion': {
                        'id': r_data['promotion_id'],
                        'code': r_data['code'],
                        'description': r_data['description'],
                        'discount_percentage': r_data['discount_percentage'],
                        'discount_amount': float(r_data['discount_amount']) if r_data['discount_amount'] else None
                    }
                })

            return redemptions

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting user redemptions: {str(error)}")

    def _map_to_promotion(self, data: dict) -> Promotion:
        """
        Mapea datos de la BD a entidad Promotion
        """
        return Promotion(
            promotion_id=data['id'],
            code=data['code'],
            description=data['description'],
            discount_percentage=data['discount_percentage'],
            discount_amount=data['discount_amount'],
            max_uses=data['max_uses'],
            current_uses=data['current_uses'],
            is_active=data['is_active'],
            expires_at=data['expires_at'],
            created_at=data['created_at'],
            place_id=data.get('place_id'),        
            place_name=data.get('place_name'),    
        )
