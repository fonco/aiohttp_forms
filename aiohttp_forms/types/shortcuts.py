from typing import Callable, Awaitable, Optional, Union


WebHandler = Callable
IdType = Optional[Union[str, int]]
ExecutorFunction = Callable[["Application"], Awaitable[None]]
