from typing import Optional, NoReturn

import aiohttp_jinja2
from jinja2 import FileSystemLoader
from aiohttp import web

from .views import MainView
from .storage import BaseStorage, MemoryStorage
from .types import WebHandler
from .settings import DEFAULT_PATH, BASE_DIR, HANDLER_KEY, FORMAT_VALUE, STORAGE_KEY


class Dispatcher:
    def __init__(
            self,
            app: Optional[web.Application] = None,
            path: Optional[str] = None,
            storage: Optional[BaseStorage] = None
    ) -> NoReturn:
        self._app = app
        path = self._resolve_path(path)
        self._path = path
        self._set_routes()
        if not storage:
            storage = MemoryStorage(path)
        self.storage = storage
        app[STORAGE_KEY] = storage
        self._setup_jinja()
        self.handler = None

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def path(self) -> str:
        return self._path

    def _setup_jinja(self):
        aiohttp_jinja2.setup(self._app,
                             loader=FileSystemLoader(BASE_DIR / 'templates'))

    @staticmethod
    def _resolve_path(path: Optional[str] = None) -> str:
        if not path:
            path = DEFAULT_PATH
        elif not path.startswith('/'):
            path = '/' + path
        if FORMAT_VALUE not in path:
            raise ValueError("The 'path' argument needs to contain the '{value}' string".format(value=FORMAT_VALUE))

        return path

    def _set_routes(self) -> NoReturn:
        self._app.router.add_view(self._path, MainView)

    def register_handler(self, handler: WebHandler) -> NoReturn:
        self._app[HANDLER_KEY] = handler
        self.handler = handler
