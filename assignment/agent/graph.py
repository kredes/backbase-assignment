from enum import auto
from typing import TypedDict

from langchain_core.runnables.configurable import StrEnum
from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.model import get_model
from agent.prompts import (
    QUESTION_TYPE_CHECKER_SYSTEM_PROMPT,
    MATH_MODEL_SYSTEM_PROMPT,
    HISTORY_MODEL_SYSTEM_PROMPT,
)


class InputState(TypedDict):
    """
    The initial state of the system.
    """

    question: str


class State(InputState):
    """
    The state used to pass information between nodes.
    """

    question_type: str
    is_valid_question: bool
    answer: str


class Node(StrEnum):
    """
    An enum of valid nodes.
    """

    CHECK_QUESTION_TYPE = auto()
    ANSWER_MATH_QUESTION = auto()
    ANSWER_HISTORY_QUESTION = auto()


def check_question_type_node(state: State):
    """
    Call the LLM to determine the type (math, history or other) of a question.
    """
    model = get_model()

    response = model.invoke(
        [("system", QUESTION_TYPE_CHECKER_SYSTEM_PROMPT), ("human", state["question"])]
    )

    is_valid_question = True
    if not any(_type in response.content for _type in ("math", "history")):
        is_valid_question = False

    return {"question_type": response.content, "is_valid_question": is_valid_question}


def answer_math_question_node(state: State):
    """
    Call the LLM to answer a math question.
    """
    model = get_model()

    response = model.invoke([("system", MATH_MODEL_SYSTEM_PROMPT), ("human", state["question"])])

    answer = response.content

    return {"answer": answer}


def answer_history_question_node(state: State):
    """
    Call the LLM to answer a history question.
    """
    model = get_model()

    response = model.invoke([("system", HISTORY_MODEL_SYSTEM_PROMPT), ("human", state["question"])])

    answer = response.content

    return {"answer": answer}


def route_question_type(state: State) -> str:
    """
    Determines which node to call next based on the question type.
    """
    question_type = state["question_type"]

    next_nodes = {
        "math": Node.ANSWER_MATH_QUESTION,
        "history": Node.ANSWER_HISTORY_QUESTION,
    }

    return next_nodes.get(question_type, END)


graph = StateGraph(State, input_schema=InputState)

graph.add_node(Node.CHECK_QUESTION_TYPE, check_question_type_node)
graph.add_node(Node.ANSWER_MATH_QUESTION, answer_math_question_node)
graph.add_node(Node.ANSWER_HISTORY_QUESTION, answer_history_question_node)

# We start by checking the question type
graph.set_entry_point(Node.CHECK_QUESTION_TYPE)

# Route to the appropriate node based on the question type
graph.add_conditional_edges(Node.CHECK_QUESTION_TYPE, route_question_type)

# After answering the question, we're done
graph.add_edge(Node.ANSWER_MATH_QUESTION, END)
graph.add_edge(Node.ANSWER_HISTORY_QUESTION, END)

agent = graph.compile()
