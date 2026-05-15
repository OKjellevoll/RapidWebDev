from flask import render_template
from project import app
from project import models

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html") #Use this method to fetch all properties in index.html
def properties():
    properties_list = models.getAllProperties()
    return render_template("index.html", properties=properties_list)

@app.route("/index.html")
def getPropertyById():
    property = models.getPropertyById()
    return render_template("index.html", property=property)