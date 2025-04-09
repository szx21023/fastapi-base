from abc import ABCMeta, abstractmethod

from fastapi import FastAPI

class BaseFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_app_config(self):
        """
        Each factory should define what config it wants.
        """

    def create_app(self):
        """
        Create an application instance.
        """
        settings = self.get_app_config()
        app = FastAPI(docs_url=settings.get('DOCS_URL'), redoc_url=settings.get('REDOC_URL'), openapi_url=settings.get('OPENAPI_URL'))
        return app