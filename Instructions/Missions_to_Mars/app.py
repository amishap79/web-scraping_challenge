from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import mars_astrogeology
import mars_facts
import mars_featured_image
import mars_news
import mars_weather

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    # Uncomment to reload the database with latest data
    # load_data()

    astrogeology = mongo.db.mars.astrogeology.find_one()
    facts = mongo.db.mars.facts.find_one()
    featured_image = mongo.db.mars.featured_image.find_one()
    news = mongo.db.mars.news.find_one()
    weather = mongo.db.mars.weather.find_one()

    print(facts)

    return render_template("index.html", \
        astrogeology=astrogeology, \
        facts=facts, \
        featured_image=featured_image, \
        news=news, \
        weather=weather)


# @app.route("/scrape")
# def scraper():
#     listings = mongo.db.listings
#     listings_data = scrape_mars.scrape()
#     listings.update({}, listings_data, upsert=True)
#     return redirect("/", code=302)


def load_data():

    mars_astrogeology.scrape()
    mars_facts.scrape()
    mars_featured_image.scrape()
    mars_news.scrape()
    mars_weather.scrape()


if __name__ == "__main__":
    app.run(debug=True)
