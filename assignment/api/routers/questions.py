from fastapi import APIRouter, Response

from api.models.questions import UserQuestion, AnswerResponse, QuestionType
from agent.util import ask_question_to_agent

router = APIRouter(tags=["questions"])


@router.post("/ask")
def ask_question(data: UserQuestion, response: Response) -> AnswerResponse:
    """
    Answers the given question, if valid.

    This API can only answer questions related to math or history. Any other questions won't
    receive an answer.
    """
    # TODO: Handle exceptions
    # It's proven quite difficult to find accurate documentation about which exceptions might be
    # raised here. For simplicity, let's assume that any errors happening at this point are due to
    # improper configuration on our side, since user input is quite simple. If so, returning a
    # 500 error (default for uncaught exceptions) seems appropriate.
    agent_response = ask_question_to_agent(data.question)

    if not agent_response["is_valid_question"]:
        response.status_code = 400
        return AnswerResponse(
            answer="Not a math or history question",
            is_valid_question=False,
            question_type=QuestionType.OTHER,
        )

    return AnswerResponse.model_validate(agent_response)
