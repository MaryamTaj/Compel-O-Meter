"""
This file contains the all the functions needed to process a written textual post into something
 that we can create parse trees with and run sentiment analysis on :)
"""

from __future__ import annotations
from typing import Any
import nltk
import spacy
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import csv


# from python_ta.contracts import check_contracts


def text_to_sentences(text: str) -> list[str]:
    """ Breaks a text up into a list of the sentences it's composed of.
    """
    sentences = text.split(".")
    if sentences[-1] == '':
        sentences.remove('')
    return sentences


def is_independent_clause(sentence: str) -> bool:
    """Returns True when a sentence is an independent clause and False when it is not.

    Preconditions:
    - the inputted sentence should not have leading whitespace!

    >>> is_independent_clause("I like cheese")
    True
    >>> not is_independent_clause("Just because")
    True
    >>> is_independent_clause("I brought a knife to a gun fight")
    True
    >>> is_independent_clause("It's okay")
    True
    """
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    root = [token for token in doc if token.head == token][0]
    return root.pos_ == 'VERB' or root.pos_ == 'AUX'


def find_conjunctions(sentence) -> list[str]:
    """
    Returns a list containing the conjunctions in a sentence.
    >>> my_sentence = "I like, the moon; but I: like the — stars more and I like the sun most"
    >>> find_conjunctions(my_sentence)
    ['but', 'and', ',', '—', ':', ';']

    Implementation Notes:
    - Note that commas may split independent sentences as comma splicing is common on social media platforms. Thus,
    treat commas as conjunctions

    """
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    conjunctions = [token.text for token in doc if 'CONJ' in token.pos_]
    if ',' in sentence:
        conjunctions.append(',')
    if '—' in sentence:
        conjunctions.append('—')
    if ':' in sentence:
        conjunctions.append(':')
    if ';' in sentence:
        conjunctions.append(';')
    return conjunctions


def split_ind_clauses(sentence: str) -> list[str]:
    """ Takes in a sentence and returns a new sentence in which all independent clauses appear
    as separate sentences.

    Implementation Notes:
    - Note that commas may split independent sentences as comma splicing is common on social media platforms.

    >>> my_sentence = "I like pizza and pasta but I don't like you"
    >>> split_ind_clauses(my_sentence)
    ['I like pizza and pasta ', "I don't like you"]

    NOTE: This function gets rid of conjunctions that split independent clauses. For our purposes, this is preferrable.
    """
    conjunctions = find_conjunctions(sentence)
    potentially_independent = []
    for conjunction in conjunctions:
        potentially_independent.extend(sentence.split(conjunction))
    # Remove any leading whitespace from sentence
    potentially_independent = [sentence.lstrip() for sentence in potentially_independent]
    independent = [potential for potential in potentially_independent if is_independent_clause(potential)]

    duplicates = []

    for i in range(len(independent)):
        for j in range(len(independent)):
            if i != j and independent[i] in independent[j]:
                duplicates.append(i)

    independent = [independent[i] for i in range(len(independent)) if i not in duplicates]

    return independent


def split_ind_clauses_list(sentences: list[str]) -> list[str]:
    """ Takes in a sentence and returns a new sentence in which all independent clauses appear
    as separate sentences.

    Implementation Notes:
    - Note that commas may split independent sentences as comma splicing is common on social media platforms.
    """
    independent_sentences = []
    for sentence in sentences:
        independent_sentences.extend(split_ind_clauses(sentence))

    return independent_sentences


def upper_to_lower(sentences: list[str]) -> list[str]:
    """Turns all upper case characters to lower case
    """
    return [str.lower(word) for word in sentences]


