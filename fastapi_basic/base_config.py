from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    # Swagger docs config
    DOCS_URL: str|None = '/docs'
    REDOC_URL: str|None = '/redoc'
    OPENAPI_URL: str|None = '/openapi.json'

    # Logging config
    LOGGER_NAME: str|None = 'uvicorn'