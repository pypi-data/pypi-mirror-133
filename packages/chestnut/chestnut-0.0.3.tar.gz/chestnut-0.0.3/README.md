# About

This package provides a framework to develop portable APIs. Supported platforms: Azure Functions, AWS Lambda, GPC, Flask.

## Install
```
pip install chestnut
```

## How to use
Write functions to handle your API operation using the package chestnut.http request/response classes. Then, depending on the platform you want to deploy to, add a conversion layer.

#### Develop your API
```
from chestnut.http import Request, Response


def handler(req: Request) -> Response:
	message = "Hello {} !".format(
		req.query_params.get("name", "anonymous")
	)
	return Response(status=200, body=message)

```

#### Deploy on Azure
```
import azure.functions as func
from chestnut.layers.azure import azure_layer
from <package.module> import handler


def main(req: func.HttpRequest) -> func.HttpResponse:
	return azure_layer(handler, req)

```
#### Deploy on AWS
```
from chestnut.layers.aws import aws_layer
from <package.module> import handler


def handler(event: dict, context: dict) -> dict:
	return aws_layer(handler, event)

```
#### Deploy on Google Cloud
```
import flask
from chestnut.layers.aws import gcp_layer
from <package.module> import handler


def hello_http(request: flask.Request) -> flask.Response:
	return gcp_layer(handler, request)

```

## Unit test
```
pip install -r requirements.txt -r test-requirements.txt
python -m pytest tests/ --cov=chestnut
```
