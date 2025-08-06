from enum import auto, StrEnum

from pydantic import BaseModel


class HealthStatus(StrEnum):
    HEALTHY = auto()
    DEGRADED = auto()


class HealthCheckResponse(BaseModel):
    """
    Response from the `/health` endpoint.
    """

    status: HealthStatus
    message: str
