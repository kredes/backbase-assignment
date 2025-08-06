"""
Entry point for the API.
"""

from fastapi import FastAPI

from api.routers import questions, healthcheck

app = FastAPI()

app.include_router(questions.router)
app.include_router(healthcheck.router)
