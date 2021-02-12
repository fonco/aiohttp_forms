from typing import Optional, NoReturn

import aiohttp_jinja2
from jinja2 import FileSystemLoader
from aiohttp import web

from .handlers import get_page
from .storage import BaseStorage, MemoryStorage
from .types import WebHandler
from .settings import DEFAULT_PATH, BASE_DIR


class Dispatcher:
    def __init__(
            self, app: Optional[web.Application] = None,
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
        app['storage'] = storage
        self._setup_jinja()

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
        if '{form_id}' not in path:
            raise ValueError("The 'path' argument needs to contain the '{form_id}' string")

        return path

    def _set_routes(self) -> NoReturn:
        self._app.router.add_get(path=self._path, handler=get_page)

    async def register_handler(self, handler: WebHandler) -> NoReturn:
        self._app.router.add_post(path=self._path, handler=handler)
        for route in self._app.router.routes():
            print(route, route.handler)
