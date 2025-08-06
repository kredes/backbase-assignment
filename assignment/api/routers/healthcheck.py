from fastapi import APIRouter

from agent.model import get_model
from api.models.healthcheck import HealthCheckResponse, HealthStatus

router = APIRouter(tags=["health"])


@router.get("/health")
def healthcheck() -> HealthCheckResponse:
    """
    Validates that the underlying AI model is running.
    """

    # Check that the model is accepting requests
    model = get_model()

    try:
        model.invoke([("human", "Echo the word 'OK'")])
    except Exception:
        return HealthCheckResponse(
            status=HealthStatus.DEGRADED, message="Could not reach the AI model"
        )

    return HealthCheckResponse(status=HealthStatus.HEALTHY, message="All systems are running")
