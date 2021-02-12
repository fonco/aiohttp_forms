from aiohttp import web

import logging

from aiohttp_forms.dispatcher import Dispatcher


async def form_handler(request: web.Request):  # TODO The handler is called twice.
    data = await request.post()
    form_id = request.match_info['form_id']
    storage = request.app['storage']
    form = await storage.get_form(form_id=form_id)
    chat, user = form.get('chat'), form.get('user')
    print(data)
    print(chat, user)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    web_path = 'form-{form_id}/'
    dp = Dispatcher(
        app=app,
        path=web_path,
    )
    await dp.register_handler(form_handler)
    form = {
        'title': 'Example Form',
        'chat': 1,
        'user': 1,
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
        }
    }
    form_id = await dp.storage.create_form(form=form)
    path = dp.path.format(form_id=form_id)
    print(path)
    return app


if __name__ == '__main__':
    web.run_app(main())
