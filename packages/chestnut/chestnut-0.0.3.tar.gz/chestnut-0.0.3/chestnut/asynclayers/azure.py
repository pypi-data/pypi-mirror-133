from typing import Callable, Awaitable
from chestnut.layers.azure import azure_to_request, response_to_azure
from .framework import framework_layer
import azure.functions as func


async def azure_layer(handler: Awaitable, req: func.HttpRequest) -> func.HttpResponse:
	return await framework_layer(azure_to_request, response_to_azure, handler, req)
