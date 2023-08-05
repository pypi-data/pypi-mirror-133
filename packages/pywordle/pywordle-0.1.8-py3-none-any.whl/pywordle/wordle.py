#!/usr/bin/env python
"""
Play Wordle game
https://www.powerlanguage.co.uk/wordle/

Usage:
poetry install
poetry run wordle --help
"""

from argparse import ArgumentParser, Namespace

from datetime import datetime
from importlib.resources import open_text
from json import dump, load, loads
from os import getenv, makedirs
from os.path import join
import sys
from typing import Any, List, Generator, Callable, Union

from marshmallow import Schema, fields, post_load
from pytz import timezone
from requests import get

WORDS_DIR = "words"
WORDS_FOUND_FILE = "words.en.json"
WORDS_NOT_FOUND_FILE = "words.en.notfound.txt"
GAME_FILE = f"games/{datetime.now(timezone('CET')).strftime('%Y%m%d')}.json"
ARGS = Namespace()


# pylint: disable=no-member, no-self-use


def parse_arguments() -> None:
    """
    Parse the command line arguments.
    """
    parser = ArgumentParser("Propose words for the Wordle game.")
    parser.add_argument("--all", action="store_true", help="Displays the full list of available words.")
    parser.add_argument("--none", action="store_true", help="Use none of the previously used letters.")
    parser.add_argument("--unique", action="store_true", help="Do not repeat letters in a word.")
    parser.add_argument("--check", action="store_true", help="Check that the word is valid.")
    parser.add_argument("--verbose", action="store_true", help="Print progress.")
    parser.add_argument("--letters", help="The set of letters to be used.")
    parser.add_argument(
        "--minfrequency", type=float, default=0, help="A minimum frequency for the proposed words, between 1 and 7."
    )
    parser.parse_args(namespace=ARGS)
    if ARGS.check and getenv("RAPIDAPI_KEY") is None:
        print(
            "You need to provide a valid Rapid API key in RAPIDAPI_KEY environment variable",
            "to be able to check the existence and the usage frequency of the words.",
        )
        sys.exit(1)


class Play:
    """
    This represent a played word with its result.
    For each letter is the corresponding code:
    0: letter not in word
    1: letter in word in a different position
    2: letter in word in that position
    """

    word: str
    result: List[int]

    def __init__(self, word: str, result: List[int]):
        self.word = word
        self.result = result

    def is_valid(self, word: str) -> bool:  # NOSONAR
        """
        Check if the new word would give this result for the current word.
        """
        if len(self.word) != len(word):
            return False
        letters = list(self.word)
        newletters = list(word)
        # First handle the exact match
        for index, letter in enumerate(letters):
            if self.result[index] == 2:
                if newletters[index] != letter:  # Exact match is missing
                    return False
                letters[index] = "_"
                newletters[index] = "_"
        # Now handle the non exact match
        for index, letter in enumerate(letters):
            if self.result[index] == 1:
                if newletters[index] == letter:  # This is an exact match where it should not
                    return False
                if letter not in newletters:  # We should find this letter in the solution
                    return False
                letters[index] = "_"
                newindex = newletters.index(letter)
                newletters[newindex] = "_"
        # Finally handle the miss
        for index, letter in enumerate(letters):
            if self.result[index] == 0 and letter in newletters:  # There should be no match
                return False
        # It's all good, we have a match
        return True

    def is_none(self, word: str) -> bool:
        """
        Check if the proposed word has none of the letters of the played word.
        """
        for letter in word:
            # Letter is never used before
            if letter in self.word:
                return False
        return True


class Game:
    """
    This is a full game session with the list of words played already.
    """

    played: List[Play]

    def __init__(self, played: List[Play]):
        self.played = played

    def is_valid(self, word: str) -> bool:
        """
        Check each word played to see if the provided one is a match.
        """
        for play in self.played:
            if not play.is_valid(word):
                return False
        return True

    def is_none(self, word: str) -> bool:
        """
        Check each word played to see if the provided one uses any of the letters.
        """
        for play in self.played:
            if not play.is_none(word):
                return False
        return True


