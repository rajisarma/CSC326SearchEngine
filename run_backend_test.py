from crawler import *
import sqlite3

'''The following function setups a SQL database connection to test_crawler.db and uses a crawler object to insert entries related to the document id and its corresponding page rank score in the database. The function ends by making a call to crawler method pretty_print_page_rank_scores to print the page rank score in a readable "pretty" format
'''

def print_pretty_page_rank_score():

	db = sqlite3.connect("test_crawler.db")
	bot = crawler(db, "urls.txt")
    	bot.crawl(depth=1)
	db = sqlite3.connect("test_crawler.db")
	bot.pretty_print_page_rank_scores(db)


if __name__ == "__main__":
	print_pretty_page_rank_score()
