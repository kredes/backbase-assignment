from typing import cast

from agent.graph import agent, State


def ask_question_to_agent(question: str) -> State:
    """
    Util function to invoke the agent.
    """
    return cast(State, agent.invoke({"question": question}))
