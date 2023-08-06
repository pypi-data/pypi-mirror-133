# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphviz_overlay', 'graphviz_overlay.overlays']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.19.1,<0.20.0']

entry_points = \
{'console_scripts': ['graphviz-overlay = graphviz_overlay.graph:run']}

setup_kwargs = {
    'name': 'graphviz-overlay',
    'version': '0.1.0',
    'description': 'Generate templated graphviz source files from structured data',
    'long_description': None,
    'author': 'Ronni Elken Lindsgaard',
    'author_email': 'ronni.lindsgaard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
