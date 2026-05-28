from flask import render_template, request, redirect, url_for, session, flash
from project import app
from project import models
from project import auth

@app.route("/")
@app.route("/index.html")

def index():
    properties_list = models.getAllProperties()
    current_user = auth.get_current_user()
    main_images = []
    for property in properties_list:
        images = models.getAllImagesProperty(property["property_id"])
        image = images[0] if images else None
        main_images.append(image)       
    print("=== DEBUG LOGIN ===")
    print("Current User:", current_user)          
    print("Is Logged In:", auth.is_logged_in())
    return render_template("index.html", properties=properties_list, current_user=current_user, main_images=main_images)

@app.route("/listings.html")
@auth.seller_required
def listings():
    owner_id = session.get("owner_id") #using session as thougt in class
    if not owner_id:
        return redirect(url_for("index")) #if a user is not logged in you return to index indead of errormessage/crash
    properties_list = models.getPropertyByOwner(owner_id)
    main_images = []
    for listing in properties_list:
        images = models.getAllImagesProperty(listing["property_id"])
        image = images[0] if images else None
        main_images.append(image)
    return render_template("listings.html", properties=properties_list, main_images=main_images)


@app.route("/property/<int:property_id>")
@app.route("/property_details.html/<int:property_id>")
def property_details(property_id):
    property_data = models.getPropertyById(property_id)
    images = models.getAllImagesProperty(property_id)

    if property_data is None:
        return "Property not found"

    return render_template("property_details.html", property=property_data, images=images)

# ============================================================
# SECTION B: AUTHENTICATION ROUTES (Added by Vinod till 155)
# ============================================================

@app.route("/owner/login", methods=["POST"])
def owner_login():
    username = request.form.get("username")
    password = request.form.get("password")
    return auth.login_owner(username, password)


@app.route("/tourist/login", methods=["POST"])
def tourist_login():
    username = request.form.get("username")
    password = request.form.get("password")
    return auth.login_tourist(username, password)


@app.route("/logout")
def logout():
    return auth.logout_user()


# ------------------ Registration ------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        role = request.form.get("role")          # "seller" or "buyer"

        success = auth.register_user(username, password, email, role)

        if success:
            flash("Sucessfully logged in", "success")
            return redirect(url_for("index"))
        else:
            flash("Wrong username or password", "error")
            return redirect(url_for("register"))

    # GET request → show registration form
    return render_template("register.html")


@app.route("/property/<int:property_id>/enquiry", methods=["POST"])
def send_enquiry(property_id):
    tourist_id = session.get("tourist_id")
    if not tourist_id:
        return redirect(url_for("index"))

    text = request.form.get("text")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    models.create_enquiry(tourist_id=tourist_id, property_id=property_id, text=text, start_date=start_date, end_date=end_date)

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

    models.addBookmark(session.get("tourist_id"), property_id, request.form.get("notes", ""))

    return redirect(url_for("property_details", property_id=property_id))


@app.route("/bookmarks.html")
def getBookmarks():
    tourist_id = session.get("tourist_id") #Is it possible to do this in a separet method for the whole
    if not tourist_id:
        return redirect(url_for("index"))

    bookmarks = models.getBookmarks(tourist_id)
    main_images = []
    for bookmark in bookmarks:
        images = models.getAllImagesProperty(bookmark["property_id"])
        image = images[0] if images else None
        main_images.append(image)
    return render_template("bookmarks.html", bookmarks=bookmarks, main_images=main_images)

#Must add logic for this: (This is to be able to update the database when a property is updated in listings.html)
#@app.route("/property/<int:property_id>/edit", methods=["POST"])
#def edit_property(property_id):




@app.route("/property/add", methods=["POST"])
@auth.seller_required
def addProperty():
    owner_id = session.get("owner_id")
    
    
    name = request.form.get("name")
    price_per_night = request.form.get("price_per_night")
    property_type_id = request.form.get("property_type_id")
    address = request.form.get("address")
    location = request.form.get("location")
    beds = request.form.get("beds")
    bedrooms = request.form.get("bedrooms")
    bathrooms = request.form.get("bathrooms")
    area = request.form.get("area")
    description = request.form.get("description")

    # facilities
    has_parking = 1 if request.form.get("has_parking") else 0
    has_wifi = 1 if request.form.get("has_wifi") else 0
    has_kitchen = 1 if request.form.get("has_kitchen") else 0
    has_boat = 1 if request.form.get("has_boat") else 0
    has_fireplace = 1 if request.form.get("has_fireplace") else 0
    has_tv = 1 if request.form.get("has_tv") else 0
    has_washer = 1 if request.form.get("has_washer") else 0
    has_lounge = 1 if request.form.get("has_lounge") else 0
    has_sauna = 1 if request.form.get("has_sauna") else 0
    has_grill = 1 if request.form.get("has_grill") else 0
    is_pet_friendly = 1 if request.form.get("is_pet_friendly") else 0
    has_board_games = 1 if request.form.get("has_board_games") else 0

    models.addProperty(
        owner_id=owner_id, name=name, price_per_night=price_per_night,
        property_type_id=property_type_id, address=address, location=location,
        beds=beds, bedrooms=bedrooms, bathrooms=bathrooms, area=area,
        description=description, has_parking=has_parking, has_wifi=has_wifi,
        has_kitchen=has_kitchen, has_boat=has_boat, has_fireplace=has_fireplace,
        has_tv=has_tv, has_washer=has_washer, has_lounge=has_lounge,
        has_sauna=has_sauna, has_grill=has_grill, is_pet_friendly=is_pet_friendly,
        has_board_games=has_board_games
    )
    return redirect(url_for("listings"))