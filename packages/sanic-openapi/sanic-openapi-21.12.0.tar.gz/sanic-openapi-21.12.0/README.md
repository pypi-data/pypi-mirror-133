⚠️ This package is being replaced by [Sanic Extensions](https://sanicframework.org/en/plugins/sanic-ext/getting-started.html). The project will continue to be monitored, but no new features or major development is anticipated. Sanic Extensions contains a near 1:1 upgrade if you are using Sanic OpenAPI with OAS3. Ask in the [forums](https://community.sanicframework.org/) or [discord server](https://discord.gg/FARQzAEMAA) for questions about upgrading.

# Sanic OpenAPI

[![Build Status](https://travis-ci.com/sanic-org/sanic-openapi.svg?branch=master)](https://travis-ci.com/sanic-org/sanic-openapi)
[![PyPI](https://img.shields.io/pypi/v/sanic-openapi.svg)](https://pypi.python.org/pypi/sanic-openapi/)
[![PyPI](https://img.shields.io/pypi/pyversions/sanic-openapi.svg)](https://pypi.python.org/pypi/sanic-openapi/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![codecov](https://codecov.io/gh/sanic-org/sanic-openapi/branch/master/graph/badge.svg)](https://codecov.io/gh/sanic-org/sanic-openapi)

Give your Sanic API a UI and OpenAPI documentation, all for the price of free!

![Example Swagger UI](docs/_static/images/code-to-ui.png?raw=true "Swagger UI")

Check out [open collective](https://opencollective.com/sanic-org) to learn more about helping to fund Sanic.


## Installation

```shell
pip install sanic-openapi
```

Add Swagger UI with the OpenAPI spec:

```python
from sanic_openapi import swagger_blueprint

app.blueprint(swagger_blueprint)
```

You'll now have a Swagger UI at the URL `/swagger/` and an OpenAPI 2.0 spec at `/swagger/swagger.json`.
Your routes will be automatically categorized by their blueprints.

## OpenAPI 2

Here is an example to use Sanic-OpenAPI 2:

```python
from sanic import Sanic
from sanic.response import json
from sanic_openapi import openapi2_blueprint

app = Sanic(name="AwesomeApi")
app.blueprint(openapi2_blueprint)


@app.route("/")
async def test(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

```

And you can get your Swagger document at <http://localhost:8000/swagger> like this:
![](docs/_static/images/hello_world_example.png)

## OpenAPI 3


Here is an example to use Sanic-OpenAPI 3:

```python
from sanic import Sanic
from sanic.response import json
from sanic_openapi import openapi3_blueprint

app = Sanic(name="AwesomeApi")
app.blueprint(openapi3_blueprint)


@app.route("/")
async def test(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

```

And you can get your Swagger document at <http://localhost:8000/swagger> like this:
![](docs/_static/images3/hello_world_example.png)

## Documentation

Please check the documentation on [Readthedocs](https://sanic-openapi.readthedocs.io)

## Contribution

Any contribution is welcome. If you don't know how to getting started, please check issues first and check our [Contributing Guide](CONTRIBUTING.md) to start you contribution.
