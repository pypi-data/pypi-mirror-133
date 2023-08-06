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
    'version': '0.2.3',
    'description': 'Little helper to play the Wordle game',
    'long_description': '# Wordle\n\nThis package can help you playing the [Wordle](https://www.powerlanguage.co.uk/wordle/) game. It will not play for you. You will still have to choose the best strategy.\n\n## Installation\n\nThe tool can easily be installed on a computer where a recent (>=3.10) version of Python is present.\n\n```bash\npython3 -m venv venv\n. venv/bin/activate\npip install pywordle\n```\n\n## Usage\n\nEach time that you want to enter a new word, you will ask the tool to provide a list of candidates. When you have selected a word, type it in as well as the result provided by the `Wordle` game. The code values for the result colours are:\n\n* Dark gray: 0\n* Yellow: 1\n* Green: 2\n\nHere is an example:\n\n```bash\n$ wordle --letters=etaions --unique\nHere is the list of 14 possibilities: [\'aeons\', \'anise\', \'atone\', \'eosin\', \'inset\', \'iotas\', \'noise\', \'notes\', \'onset\', \'saint\', \'satin\', \'stain\', \'stone\', \'tones\']\nPlease enter the word played:\nnoise\nPlease enter the result:\n20001\nSaving result for \'noise\': [2, 0, 0, 0, 1]\n```\n\nThe result will be stored in today\'s game file and be used next time you call the tool, limiting the possibilities. Just type `Enter`, if you do not want to choose a word just yet.\n\nAll the command line options can be found with the `--help` option.\n\n```bash\n$ wordle --help\nusage: Propose words for the Wordle game. [-h] [--large] [--stats] [--none] [--unique] [--check] [--verbose] [--letters LETTERS] [--minfrequency MINFREQUENCY]\n\noptions:\n  -h, --help            show this help message and exit\n  --large               Uses the large file of English words.\n  --stats               Displays some stats about the found words.\n  --none                Use none of the previously used letters.\n  --unique              Do not repeat letters in a word.\n  --check               Check that the word is valid.\n  --verbose             Print progress.\n  --letters LETTERS     The set of letters to be used.\n  --minfrequency MINFREQUENCY\n                        A minimum frequency for the proposed words, between 1 and 7.\n\n```\n\n### Letters\n\nThe `--letters` is useful to start the game with a word that is using the most common English letters to have the best chances to find letters of the solution word. It also could be a good idea to add the `--unique` option to avoid repeating a letter.\n\n```bash\nwordle --letters=etaionshr --unique\n```\n\n### None\n\nThis is a different strategy. Instead of looking for a possible word, you are trying to look for information on letters that you have not used yet today. This is not possible if you have selected the `Hard Mode`. It only makes sense to use the option for the second and possibly third word. Again the `--unique` option will give you more information.\n\n```bash\nwordle --none --unique\n```\n\n### Stats\n\nThis will give you some statistics in the list of proposed words. First you will get the most used letters in that list. Then you will get the words that used the most used letters. This is another strategy to give you more chance to have valuable information.\n\n```bash\n$ wordle --stats\nHere is the list of 10 possibilities: [\'naked\', \'named\', \'navel\', \'needy\', \'negev\', \'nepal\', \'nervy\', \'never\', \'newer\', \'newly\']\n10 most used letters in the words: e, n, a, v, d, l, r, y, w, g\n5 most scored words: never, needy, negev, newer, navel\nPlease enter the word played:\n\nNo play recorded.\n```\n\n### Using the Words API\n\nIn order to check the validity and frequency of the words with a call to the [Words API](https://github.com/dwyl/english-words), you need to store a valid [Rapid API](https://rapidapi.com) key in `RAPIDAPI_KEY` environment variable. It is free for up to 2500 words per day. Once a word is checked, it is stored locally so it will not be checked again the next days.\n\n```bash\nexport RAPIDAPI_KEY="{YourKey}"\nwordle --check\n```\n\nChecking the words allows you to filter the proposed words by their frequency. The solution of the Wordle game tends to be a word with a high frequency.\n\n```bash\nwordle --check --minfrequency=5\n```\n\n### Large English word list\n\nBy default the tool will rely on a list that contains less than 4300 words of 5 letters. The good news is that most are valid but a few are missing. With the `--large` option, you will use a list with nearly 16000 words of 5 letters. It\'s exhaustive but unfortunately it also contains many invalid words. This is where the Words API will become handy. But beware of your daily quota.\n\n```bash\nwordle --large\n```\n',
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
