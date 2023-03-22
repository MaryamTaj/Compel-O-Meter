"""CSC111 Winter 2023 Assignment 4: Compel-O-Meter

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Akshaya D., Kashish M., Maryam T. and Pratibha T..
"""

# from python_ta.contracts import check_contracts
import csv
import snscrape.modules.twitter as sntwitter

# Define the query to search for
query = 'python'

# Define the url to search
url = 'https://twitter.com/search?q={}&lang=en'.format(query)

# Create a csv file to write the results to
with open('tweets.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Iterate over the tweets matching the query
    for tweet in sntwitter.TwitterSearchScraper(url).get_items():
        writer.writerow([tweet.date, tweet.content, tweet.followersCount])

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
