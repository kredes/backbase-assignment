from enum import auto, StrEnum

from pydantic import BaseModel


class UserQuestion(BaseModel):
    """
    Model accepted by the `/ask` endpoint as its input.
    """

    question: str


class QuestionType(StrEnum):
    MATH = auto()
    HISTORY = auto()
    OTHER = auto()


class AnswerResponse(BaseModel):
    """
    Response returned by the `/ask` endpoint with the agent's answer.
    """

    question_type: QuestionType
    is_valid_question: bool
    answer: str
