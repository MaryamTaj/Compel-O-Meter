"""..."""

import csv
from typing import Optional


def read_csv_positive_file(csv_file1: Optional[str] = None) -> dict[str, int]:
    """..."""
    csv_file1 = 'data/positive_words.csv'
    with open(csv_file1) as file:
        reader = csv.reader(file)

        i = 0
        while i < 35:
            next(reader)
            i += 1

        words = {}
        for row in reader:
            words[row[0]] = 1

    return words


def read_csv_negative_file(csv_file1: str) -> dict[str, int]:
    """..."""

    with open(csv_file1) as file:
        reader = csv.reader(file)

        i = 0
        while i < 35:
            next(reader)
            i += 1

        words = {}
        for row in reader:
            words[row[0]] = -1

    return words


def return_dictionary(csv_file1: str, csv_file2: str) -> dict[str, int]:
    """..."""
    positive = read_csv_positive_file(csv_file1)
    negative = read_csv_negative_file(csv_file2)

    words = positive
    for word in negative:
        words[word] = -1

    return words
