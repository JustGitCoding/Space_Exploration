# Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Create a new flask app 'instance'
app = Flask(__name__)

# Use flask_pymongo to set up Mongo connection to our 'space_app' database (in Mongo 'use space_app')
app.config['MONGO_URI'] = 'mongodb://localhost:27017/space_app'
mongo = PyMongo(app)

# Set up app routes
# HOME PAGE
@app.route('/')
def index():
    mars = mongo.db.mars.find_one() ### searching for 'mars' collection within space_app database
    return render_template('index.html', mars=mars)

# SCRAPING route - Button that will appear on home page, and scrape updated data when clicked
@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {'$set':mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run()