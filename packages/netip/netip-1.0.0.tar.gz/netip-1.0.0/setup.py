# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['netip']
setup_kwargs = {
    'name': 'netip',
    'version': '1.0.0',
    'description': 'Print a user ipv4 in youre code.',
    'long_description': None,
    'author': 'OwoNicoo',
    'author_email': '86409467+DiscordBotML@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9.6,<4.0.0',
}


setup(**setup_kwargs)
