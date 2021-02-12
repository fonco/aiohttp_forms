class BaseStorage:
    async def close(self):
        """
        You have to override this method and use when application shutdowns.
        Perhaps you would like to save data and etc.
        """
        raise NotImplementedError

    async def _wait_closed(self):
        """
        You have to override this method for all asynchronous storages (e.g., Redis).
        """
        raise NotImplementedError

    async def create_form(self, form: dict) -> str:
        raise NotImplementedError

    async def get_form(self, form_id: str):
        raise NotImplementedError
