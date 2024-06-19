import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "My LLM App"
    APP_VERSION: str = "1.0.0"

    # Username and Password for login
    USER_NAME: str = os.getenv('USER_NAME', '')
    PASSWORD: str = os.getenv('PASSWORD', '')

    # API KEY
    OPENROUTER_API_KEY: str = os.getenv('OPENROUTER_API_KEY', '')

    def DB_URL(self):
        if self.ENV_MODE == "dev":
            return self.DEV_DB_URL
        return '{}://{}:{}@{}:{}/{}'.format(
            self.DB_ENGINE,
            self.DB_USERNAME,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME
        )

    def ASYNC_DB_URL(self):
        if self.ENV_MODE == "dev":
            return "sqlite+aiosqlite:///./dev.db"
        return '{}+asyncpg://{}:{}@{}:{}/{}'.format(
            self.DB_ENGINE,
            self.DB_USERNAME,
            self.DB_PASS,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME
        )
    
    def Get_API_BASE_URL(self):
        if self.ENV_MODE == "dev":
            self.API_BASE_URL = 'http://localhost:5000/'
        return self.API_BASE_URL

class DevSettings(Settings):
    # Environment mode: 'dev' or 'prod'
    ENV_MODE: str = 'dev'

    # Database settings for development
    DEV_DB_URL: str = "sqlite:///./dev.db"

    model_config = SettingsConfigDict(env_file=".env", extra='allow')

class ProdSettings(Settings):
    # Environment mode: 'dev' or 'prod'
    ENV_MODE: str = 'prod'

    # Database settings for production
    DB_ENGINE: str = os.getenv('DB_ENGINE', '')
    DB_USERNAME: str = os.getenv('DB_USERNAME', '')
    DB_PASS: str = os.getenv('DB_PASS', '')
    DB_HOST: str = os.getenv('DB_HOST', '')
    DB_PORT: str = os.getenv('DB_PORT', '')
    DB_NAME: str = os.getenv('DB_NAME', '')

    # Define API_BASE_URL based on environment mode
    API_BASE_URL: str = os.getenv('API_BASE_URL', '')

    # Database settings for production
    model_config = SettingsConfigDict(env_file=".env", extra='allow')

def get_settings(env_mode: str = "dev"):
    if env_mode == "dev":
        return DevSettings()
    return ProdSettings()