class PlaySchema(Schema):
    """
    Marshmallow schema of the Play object.
    """

    word = fields.Str()
    result = fields.List(fields.Integer)

    @post_load
    def make_play(self, data: Any, **_: Any) -> Play:
        """
        This mill create a Play object when invoking a load() on the schema.
        """
        return Play(**data)


class GameSchema(Schema):
    """
    Marshmallow schema of the Game object.
    """

    played = fields.List(fields.Nested(PlaySchema))

    @post_load
    def make_game(self, data: Any, **_: Any) -> Game:
        """
        This will create a Game object when invoking a load() on the schema.
        """
        return Game(**data)


def get_words() -> Generator[str, None, None]:
    """
    Read the words from the words.en.txt file.
    It is now a ressource provided by the package.
    """
    with open_text("pywordle.words", "words.en.txt") as wfile:
        for line in wfile:
            yield line.split("\n")[0]


def get_game(gamefilename: str) -> Union[Game, Any]:
    """
    Get the current game progress from a JSON file.
    """
    try:
        with open(gamefilename, mode="r", encoding="utf_8") as gfile:
            return GameSchema().loads(gfile.read())
    except FileNotFoundError:
        # If the game file was not found, we create it
        # First we make sure that the games directory exists
        makedirs("games", exist_ok=True)
        emptygame: dict[str, List[Any]] = {"played": []}
        with open(gamefilename, mode="w", encoding="utf_8") as gfile:
            dump(emptygame, gfile, indent=4)
        return GameSchema().load(emptygame)


def appendtofile(word: str, filename: str) -> None:
    """
    Append the word to the list of files.
    One word per line.
    """
    with open(filename, mode="a", encoding="utf_8") as thefile:
        thefile.write(f"{word}\n")


def savefrequency(word: str, frequency: int) -> None:
    """
    For the moment we simply save the frequency in case we want to use
    it to improve the algorithm.
    """
    print(f"Save frequency for '{word}': {frequency}")
    words = {}
    with open(join(WORDS_DIR, WORDS_FOUND_FILE), mode="r", encoding="utf_8") as thejson:
        words = load(thejson)
    words[word] = frequency
    with open(join(WORDS_DIR, WORDS_FOUND_FILE), mode="w", encoding="utf_8") as thejson:
        dump(words, thejson, indent=4)


def wordsapi(word: str, minfrequency: int) -> bool:
    """
    Check if a word is found in the Words API.
    """
    verbose(f"Check the Words API for '{word}'")
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}"

    headers = {
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
        "x-rapidapi-key": getenv("RAPIDAPI_KEY"),
    }

    response = get(url, headers=headers)

    if response.status_code == 200:
        frequency = loads(response.text).get("frequency")
        savefrequency(word, frequency)
        return frequency is not None and frequency >= minfrequency

    appendtofile(word, join(WORDS_DIR, WORDS_NOT_FOUND_FILE))
    return False


def filterwords(words: Generator[str, None, None], predicate: Callable[[str], bool]) -> Generator[str, None, None]:
    """
    Filter a generator of words according to the given predicate.
    """
    for word in words:
        if predicate(word):
            yield word


