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

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    featured = {}

    img_base_url = 'https://www.jpl.nasa.gov/'
    feature_image_1 = soup.find('article', class_='carousel_item')
    feature_image_2 = feature_image_1.a['data-fancybox-href']
    featured.update({'featured_image': f'''{img_base_url}{feature_image_2}'''})

    print('--------------------------------')
    print(featured)
    print('--------------------------------')

    load_to_db(featured)
    
def load_to_db(items):
    # Drops collection if available to remove duplicates
    db.mars.featured_image.drop()

    # load data to collection
    collection = db.mars.featured_image
    collection.insert_one(items)


def main():
    init_browser()
    scrape()


if __name__ == "__main__":
    main()