def lemmatize(word: str) -> str:
    """ Convert a word to its base or dictionary form, also known as a lemma. This makes it possible to compare the word
    with the words in the lexicon.
    >>> lemmatize('bats')
    'bat'
    >>> lemmatize('running')
    'run'
    >>> lemmatize('was')
    'be'
    """
    # download 'averaged_perceptron_tagger' if not already present in system.
    nltk.download('averaged_perceptron_tagger')
    # Initialize the WordNetLemmatizer function.
    lemmatizer = WordNetLemmatizer()

    # Find the parts of speech tag for the word.
    spacy.load('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

    doc = nlp(word)
    pos_tag = ''
    for token in doc:
        pos_tag = token.pos_

    # Since the lemmatizer takes in a word and the first letter of the part of speech (POS) tag as input, find the
    # first letter of the pos tag. Then, call the lemmatizer.
    if pos_tag.startswith('J'):
        pos_tag = wordnet.ADJ
        return lemmatizer.lemmatize(word, pos_tag)

    elif pos_tag.startswith('V') or pos_tag == 'AUX':
        pos_tag = wordnet.VERB
        return lemmatizer.lemmatize(word, pos_tag)

    elif pos_tag.startswith('N'):
        pos_tag = wordnet.NOUN
        return lemmatizer.lemmatize(word, pos_tag)

    elif pos_tag.startswith('R'):
        pos_tag = wordnet.ADV
        return lemmatizer.lemmatize(word, pos_tag)

    else:
        pos_tag = None
        return word


def is_numeral(word: str) -> bool:
    """ Return True if the given word is a numeral and False otherwise.
    >>> is_numeral('7')
    True
    >>> is_numeral('777')
    True
    >>> is_numeral('seventy one')
    True
    >>> is_numeral('hi')
    False
    """
    word_new = [w for w in word if w.isdigit()]
    if not word_new:
        singles = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        tens_first = ['ten', 'twent', 'thirt', 'forti', 'forty', 'fifti', 'fifty']
        powers = ['hundred', 'thousand', 'million', 'trillion', 'billion']
        teens_first = ['twel', 'thirt', 'fourt', 'fift']
        numbers = singles + tens_first + teens_first + powers
        word = word.lower()
        word = word.split(' ')
        for w in word:
            for num in numbers:
                if num in w:
                    return True
        return False
    else:
        return True


def count_numerals(sentence: str) -> int:
    """Return the number of numerals in a sentence
    >>> count_numerals("I'm 19.")
    1
    >>> count_numerals("We have 13, 14, and 15 cars, trucks, and tractors, respectively.")
    3
    >>> count_numerals("79% of Vietnamese citizens and 21% of Indian citizens agreed with the bill.")
    2
    >>> count_numerals("'They tell you that you're lucky, but you're so confused', says Taylor Swift in a new song.")
    0
    """
    sentence = sentence.split(' ')
    return sum([is_numeral(num) for num in sentence])


def reasoning_words_list(csv_file: str) -> list:
    """
    ....
    """
    with open(csv_file) as file:
        reader = csv.reader(file)
        reasoning_words = []
        for row in reader:
            row = row[0].lower()
            reasoning_words.append(row)
    return reasoning_words


def is_reasoning_text(text: str) -> bool:
    """Return True if the inputted text contains one or more words
    or phrases frequently used for reasoning purposes and False if not.

    >>> is_reasoning_text("I don't want to go because I'm scared")
    True
    >>> is_reasoning_text("Due to the failure of Congress, inflation is at 16%, marking an all-time high.")
    True
    >>> is_reasoning_text("Inflation is at 16%, marking an all-time high.")
    False
    """
    reasoning_words = reasoning_words_list('data/reasoning_words.csv')
    text = text.lower()
    for word in reasoning_words:
        if word in text:
            return True
    return False


def count_logos_numerals(text: str) -> list[int]:
    """Return a list of counts of logos numerals in each sentece of a text.

    A logos numeral is one that is used for reasoning about something.

    IMPLEMENTATION NOTES:
    - Assume that a sentence's numerals are logos numerals if and only if the text it is a part of contains
    at least one word that is frequently used for reasoning.
    - use is_reasoning_text to complete this function

    >>> count_logos_numerals("Hi. We have 13, 14, and 15 cars, trucks, and tractors, respectively.")
    [0, 0]
    >>> count_logos_numerals("We should not buy more. We have 13, 14, and 15 cars, trucks, and tractors, respectively.")
    [0, 3]
    >>> count_logos_numerals("I went to the market today")
    [0]
    >>> count_logos_numerals("Covid cases are rising but the school doesn't care. This is unacceptable.")
    [0, 0]
    >>> count_logos_numerals("57 people died.")
    [0]
    >>> count_logos_numerals("57 people died because of you!")
    [1]
    """
    sentences = text_to_sentences(text)
    logos_num = []
    if is_reasoning_text(text):
        for sentence in sentences:
            num = count_numerals(sentence)
            logos_num.append(num)
    else:
        for sentence in sentences:
            logos_num.append(0)
    return logos_num


def process_text(text: str) -> list[str]:
    """Takes a given text and returns a list of independent clauses where all characters are in lower case
    >>> text = 'The castle crumbled overnight because I brought a knife to a gunfight. They took the crown but it is ok.'
    >>> process_text(text)
    ['the castle crumbled overnight ', 'i brought a knife to a gunfight', 'they took the crown ', 'it is ok']
    """
    sentences = text_to_sentences(text)
    sentences = split_ind_clauses_list(sentences)
    sentences = upper_to_lower(sentences)
    return sentences


if __name__ == '__main__':
    # Here is a sample call to part3_runner. Feel free to change it or add new calls!
    # part3_runner('data/always_right_ring_TEST.csv')
    # part3_runner_optional([GreedyPathRing(4), ShortestPathRing(4), AlwaysRightRing(4)], 'latencies')

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['forbidden-import'],
        'allowed-io': []
    })
