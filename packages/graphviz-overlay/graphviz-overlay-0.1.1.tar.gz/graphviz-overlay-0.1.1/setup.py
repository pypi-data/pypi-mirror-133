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
    'version': '0.1.1',
    'description': 'Generate templated graphviz source files from structured data',
    'long_description': "#####\nAbout\n#####\n\nGenerate templated graphviz source files from structured data\n\nWhy\n===\n\nThe Graphviz dot language offers a descriptive and flexible way\nto define graphs of various sorts. However, I think it also has\nsome issues.\n\n- Maintenance/small changes quickly becomes a hassle, especially\n  when you want to produce similar looking graphs. I.e. highlighting\n  certain elements, or selecting specific parts (it is possible\n  to render just subgraphs, but for me that is not always what\n  I want).\n\n- The layout engine is not exactly what you would call intuitive\n  and getting it to do your bidding takes time and effort to\n  discover. Also, you need to pull (and remember those) weird\n  tricks. Basically, it's just boilerplate work.\n\n- The defaults does not really produce pretty looking graphs, and\n  customizing the design is often tedious work and for me often\n  ends up involving a bunch of copy paste. For SVG output\n  stylesheets are supported, however that doesn't really work\n  with common cooperation tools (such as slack and github)\n\nSo, to address these issues I decided to put together a tool\nto address all that (and more).\n\n\nUsage\n=====\n\nCLI\n---\n\nThe ``graphviz-overlay`` executable reads from stdin and produces\ndot source::\n\n    cat examples/simple.json | graphviz-overlay\n\n\nVersion History\n===============\n\n0.1.1:\n  - Add initial documentation and project description\n\n0.1.0:\n  - ``graph``, ``digraph`` and ``er`` commands.\n  - Support for ``--select``, ``--highlight`` and ``--shade``\n    via paths.\n  - Support for ranks\n  - External stylesheet definition.\n  - Nodes, edges, and graphs can have `classes`.\n",
    'author': 'Ronni Elken Lindsgaard',
    'author_email': 'ronni.lindsgaard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlindsgaard/graphviz-overlay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
