from typing import Callable, Awaitable, Optional, Union

from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse

WebHandler = Callable[[Request], Awaitable[StreamResponse]]
IdType = Optional[Union[str, int]]
