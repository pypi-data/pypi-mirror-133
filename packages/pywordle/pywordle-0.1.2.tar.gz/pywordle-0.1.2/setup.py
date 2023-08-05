# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wordle']
install_requires = \
['marshmallow>=3.14.1,<4.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['wordle = wordle:main']}

setup_kwargs = {
    'name': 'pywordle',
    'version': '0.1.2',
    'description': 'https://www.powerlanguage.co.uk/wordle/',
    'long_description': None,
    'author': 'Pierre Cart-Grandjean',
    'author_email': 'pcart-grandjea@noreply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
