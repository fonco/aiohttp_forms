from typing import NoReturn

from aiohttp import web

from aiohttp_forms import Dispatcher
from aiohttp_forms.settings import DEFAULT_PATH, DISPATCHER_KEY, STORAGE_KEY
from aiohttp_forms.storage import BaseStorage, MemoryStorage
from aiohttp_forms.types import WebHandler
from aiohttp_forms.types.shortcuts import ExecutorFunction


class Executor:
    def __init__(
            self,
            dispatcher: Dispatcher = None,
            storage: BaseStorage = None,
            app: web.Application = None,
            path: str = None,
            handler: WebHandler = None,
            on_startup: ExecutorFunction = None,
            on_shutdown: ExecutorFunction = None,
    ) -> NoReturn:
        if not path:
            path = DEFAULT_PATH
        if not storage:
            storage = MemoryStorage(path)
        if not app:
            app = web.Application()
        if not dispatcher:
            dispatcher = Dispatcher(app=app, storage=storage, path=path)
        if handler:
            dispatcher.register_handler(handler)
        if on_startup:
            app.on_startup.append(on_startup)
        if on_shutdown:
            app.on_shutdown.append(on_shutdown)
        app[DISPATCHER_KEY] = dispatcher
        app[STORAGE_KEY] = storage
        self._dispatcher = dispatcher
        self._app = app
        self._storage = storage

    def run(self) -> NoReturn:
        web.run_app(self._app)
