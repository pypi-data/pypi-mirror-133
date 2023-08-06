# Wordle

This package can help you playing the [Wordle](https://www.powerlanguage.co.uk/wordle/) game. It will not play for you. You will still have to choose the best strategy.

## Installation

The tool can easily be installed on a computer where a recent (>=3.10) version of Python is present.

```bash
python3 -m venv venv
. venv/bin/activate
pip install pywordle
```

## Usage

Each time that you want to enter a new word, you will ask the tool to provide a list of candidates. When you have selected a word, type it in as well as the result provided by the `Wordle` game. The code values for the result colours are:

* Dark gray: 0
* Yellow: 1
* Green: 2

Here is an example:

```bash
$ wordle --letters=etaions --unique
Here is the list of 14 possibilities: ['aeons', 'anise', 'atone', 'eosin', 'inset', 'iotas', 'noise', 'notes', 'onset', 'saint', 'satin', 'stain', 'stone', 'tones']
Please enter the word played:
noise
Please enter the result:
20001
Saving result for 'noise': [2, 0, 0, 0, 1]
```

The result will be stored in today's game file and be used next time you call the tool, limiting the possibilities. Just type `Enter`, if you do not want to choose a word just yet.

All the command line options can be found with the `--help` option.

```bash
$ wordle --help
usage: Propose words for the Wordle game. [-h] [--large] [--stats] [--none] [--unique] [--check] [--verbose] [--letters LETTERS] [--minfrequency MINFREQUENCY]

options:
  -h, --help            show this help message and exit
  --large               Uses the large file of English words.
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

The `--letters` is useful to start the game with a word that is using the most common English letters to have the best chances to find letters of the solution word. It also could be a good idea to add the `--unique` option to avoid repeating a letter.

```bash
wordle --letters=etaionshr --unique
```

### None

This is a different strategy. Instead of looking for a possible word, you are trying to look for information on letters that you have not used yet today. This is not possible if you have selected the `Hard Mode`. It only makes sense to use the option for the second and possibly third word. Again the `--unique` option will give you more information.

```bash
wordle --none --unique
```

### Stats

This will give you some statistics in the list of proposed words. First you will get the most used letters in that list. Then you will get the words that used the most used letters. This is another strategy to give you more chance to have valuable information.

```bash
$ wordle --stats
Here is the list of 10 possibilities: ['naked', 'named', 'navel', 'needy', 'negev', 'nepal', 'nervy', 'never', 'newer', 'newly']
10 most used letters in the words: e, n, a, v, d, l, r, y, w, g
5 most scored words: never, needy, negev, newer, navel
Please enter the word played:

No play recorded.
```

### Using the Words API

In order to check the validity and frequency of the words with a call to the [Words API](https://github.com/dwyl/english-words), you need to store a valid [Rapid API](https://rapidapi.com) key in `RAPIDAPI_KEY` environment variable. It is free for up to 2500 words per day. Once a word is checked, it is stored locally so it will not be checked again the next days.

```bash
export RAPIDAPI_KEY="{YourKey}"
wordle --check
```

Checking the words allows you to filter the proposed words by their frequency. The solution of the Wordle game tends to be a word with a high frequency.

```bash
wordle --check --minfrequency=5
```

### Large English word list

By default the tool will rely on a list that contains less than 4300 words of 5 letters. The good news is that most are valid but a few are missing. With the `--large` option, you will use a list with nearly 16000 words of 5 letters. It's exhaustive but unfortunately it also contains many invalid words. This is where the Words API will become handy. But beware of your daily quota.

```bash
wordle --large
```
