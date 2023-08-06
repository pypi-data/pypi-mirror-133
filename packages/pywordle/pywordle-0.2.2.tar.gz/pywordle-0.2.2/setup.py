# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywordle']

package_data = \
{'': ['*'], 'pywordle': ['words/*']}

install_requires = \
['marshmallow', 'pytz', 'requests']

entry_points = \
{'console_scripts': ['wordle = pywordle.wordle:main']}

setup_kwargs = {
    'name': 'pywordle',
    'version': '0.2.2',
    'description': 'Little helper to play the Wordle game',
    'long_description': '# Wordle\n\nThis package can help you playing playing the [Wordle](https://www.powerlanguage.co.uk/wordle/) game.\n\n## Installation\n\nThe tool can easyly be insalled on a computer where a recent (>=3.10) version of Python is present.\n\n```bash\npython3 -m venv venv\n. venv/bin/activate\npip install pywordle\n```\n\n## Usage\n\nAll the command line options can be found with the `--help` option.\n\n```bash\n$ wordle --help\nusage: Propose words for the Wordle game. [-h] [--large] [--stats] [--none] [--unique] [--check] [--verbose] [--letters LETTERS] [--minfrequency MINFREQUENCY]\n\noptions:\n  -h, --help            show this help message and exit\n  --large               Uses the large file of english words.\n  --stats               Displays some stats about the found words.\n  --none                Use none of the previously used letters.\n  --unique              Do not repeat letters in a word.\n  --check               Check that the word is valid.\n  --verbose             Print progress.\n  --letters LETTERS     The set of letters to be used.\n  --minfrequency MINFREQUENCY\n                        A minimum frequency for the proposed words, between 1 and 7.\n\n```\n\n### Letters\n\nThe `--letters` is useful to start the game with a word that is using the most common english letters to have the best chances to find letters of the solution word. It also could be a good idea to add the `--unique` option to avoid repeating a letter. Adding the `--check` will allow to check how often the words are used. This can be filtered with a `--minfrequency`. And if you do not add too many letters, you can finally add `--all` to see the full list of matching words.\n\n```bash\nwordle --letters=etaionshr --unique --check --minfrequency=3 --all\n```\n\n### Using the Words API\n\nIn order to check the validity and frequency of the words with a call to the [Words API](https://github.com/dwyl/english-words), you need to store a valid [Rapid API](https://rapidapi.com) key in `RAPIDAPI_KEY` environment variable. It is free for up to 2500 words per day. Once a word is checked, it is stored locally so it will not be checked again the next days.\n\n```bash\nexport RAPIDAPI_KEY="{YourKey}"\nwordle --check\n```\n\nChecking the words allows you to filter the proposed words by their frequency. The solution of the Wordle game tend to be a word with a high frequency.\n\n```bash\nwordle --check --minfrequency 5\n```\n',
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
