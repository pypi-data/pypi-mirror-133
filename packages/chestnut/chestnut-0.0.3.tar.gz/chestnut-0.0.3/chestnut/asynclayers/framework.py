from typing import Callable, Awaitable
from chestnut.http import Request


async def framework_layer(
	request_converter: Callable,
	response_converter: Callable,
	handler: Awaitable,
	req: Request
):
	return response_converter(await handler(request_converter(req)))
