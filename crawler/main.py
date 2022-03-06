import os

# Run the Crawler
os.system('scrapy crawl msfSpider -o rawdata.csv')

# Clean the Data
os.system('python cleandata.py')
