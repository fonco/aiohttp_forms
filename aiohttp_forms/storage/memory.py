from copy import deepcopy
from secrets import token_urlsafe
from typing import NoReturn

from .base import BaseStorage
from ..settings import CODE_LENGTH
from .. import exceptions


class MemoryStorage(BaseStorage):
    def __init__(self, path: str) -> NoReturn:
        self.forms = dict()
        self.path = path

    async def close(self) -> NoReturn:
        self.forms.clear()

    async def _wait_closed(self) -> NoReturn:
        pass

    def _get_unique_form_id(self) -> str:
        while True:
            if (code := token_urlsafe(CODE_LENGTH)) not in self.forms:
                return code

    async def create_form(self, form: dict) -> str:
        form_id = self._get_unique_form_id()
        form = {
            'path': self.path.format(form_id=form_id),
            'id': form_id,
            **form,
        }
        self.forms[form_id] = deepcopy(form)
        return form_id

    async def remove_form(self, form_id: str) -> NoReturn:
        try:
            del self.forms[form_id]
        except KeyError:
            raise exceptions.FormDoesntExist

    async def get_form(self, form_id: str) -> dict:
        return self.forms.get(form_id, None)
