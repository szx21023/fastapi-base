from abc import ABCMeta, abstractmethod
from functools import lru_cache
import os, dotenv

from fastapi import FastAPI

from .utils import update_dict_with_cast

class BaseFactory(metaclass=ABCMeta):
    @abstractmethod
    @lru_cache()
    def get_app_config(self):
        """
        Each factory should define what config it wants.
        """

    def create_app(self):
        """
        Create an application instance.
        """
        self.__load_local_config()
        app_config = self.get_app_config()
        app = FastAPI(docs_url=app_config.get('DOCS_URL'), redoc_url=app_config.get('REDOC_URL'), openapi_url=app_config.get('OPENAPI_URL'))
        app.state.config = app_config
        return app

    def __load_local_config(self):
        dotenv.load_dotenv(override=True)
        update_dict_with_cast(self.get_app_config(), os.environ)
