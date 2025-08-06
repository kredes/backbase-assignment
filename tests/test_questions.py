from fastapi.testclient import TestClient

INVALID_QUESTION_ANSWER = "Not a math or history question"


def test_ask_math_question(client: TestClient) -> None:
    question = "Who was the first president of the united states?"

    response = client.post("/ask", json={"question": question})

    assert response.status_code == 200
    assert response.json()["answer"] != INVALID_QUESTION_ANSWER


def test_ask_history_question(client: TestClient) -> None:
    question = "Who invented graph theory?"

    response = client.post("/ask", json={"question": question})

    assert response.status_code == 200
    assert response.json()["answer"] != INVALID_QUESTION_ANSWER


def test_ask_invalid_question(client: TestClient) -> None:
    question = "What are the most popular spots in Amsterdam?"

    response = client.post("/ask", json={"question": question})

    assert response.status_code == 400
    assert response.json()["answer"] == INVALID_QUESTION_ANSWER
