from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from config import Config


def get_model() -> BaseChatModel:
    """
    Instantiates a model based on the system configuration.

    For this simple case, it always instantiates the same model. In a real world application, it
    might create different models based on the specific context.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=Config.GOOGLE_API_KEY,
    )
