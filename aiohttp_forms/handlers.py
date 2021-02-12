import aiohttp_jinja2
from aiohttp import web

from aiohttp_forms.storage import BaseStorage


@aiohttp_jinja2.template('form.html')
async def get_page(request: web.Request):
    form_id = request.match_info['form_id']
    storage: BaseStorage = request.app['storage']
    return await storage.get_form(form_id=form_id)
