"""CSC111 Winter 2023 Assignment 4: Compel-O-Meter

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Akshaya D., Kashish M., Maryam T. and Pratibha T..
"""

<<<<<<< HEAD
from python_ta.contracts import check_contracts
import csv


def read_csv_file(csv_file1: str, csv_file2: str) -> dict[str, int]:
    """..."""

    with open(csv_file1) as file:
        reader = csv.reader(file)

        i = 0
        while i < 35:
            next(reader)
            i += 1

        words = {}
        for row in reader:
            words[row[0]] = 1

    with open(csv_file2) as file:
        reader = csv.reader(file)

        i = 0
        while i < 35:
            next(reader)
            i += 1

        for row in reader:
            words[row[0]] = -1

    return words

=======
# from python_ta.contracts import check_contracts
import snscrape.modules.twitter as sntwitter
import pandas as pd

username = 'realDonaldTrump'

url = f'https://twitter.com/{username}/from{username}'

tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(url).get_items()):
    if i >= 100:
        break
    tweets.append((tweet.date, tweet.content))

df = pd.DataFrame(tweets, columns=['date', 'content'])

df.to_csv('trump_tweets.csv', index=False)

<<<<<<< HEAD
=======
    # Iterate over the tweets matching the query
    for tweet in sntwitter.TwitterSearchScraper(url).get_items():
        writer.writerow([tweet.date, tweet.content, tweet.followersCount])
>>>>>>> 97e7213f990c5b6fef017984aca9da9f10725503
>>>>>>> 8c9a4e58da72c00c6d6fa1e95c82401d09a88326

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['random', 'a3_network', 'a3_part1'],
    #     'disable': ['unused-import']
    # })
