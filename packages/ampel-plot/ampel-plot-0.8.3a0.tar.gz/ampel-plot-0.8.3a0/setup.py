# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel', 'ampel.content', 'ampel.model', 'ampel.plot']

package_data = \
{'': ['*']}

install_requires = \
['CairoSVG>=2.5.2,<3.0.0',
 'ampel-core>=0.8.3-alpha.2,<0.9.0',
 'matplotlib>=3.4.3,<4.0.0',
 'svgutils==0.3.0']

setup_kwargs = {
    'name': 'ampel-plot',
    'version': '0.8.3a0',
    'description': 'Plotting add-on for the Ampel system',
    'long_description': None,
    'author': 'Valery Brinnel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
