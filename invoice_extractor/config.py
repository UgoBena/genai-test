from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    mistral_model: str = "mistral-large-latest"
    mistral_api_key: str = "cxOA2qqFm6OmiPNUioiBTqwanCTgO5pR"
    mistral_model_temperature: float = 0.0


settings = Settings()
