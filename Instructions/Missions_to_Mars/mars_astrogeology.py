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

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img_url_base = "https://astrogeology.usgs.gov"
    item_dict = []
    items = soup.find_all("div", class_="description")

    for item in items:
        title = item.a.h3.text
        img_url = item.a["href"]
        img_url = f"{img_url_base}{img_url}"
        item_dict.append({"title": title, "img_url": img_url})

    print('--------------------------------')
    print(*item_dict, sep="\n")
    print('--------------------------------')

    load_to_db(item_dict)
    
def load_to_db(items):
    # Drops collection if available to remove duplicates
    db.mars.astrogeology.drop()

    # load data to collection
    collection = db.mars.astrogeology
    collection.insert_many(items)


# def main():
#     init_browser()
#     scrape()


# if __name__ == "__main__":
#     main()