def filterapi(words: Generator[str, None, None], minfrequency: int = 0) -> Generator[str, None, None]:
    """
    Check the Words API, but first see if we didn't do it already.
    """
    # Get the list of words not found in the Words API
    try:
        with open(join(WORDS_DIR, WORDS_NOT_FOUND_FILE), mode="r", encoding="utf_8") as notfoundfile:
            notfoundwords = notfoundfile.read().splitlines()
    except FileNotFoundError:
        notfoundwords = []

    # Get the list of words foun din the API with their frequency
    try:
        with open(join(WORDS_DIR, WORDS_FOUND_FILE), mode="r", encoding="utf_8") as foundfile:
            foundwords = loads(foundfile.read())
    except FileNotFoundError:
        # Make sure the words directory exists
        makedirs(WORDS_DIR, exist_ok=True)
        foundwords = {}
        with open(join(WORDS_DIR, WORDS_FOUND_FILE), mode="w", encoding="utf_8") as foundfile:
            dump(foundwords, foundfile, indent=4)

    # Check each words
    for word in words:

        # Already not found in the API?
        if word in notfoundwords:
            verbose(f"Word already not found in the API: {word}")
            continue

        # If we have it in the file, no need to go to the API
        if word in foundwords:
            frequency = foundwords[word]
            if frequency and frequency >= minfrequency:
                print(f"Frequency of {word} is {frequency}")
                yield word
            else:
                verbose(f"Frequency of {word} is too low: {frequency}")
            continue

        # Now we need to ask the API.
        # It will save the result in the files for later.
        if wordsapi(word, minfrequency):
            yield word
        else:
            verbose(f"Word excluded by the API: {word}")


def verbose(text: str) -> None:
    """
    Print a message on the console in verbose mode.
    """
    if ARGS.verbose:
        print(text)


def composedofletters(word: str, letters: str) -> bool:
    """
    Check if a word only contains the provided letters.
    """
    for letter in word:
        if letter not in letters:
            return False
    return True


def saveplay(gamefilename: str, game: Game) -> None:
    """
    Records the word that was just played and the result given by Wordle.
    """
    print("Please enter the word played: ")
    word = input()
    if not word:
        print("No play recorded.")
        return
    word = word.lower()
    if len(word) != 5 or not word.isalpha():
        print(f"Invalid word '{word}'. It should be purely alphabetic and 5 characters long.")
        return
    print("Please enter the result:")
    resultstr = input()
    if not resultstr:
        print("No play recorded.")
        return
    try:
        result = [max(min(int(i), 2), 0) for i in resultstr]
    except ValueError:
        print(f"Invalid result '{resultstr}'. It should be a string of 0, 1 and 2 (Ex: 00120).")
        return
    if len(result) != 5:
        print(f"Invalid result '{resultstr}'. There should be 5 values.")
        return

    print(f"Saving result for '{word}': {result}")
    game.played.append(Play(word=word, result=result))
    with open(gamefilename, mode="w", encoding="utf_8") as gamefile:
        dump(GameSchema().dump(game), gamefile, indent=4)

    if result == [2, 2, 2, 2, 2]:
        print("You WON!!!!")


def main() -> None:
    """
    Module's entry point.
    """
    parse_arguments()

    words = get_words()

    verbose("Only keep the 5 letters words")
    words = filterwords(words, lambda word: len(word) == 5)

    if ARGS.letters:
        verbose(f"Only use the letters '{ARGS.letters}'")
        words = filterwords(words, lambda word: composedofletters(word, ARGS.letters))

    if ARGS.unique:
        verbose("Only propose words with no letter repetition")
        words = filterwords(words, lambda word: len(word) == len(set(word)))

    # read the current game status
    game = get_game(GAME_FILE)

    # Are we looking for a valid word or one that uses none of the letters used before?
    if ARGS.none:
        verbose("Keep the words with only new letters")
        words = filterwords(words, game.is_none)
    else:
        verbose("Keep the valid words only")
        words = filterwords(words, game.is_valid)

    # Check if words exist with Words API
    if ARGS.check:
        verbose("Check the existence and frequency with the API")
        words = filterapi(words, ARGS.minfrequency)

    if ARGS.all:
        wordslist = list(words)
        print(f"Here is the complete list of {len(wordslist)} possibilities: {wordslist}")
    else:
        # At this point we may have no available words left
        try:
            word = next(words)
            print(f"Try this word: '{word}'")
        except StopIteration:
            print("No more matching words.")

    # Save the game play if any
    saveplay(GAME_FILE, game)


if __name__ == "__main__":
    main()
