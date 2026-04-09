"""
PostgreSQL Questionnaire Repository Implementation
===================================================

Implementación del repositorio del cuestionario para PostgreSQL.
"""

from Infrastructure.Repositories.questionnaire_repository import QuestionnaireRepository
from Domain.Entities.question import Question
from Domain.Entities.category import Category
from Domain.Entities.user_answer import UserAnswer
from Infrastructure.Database.connection import get_db_connection, close_db_connection
from typing import List, Optional


class PostgreSQLQuestionnaireRepository(QuestionnaireRepository):
    """
    Implementación del repositorio del cuestionario para PostgreSQL
    """

    def get_all_questions(self) -> List[Question]:
        """
        Obtiene todas las preguntas ordenadas con sus opciones
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, question_text, order_number
                FROM questions
                ORDER BY order_number
                """
            )

            questions_data = cursor.fetchall()

            questions = []

            for q_data in questions_data:
                # 🔹 Traer opciones de esta pregunta
                cursor.execute(
                    """
                    SELECT id, option_text
                    FROM question_options
                    WHERE question_id = %s
                    ORDER BY id
                    """,
                    (q_data['id'],)
                )

                options_data = cursor.fetchall()

                options = [
                    {
                        "id": option["id"],
                        "text": option["option_text"]
                    }
                    for option in options_data
                ]

                question = Question(
                    question_id=q_data['id'],
                    question_text=q_data['question_text'],
                    order_number=q_data['order_number'],
                    options=options
                )

                questions.append(question)

            close_db_connection(conn, cursor)

            return questions

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting questions: {str(error)}")

    def save_user_answers(self, answers: List[UserAnswer]) -> bool:
        """
        Guarda las respuestas de un usuario
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            # Insertar cada respuesta
            for answer in answers:
                cursor.execute(
                    """
                    INSERT INTO user_answers (user_id, question_id, answer_text)
                    VALUES (%s, %s, %s)
                    """,
                    (answer.user_id, answer.question_id, answer.answer_text)
                )

            conn.commit()
            close_db_connection(conn, cursor)

            return True

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error saving user answers: {str(error)}")

    def get_user_answers(self, user_id: int) -> List[UserAnswer]:
        """
        Obtiene las respuestas de un usuario
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, user_id, question_id, answer_text 
                FROM user_answers 
                WHERE user_id = %s
                ORDER BY question_id
                """,
                (user_id,)
            )

            answers_data = cursor.fetchall()

            close_db_connection(conn, cursor)

            # Convertir a entidades UserAnswer
            answers = []
            for a_data in answers_data:
                answer = UserAnswer(
                    user_id=a_data['user_id'],
                    question_id=a_data['question_id'],
                    answer_text=a_data['answer_text'],
                    answer_id=a_data['id']
                )
                answers.append(answer)

            return answers

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting user answers: {str(error)}")

    def delete_user_answers(self, user_id: int) -> bool:
        """
        Elimina las respuestas anteriores de un usuario
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM user_answers WHERE user_id = %s",
                (user_id,)
            )

            conn.commit()
            close_db_connection(conn, cursor)

            return True

        except Exception as error:
            conn.rollback()
            close_db_connection(conn, cursor)
            raise Exception(f"Error deleting user answers: {str(error)}")

    def get_all_categories(self) -> List[Category]:
        """
        Obtiene todas las categorías
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description 
                FROM categories 
                ORDER BY id
                """
            )

            categories_data = cursor.fetchall()

            close_db_connection(conn, cursor)

            # Convertir a entidades Category
            categories = []
            for c_data in categories_data:
                category = Category(
                    category_id=c_data['id'],
                    name=c_data['name'],
                    description=c_data['description']
                )
                categories.append(category)

            return categories

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting categories: {str(error)}")

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """
        Obtiene una categoría por ID
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("Could not connect to database")

        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, name, description 
                FROM categories 
                WHERE id = %s
                """,
                (category_id,)
            )

            category_data = cursor.fetchone()

            close_db_connection(conn, cursor)

            if not category_data:
                return None

            # Convertir a entidad Category
            category = Category(
                category_id=category_data['id'],
                name=category_data['name'],
                description=category_data['description']
            )

            return category

        except Exception as error:
            close_db_connection(conn, cursor)
            raise Exception(f"Error getting category: {str(error)}")
