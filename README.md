# crawler
Crawl the website https://www.msf.gov.sg/Pages/default.aspx and all its' children websites using Scrapy in python, collect all text data and preprocess it, ie, remove unicode, punctuation, URL, numbers, etc.

# Requirements
You must have python3 installed along with the following libraries:-
1. pandas
2. clean-text: (NOTE: Download using 'pip install clean-text', and NOT cleantext)
3. scrapy: (Download using: 'pip install scrapy')
4. os

# Instructions to run the program
1. Extract the parent folder 'crawler' into any directory within your computer.
2. Double click on the 'main.py' file to begin the crawling.
3. Run using command prompt: Alternatively, open command prompt on your system in the crawler working directory, and type 'python main.py'.

# Results
The results of crawling can be seen in the following files after running:-
Within the main crawler folder:-
1. rawdata.csv: Noisy text data, scraped from the websites.
2. paragraphs.csv: Cleaned text data after preprocessing.
3. titles.csv: All the titles. Cleaned text data after preprocessing.

# Code
1. crawler/spiders/spider.py: The main crawler
2. cleandata.py: Used for cleaning the scraped text data
3. main.py: The master file which runs both the crawler and cleaner.
