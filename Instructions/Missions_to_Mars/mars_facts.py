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

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    # time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    facts = {}
    fact_key = ""
    fact_value = ""
    
    facts_1 = soup.find('section', class_='sidebar widget-area clearfix')
    for tr in facts_1.tbody:
    
        fact_key = tr.find("td", class_="column-1").strong.text
        print(fact_key)

        fact_value = tr.find("td", class_="column-2").text
        print(fact_value)

        facts.update({fact_key: fact_value})

    print('--------------------------------')
    print(facts)
    print('--------------------------------')

    load_to_db(facts)

    
def load_to_db(items):
    # Drops collection if available to remove duplicates
    db.mars.facts.drop()

    # load data to collection
    collection = db.mars.facts
    collection.insert_one(items)


# def main():
#     init_browser()
#     scrape()


# if __name__ == "__main__":
#     main()