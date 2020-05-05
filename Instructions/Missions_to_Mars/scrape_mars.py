from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    scrape1()
    scrape2()
    scrape3()

def scrape1():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news = soup.find('ul', class_='item_list')
    article_listing = news.find('li', class_='slide')
    title = article_listing.h3.text
    paragraph = article_listing.find('div', class_='article_teaser_body').get_text()

    print('--------------------------------')
    print(title)
    print(paragraph)
    print('--------------------------------')

    return {"title": title, "article": paragraph}

def scrape2():
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

    return {"weather": desc_2}

def scrape3():
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

    return item_dict