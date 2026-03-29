from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    github_token: str
    github_webhook_secret: str
    
    class Config:
        env_file = ".env"

settings = Settings()
