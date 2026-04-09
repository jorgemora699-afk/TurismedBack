"""
Entity: UserAnswer
==================

Representa una respuesta de un usuario a una pregunta del cuestionario.
"""


class UserAnswer:
    """
    Entidad que representa una respuesta de usuario
    """

    def __init__(self, user_id: int, question_id: int, answer_text: str,
                 answer_id: int = None):
        """
        Constructor

        Args:
            user_id: ID del usuario
            question_id: ID de la pregunta
            answer_text: Texto de la respuesta
            answer_id: ID de la respuesta (None si aún no está guardada)
        """
        self.id = answer_id
        self.user_id = user_id
        self.question_id = question_id
        self.answer_text = answer_text

    def validate(self):
        """
        Valida que la respuesta sea válida

        Raises:
            ValueError: Si la respuesta no es válida
        """
        if not self.answer_text or len(self.answer_text.strip()) == 0:
            raise ValueError("Answer text cannot be empty")

        if len(self.answer_text) > 500:
            raise ValueError("Answer text is too long (max 500 characters)")

    def to_dict(self):
        """
        Convierte la entidad a diccionario

        Returns:
            dict: Diccionario con los datos de la respuesta
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'answer_text': self.answer_text
        }

    def __repr__(self):
        return f"UserAnswer(user_id={self.user_id}, question_id={self.question_id})"
