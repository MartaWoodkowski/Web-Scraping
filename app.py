from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data=data)

@app.route("/scrape")
def scrape():
    listings = scrape_mars.scrape()
    mongo.db.collection.update({}, listings, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)