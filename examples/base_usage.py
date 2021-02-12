from aiohttp import web

import logging

from aiohttp_forms import exceptions
from aiohttp_forms.executor import Executor
from aiohttp_forms.settings import STORAGE_KEY
from aiohttp_forms.storage import BaseStorage


async def form_handler(data: dict, storage: BaseStorage, form_id: str):
    print(data)
    print(storage)
    try:
        await storage.remove_form(form_id)
    except exceptions.FormDoesntExist:
        return 'Form does not exist'
    else:
        return 'Biba'


async def main(app: web.Application):
    form = {
        'title': 'Example Form',
        'fields': {
            'first_name': {
                'name': 'First Name',
                'type': 'text',
                'value': '',
            },
            'second_name': {
                'name': 'Second Name',
                'type': 'text',
                'value': '',
            },
        },
        'button': 'SEND',
    }
    form_id = await app[STORAGE_KEY].create_form(form=form)
    print(form_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Executor(path='form-{form_id}/', handler=form_handler, on_startup=main).run()
