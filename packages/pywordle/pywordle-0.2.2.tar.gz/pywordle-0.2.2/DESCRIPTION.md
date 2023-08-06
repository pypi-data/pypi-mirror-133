# Wordle

This package can help you playing playing the [Wordle](https://www.powerlanguage.co.uk/wordle/) game.

## Installation

The tool can easyly be insalled on a computer where a recent (>=3.10) version of Python is present.

```bash
python3 -m venv venv
. venv/bin/activate
pip install pywordle
```

## Usage

All the command line options can be found with the `--help` option.

```bash
$ wordle --help
usage: Propose words for the Wordle game. [-h] [--large] [--stats] [--none] [--unique] [--check] [--verbose] [--letters LETTERS] [--minfrequency MINFREQUENCY]

options:
  -h, --help            show this help message and exit
  --large               Uses the large file of english words.
  --stats               Displays some stats about the found words.
  --none                Use none of the previously used letters.
  --unique              Do not repeat letters in a word.
  --check               Check that the word is valid.
  --verbose             Print progress.
  --letters LETTERS     The set of letters to be used.
  --minfrequency MINFREQUENCY
                        A minimum frequency for the proposed words, between 1 and 7.

```

### Letters

The `--letters` is useful to start the game with a word that is using the most common english letters to have the best chances to find letters of the solution word. It also could be a good idea to add the `--unique` option to avoid repeating a letter. Adding the `--check` will allow to check how often the words are used. This can be filtered with a `--minfrequency`. And if you do not add too many letters, you can finally add `--all` to see the full list of matching words.

```bash
wordle --letters=etaionshr --unique --check --minfrequency=3 --all
```

### Using the Words API

In order to check the validity and frequency of the words with a call to the [Words API](https://github.com/dwyl/english-words), you need to store a valid [Rapid API](https://rapidapi.com) key in `RAPIDAPI_KEY` environment variable. It is free for up to 2500 words per day. Once a word is checked, it is stored locally so it will not be checked again the next days.

```bash
export RAPIDAPI_KEY="{YourKey}"
wordle --check
```

Checking the words allows you to filter the proposed words by their frequency. The solution of the Wordle game tend to be a word with a high frequency.

```bash
wordle --check --minfrequency 5
```
