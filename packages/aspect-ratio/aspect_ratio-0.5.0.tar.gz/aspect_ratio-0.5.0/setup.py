# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aspect_ratio']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.0,<2.0.0', 'setuptools>=60.3.1,<61.0.0']

setup_kwargs = {
    'name': 'aspect-ratio',
    'version': '0.5.0',
    'description': 'Finds the aspect ratio of image',
    'long_description': '# poetry-aspect-ratio\n\n## Property\n1. Calculate aspect ratio from the given height and width.',
    'author': 'M.C.V',
    'author_email': 'murat@visiosoft.com.tr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcvarer/poetry-aspect-ratio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
