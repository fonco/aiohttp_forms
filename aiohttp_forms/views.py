import aiohttp_jinja2
from aiohttp import web

from aiohttp_forms.settings import FORMAT_VALUE, STORAGE_KEY, HANDLER_KEY
from aiohttp_forms.storage import BaseStorage


class MainView(web.View):
    @aiohttp_jinja2.template('form.html')
    async def get(self):
        form_id = self.request.match_info[FORMAT_VALUE]
        storage: BaseStorage = self.request.app[STORAGE_KEY]
        return await storage.get_form(form_id=form_id)

    async def post(self):
        form_id = self.request.match_info[FORMAT_VALUE]
        app = self.request.app
        storage = app[STORAGE_KEY]
        data = await self.request.post()
        handler = app[HANDLER_KEY]
        error = await handler(data=data, storage=storage, form_id=form_id)
        if error:
            return {'error': error}
        return None
