"""
Entity: Question
================

Representa una pregunta del cuestionario.
"""


class Question:
    """
    Entidad que representa una pregunta del cuestionario
    """

    def __init__(
        self,
        question_id: int,
        question_text: str,
        order_number: int,
        options: list = None
    ):
        """
        Constructor

        Args:
            question_id: ID de la pregunta
            question_text: Texto de la pregunta
            order_number: Orden de la pregunta (1-6)
            options: Lista de opciones
        """
        self.id = question_id
        self.question_text = question_text
        self.order_number = order_number
        self.options = options if options else []

    def to_dict(self):
        """
        Convierte la entidad a diccionario

        Returns:
            dict: Diccionario con los datos de la pregunta
        """
        return {
            'id': self.id,
            'question_text': self.question_text,
            'order_number': self.order_number,
            'options': self.options
        }

    def __repr__(self):
        return f"Question(id={self.id}, order={self.order_number})"