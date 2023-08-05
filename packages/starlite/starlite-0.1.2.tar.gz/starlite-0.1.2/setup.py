# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlite', 'starlite.openapi', 'starlite.utils']

package_data = \
{'': ['*']}

install_requires = \
['openapi-schema-pydantic',
 'orjson',
 'pydantic',
 'pydantic-factories',
 'python-multipart',
 'pyyaml',
 'requests',
 'starlette',
 'typing-extensions']

setup_kwargs = {
    'name': 'starlite',
    'version': '0.1.2',
    'description': 'Light-weight and flexible ASGI API Framework',
    'long_description': '<img alt="Starlite logo" src="./starlite-logo.svg" width=100%, height="auto">\n\n<div align="center">\n\n![PyPI - License](https://img.shields.io/pypi/l/starlite?color=blue)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/starlite)\n\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_starlite&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Goldziher_starlite)\n[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_starlite&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Goldziher_starlite)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_starlite&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Goldziher_starlite)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_starlite&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Goldziher_starlite)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_starlite&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=Goldziher_starlite)\n[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Goldziher_starlite&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Goldziher_starlite)\n\n[![Discord](https://img.shields.io/discord/919193495116337154?color=blue&label=chat%20on%20discord&logo=discord)](https://discord.gg/X3FJqy8d2j)\n</div>\n\n# Starlite\n\nStarlite is a light, opinionated and flexible ASGI API framework built on top\nof [pydantic](https://github.com/samuelcolvin/pydantic) and [Starlette](https://github.com/encode/starlette).\n\nCheck out the [Starlite documentation 📚](https://goldziher.github.io/starlite/)\n\n## Core Features\n\n* 👉 OpenAPI 3.1 schema generation\n* 👉 built-in [Redoc](https://github.com/Redocly/redoc) based OpenAPI UI\n* 👉 class based controllers\n* 👉 decorators based configuration\n* 👉 extended testing support\n* 👉 extensive typing support including inference, validation and parsing\n* 👉 full async (ASGI) support\n* 👉 layered dependency injection\n* 👉 route guards based authorization\n* 👉 simple middleware and authentication\n* 👉 support for pydantic models and pydantic dataclasses\n* 👉 support for standard library dataclasses\n* 👉 ultra-fast json serialization and deserialization using [orjson](https://github.com/ijl/orjson)\n\n## Installation\n\nUsing your package manager of choice:\n\n```shell\npip install starlite\n```\n\nOR\n\n```sh\npoetry add starlite\n```\n\nOR\n\n```sh\npipenv install starlite\n```\n\n## Minimal Example\n\nDefine your data model using pydantic or any library based on it (see for example ormar, beanie, SQLModel etc.):\n\n```python title="my_app/models/user.py"\nfrom pydantic import BaseModel, UUID4\n\n\nclass User(BaseModel):\n    first_name: str\n    last_name: str\n    id: UUID4\n```\n\nYou can alternatively use a dataclass, either the standard library one or the one from pydantic:\n\n```python title="my_app/models/user.py"\nfrom uuid import UUID\n\n# from pydantic.dataclasses import dataclass\nfrom dataclasses import dataclass\n\n@dataclass\nclass User:\n    first_name: str\n    last_name: str\n    id: UUID\n```\n\nDefine a Controller for your data model:\n\n```python title="my_app/controllers/user.py"\nfrom pydantic import UUID4\nfrom starlite.controller import Controller\nfrom starlite.handlers import get, post, put, patch, delete\nfrom starlite.types import Partial\n\nfrom my_app.models import User\n\n\nclass UserController(Controller):\n    path = "/users"\n\n    @post()\n    async def create(self, data: User) -> User:\n        ...\n\n    @get()\n    async def get_users(self) -> list[User]:\n        ...\n\n    @patch(path="/{user_id:uuid}")\n    async def partial_update_user(self, user_id: UUID4, data: Partial[User]) -> User:\n        ...\n\n    @put(path="/{user_id:uuid}")\n    async def update_user(self, user_id: UUID4, data: list[User]) -> list[User]:\n        ...\n\n    @get(path="/{user_id:uuid}")\n    async def get_user_by_id(self, user_id: UUID4) -> User:\n        ...\n\n    @delete(path="/{user_id:uuid}")\n    async def delete_user_by_id(self, user_id: UUID4) -> User:\n        ...\n\n```\n\nImport your controller into your application\'s entry-point and pass it to Starlite when instantiating your app:\n\n```python title="my_app/main.py"\nfrom starlite import Starlite\n\nfrom my_app.controllers.user import UserController\n\napp = Starlite(route_handlers=[UserController])\n```\n\nTo run you application, use an ASGI server such as [uvicorn](https://www.uvicorn.org/):\n\n```shell\nuvicorn my_app.main:app --reload\n```\n\n### Contributing\n\nStarlite is open to contributions big and small. You can always [join our discord](https://discord.gg/X3FJqy8d2j) server\nto discuss contributions and project maintenance. For guidelines on how to contribute, please\nsee [the contribution guide](CONTRIBUTING.md).\n',
    'author': "Na'aman Hirschfeld",
    'author_email': 'Naaman.Hirschfeld@sprylab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Goldziher/starlite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
