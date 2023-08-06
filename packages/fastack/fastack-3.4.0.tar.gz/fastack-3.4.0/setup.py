# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack']

package_data = \
{'': ['*']}

install_requires = \
['Werkzeug>=2.0.2,<3.0.0',
 'asgi-lifespan>=1.0.1,<2.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'fastapi>=0.70.1,<0.71.0',
 'typer>=0.4.0,<0.5.0',
 'uvicorn>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['fastack = fastack.__main__:fastack']}

setup_kwargs = {
    'name': 'fastack',
    'version': '3.4.0',
    'description': 'fastack is an intuitive framework based on FastAPI',
    'long_description': '# Fastack\n\n<p align="center">\n<a href="https://github.com/fastack-dev/fastack"><img src="https://raw.githubusercontent.com/fastack-dev/fastack/main/docs/images/logo.png" alt="Fastack"></a>\n</p>\n<p align="center">\n    <em>⚡ Fastack makes your FastAPI much easier 😎</em>\n</p>\n<p align="center">\n<img alt="PyPI" src="https://img.shields.io/pypi/v/fastack?color=%23d3de37">\n<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/fastack">\n<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastack?style=flat">\n<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/fastack?style=flat">\n<img alt="PyPI - License" src="https://img.shields.io/pypi/l/fastack?color=%2328a682">\n<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nfastack is an intuitive framework based on FastAPI, for creating clean and easy-to-manage REST API project structures. It\'s built for FastAPI framework ❤️\n\n## Features\n\n* Project layout (based on cookiecutter template)\n* Pagination support\n* Provide a `Controller` class for creating REST APIs\n* Provides command line to manage app\n* Support to access `app`, `request`, `state` globally!\n\n## Plugins\n\nList of official plugins:\n\n* [fastack-sqlmodel](https://github.com/fastack-dev/fastack-sqlmodel) - [SQLModel](https://github.com/tiangolo/sqlmodel) integration for fastack.\n* [fastack-migrate](https://github.com/fastack-dev/fastack-migrate) - [Alembic](https://alembic.sqlalchemy.org/en/latest/) integration for fastack.\n* [fastack-mongoengine](https://github.com/fastack-dev/fastack-mongoengine) - [MongoEngine](https://github.com/MongoEngine/mongoengine) integration for fastack.\n* [fastack-cache](https://github.com/fastack-dev/fastack-cache) - Caching plugin for fastack\n\n## Installation\n\n```\npip install -U fastack\n```\n\n## Example\n\ncreate project structure\n\n```\nfastack new awesome-project\ncd awesome-project\n```\n\ninstall pipenv & create virtual environment\n\n```\npip install pipenv && pipenv install && pipenv shell\n```\n\nrun app\n\n```\nfastack runserver\n```\n\n## Documentation\n\nFor the latest documentation, see the [feature/docs](https://github.com/fastack-dev/fastack/tree/feature/docs) branch.\n',
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
