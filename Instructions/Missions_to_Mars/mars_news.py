import time
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news = soup.find('ul', class_='item_list')
    article_listing_2 = news.find('li', class_='slide')
    title = article_listing_2.h3.text
    paragraph = article_listing_2.find('div', class_='article_teaser_body').get_text()

    print('--------------------------------')
    print(title)
    print(paragraph)
    print('--------------------------------')

    load_to_db({
        'title': f'''{title}''',
        'paragraph': f'''{paragraph}'''
    })
    
def load_to_db(items):
    # Drops collection if available to remove duplicates
    db.mars.news.drop()

    # load data to collection
    collection = db.mars.news
    collection.insert_one(items)


# def main():
#     init_browser()
#     scrape()


# if __name__ == "__main__":
#     main()