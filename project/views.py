from flask import render_template, request, redirect, url_for, session
from project import app
from project import models


@app.route("/")
@app.route("/index.html")
def index():
    properties_list = models.getAllProperties()
    return render_template("index.html", properties=properties_list)


@app.route("/listings.html")
def listings():
    owner_id = session.get("owner_id") #using session as thougt in class
    if not owner_id:
        return redirect(url_for("index")) #if a user is not logged in you return to index indead of errormessage/crash
    properties_list = models.getPropertyByOwner(owner_id)
    return render_template("listings.html", properties=properties_list)


@app.route("/property/<int:property_id>")
@app.route("/property_details.html/<int:property_id>")
def property_details(property_id):
    property_data = models.getPropertyById(property_id)
    images = models.getAllImagesProperty(property_id)

    if property_data is None:
        return "Property not found"

    return render_template(
        "property_details.html",
        property=property_data,
        images=images
    )


@app.route("/owner/login", methods=["POST"])
def owner_login():
    username = request.form.get("username")
    password = request.form.get("password")

    owner = models.ownerLoginVal(username, password)

    if owner is None:
        return "Invalid username or password"

    session["owner_id"] = owner["owner_id"]
    session["owner_username"] = owner["username"]

    return redirect(url_for("index"))


@app.route("/tourist/login", methods=["POST"])
def tourist_login():
    username = request.form.get("username")
    password = request.form.get("password")

    tourist = models.touristLoginVal(username, password)

    if tourist is None:
        return "Invalid username or password"

    session["tourist_id"] = tourist["tourist_id"] #starts session
    session["tourist_username"] = tourist["username"] #dont know if we need this, not in use yet at least, move later if not in use

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/property/<int:property_id>/enquiry", methods=["POST"])
def send_enquiry(property_id):
    tourist_id = session.get("tourist_id")
    if not tourist_id:
        return redirect(url_for("index"))

    text = request.form.get("text")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    models.create_enquiry(
        tourist_id=tourist_id,
        property_id=property_id,
        text=text,
        start_date=start_date,
        end_date=end_date
    )

    return redirect(url_for("property_details", property_id=property_id))


@app.route("/owner/enquiries")
def owner_enquiries():
    owner_id = session.get("owner_id")
    if not owner_id:
        return redirect(url_for("index"))

    enquiries = models.getEnquiriesForOwner(owner_id)

    return render_template("owner_enquiries.html", enquiries=enquiries)


@app.route("/property/<int:property_id>/bookmark", methods=["POST"])
def addBookmark(property_id):
    tourist_id = session.get("tourist_id") #To get the correct bookmark list for this sessions tourist, same logic as listings (owner)
    if not tourist_id:
        return redirect(url_for("index"))

    models.addBookmark(tourist_id, property_id)

    return redirect(url_for("property_details", property_id=property_id))


@app.route("/bookmarks.html")
def getBookmarks():
    tourist_id = session.get("tourist_id") #Is it possible to do this in a separet method for the whole
    if not tourist_id:
        return redirect(url_for("index"))

    bookmarks = models.getBookmarks(tourist_id)
    return render_template("bookmarks.html", bookmarks=bookmarks)

#Must add logic for this: (This is to be able to update the database when a property is updated in listings.html)
#@app.route("/property/<int:property_id>/edit", methods=["POST"])
#def edit_property(property_id):