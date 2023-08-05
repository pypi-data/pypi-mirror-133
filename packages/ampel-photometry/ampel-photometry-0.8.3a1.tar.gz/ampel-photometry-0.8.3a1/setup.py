# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel', 'ampel.abstract', 'ampel.aux', 'ampel.demo', 'ampel.t1', 'ampel.view']

package_data = \
{'': ['*']}

install_requires = \
['ampel-core>=0.8.3-alpha.1,<0.9.0', 'ampel-interface>=0.8.3-alpha.1,<0.9.0']

extras_require = \
{':extra == "docs"': ['tomlkit>=0.8.0,<0.9.0'],
 'docs': ['Sphinx>=3.5.1,<5.0.0', 'sphinx-autodoc-typehints>=1.11.1,<2.0.0']}

setup_kwargs = {
    'name': 'ampel-photometry',
    'version': '0.8.3a1',
    'description': 'Photometry add-on for the Ampel system',
    'long_description': None,
    'author': 'Valery Brinnel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
