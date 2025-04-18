from abc import ABCMeta, abstractmethod
from functools import lru_cache
import os, dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import iterate_in_threadpool
import logging

from .const import LOG_DEFAULT_LOGGER_NAME, LOG_FMT
from .utils import update_dict_with_cast

class BaseFactory(metaclass=ABCMeta):
    @abstractmethod
    @lru_cache()
    def get_app_config(self):
        """
        Each factory should define what config it wants.
        """

    def __load_local_config(self):
        dotenv.load_dotenv(dotenv_path='.env', override=True)
        update_dict_with_cast(self.get_app_config(), os.environ)

    def __setup_main_logger(self, app, logger_name=LOG_DEFAULT_LOGGER_NAME, level=logging.DEBUG):
        logger = self.__setup_logger(app, logger_name, level)
        app.logger = logger

    def __setup_logger(self, app, logger_name, level=logging.INFO):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(LOG_FMT))
        logger.addHandler(stream_handler)
        return logger

    def create_app(self):
        """
        Create an application instance.
        """
        self.__load_local_config()
        app_config = self.get_app_config()
        app = FastAPI(docs_url=app_config.get('DOCS_URL'), redoc_url=app_config.get('REDOC_URL'), openapi_url=app_config.get('OPENAPI_URL'))
        app.state.config = app_config

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self.__setup_main_logger(app, logger_name=app.state.config.get('LOGGER_NAME', LOG_DEFAULT_LOGGER_NAME), level=logging.DEBUG)

        @app.middleware("http")
        async def handle_request_headers(request: Request, call_next):
            body = await request.body()
            form = await request.form()
            app.logger.info(f"request.url: {request.url}, method: {request.method}, headers: {request.headers}, body: {body}, form: {form}")
            response = await call_next(request)
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            if response_body:
                app.logger.info(f"response_body: {response_body[0].decode()}")
            return response

        return app
