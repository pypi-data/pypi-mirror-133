# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywordle']

package_data = \
{'': ['*'], 'pywordle': ['words/*']}

install_requires = \
['marshmallow>=3.14.1,<4.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['wordle = pywordle.wordle:main']}

setup_kwargs = {
    'name': 'pywordle',
    'version': '0.1.8',
    'description': 'Little helper to play the Wordle game',
    'long_description': '# Wordle\n\n## Description\n\nThis is to help playing the [Wordle](https://www.powerlanguage.co.uk/wordle/) game.\n\n## Usage\n\nAll the command line options can be found with the `--help` option.\n\n```bash\nubuntu@tab-pcg-ubuntu:~/wordle$ poetry run wordle --help\nusage: Propose the next word at the Wordle game. [-h] [--all] [--none] [--unique] [--check] [--verbose] [--letters LETTERS] [--minfrequency MINFREQUENCY]\n\noptions:\n  -h, --help            show this help message and exit\n  --all                 Displays the full list of available words.\n  --none                Use none of the previously used letters.\n  --unique              Do not repeat letters in a word.\n  --check               Check that the word is valid.\n  --verbose             Print progress.\n  --letters LETTERS     The set of letters to be used.\n  --minfrequency MINFREQUENCY\n                        A minimum frequency for the proposed words, between 1 and 7.\n```\n\n### Check the Words API\n\nIn order to call the [Words API](https://github.com/dwyl/english-words) below, you need to store a valid [Rapid API](https://rapidapi.com) key in `RAPIDAPI_KEY` environment variable. This can be done with the `secret.sh` if available in the repository:\n\n```bash\n. secret.sh\n```\n\nUsing the `--check` option will check all proposed words with the [Words API](https://github.com/dwyl/english-words). Be carefull that we only have 2500 free queries per day. After that it will automatically cost $0.004 per extra word. But it is also quite easy to check the status current of the [usage](https://rapidapi.com/developer/dashboard).\n\n```bash\npoetry run wordle --check\n```\n\n### Letters\n\nThe `--letters` is useful to start the game with a word that is using the most common english letters to have the best chances to find letters of the solution word. It also could be a good idea to add the `--unique` option to avoid repeating a letter. Adding the `--check` will allow to check how often the words are used. This can be filtered with a `--minfrequency`. And if you do not add too many letters, you can finally add `--all` to see the full list of matching words.\n\n```bash\npoetry run wordle --letters=etaionshr --unique --check --minfrequency=3 --all\n```\n\n## Development\n\nThe python depedencies are handled with Poetry.\n\n```bash\npoetry install\n```\n\n### Unit tests\n\nThis is how to run the unit tests and generate the JUnit report.\n\n```bash\npoetry run pytest --junitxml=test-reports/report.xml\n```\n\n### Check the types\n\nThis is done with [mypy](https://mypy.readthedocs.io/en/latest/index.html)\n\n```bash\npoetry run mypy *.py\n```\n\n### Check the syntax\n\nThis is done with [pylint](https://pypi.org/project/pylint/)\n\n```bash\npoetry run pylint *.py\n```\n\n### Initial word list\n\nThe initial list is taken from [Github](https://github.com/dwyl/english-words). But it contains many word that hardly exist.\n\n### Safety\n\nIn order to test that all the dependencies have no known issues, we are experimenting with [Safety](https://pypi.org/project/safety/) that compares our dependencies to the [Satefty DB](https://github.com/pyupio/safety-db).\n\nChecking the safety of the installed packages is done as follow:\n\n```bash\npoetry run safety check\n```\n\n`Poetry` makes it easy to upgrade to the latest packages. It will update the `poetry.lock` and even the `pyproject.toml` accordingly.\n\n```bash\npoetry update\n```\n\n### Publish to Pypi\n\nOn Pypi, this package is called `pywordle`. It is very simple to publish it with `poetry`:\n\n```bash\npoetry install\npoetry build\npoetry publish\n```\n\nThen it can be used with `pip` for example:\n\n```bash\npip instal pywordle\nwordle --help\n```\n',
    'author': 'Pierre Cart-Grandjean',
    'author_email': 'pcart-grandjea@noreply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
