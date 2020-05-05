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

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather_1 = soup.find("main")
    desc_1 = mars_weather_1.find("section")
    desc_2 = desc_1.find_all("span")[4].get_text()

    print('--------------------------------')
    print(desc_2)
    print('--------------------------------')

    load_to_db({
        'description': f'''{desc_2}'''
    })
    
def load_to_db(items):
    # Drops collection if available to remove duplicates
    db.mars.weather.drop()

    # load data to collection
    collection = db.mars.weather
    collection.insert_one(items)


# def main():
#     init_browser()
#     scrape()


# if __name__ == "__main__":
#     main()