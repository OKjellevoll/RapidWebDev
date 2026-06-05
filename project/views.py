from flask import render_template, request, redirect, url_for, session, flash
from project import app
from project import models
from project import forms
from datetime import date



@app.route("/")
@app.route("/index.html")
def index():
    search = request.args.get('search', '')
    property_type = request.args.get('property_type')
    min_bedrooms = request.args.get('min_bedrooms')
    has_boat = request.args.get('has_boat')
    has_sauna = request.args.get('has_sauna')
    has_parking = request.args.get('has_parking')
    has_wifi = request.args.get('has_wifi')
    has_fireplace = request.args.get('has_fireplace')
    has_kitchen = request.args.get('has_kitchen')
    has_tv = request.args.get('has_tv')
    has_washer = request.args.get('has_washer')

    properties_list = models.filtering(
        search=search,
        property_type=property_type,
        min_bedrooms=min_bedrooms,
        has_boat=has_boat,
        has_sauna=has_sauna,
        has_parking=has_parking,
        has_wifi=has_wifi,
        has_fireplace=has_fireplace,
        has_kitchen=has_kitchen,
        has_tv=has_tv,
        has_washer=has_washer

    )
    current_user = forms.get_current_user()
    main_images = []
    for property in properties_list:
        images = models.getAllImagesProperty(property["property_id"])
        image = images[0] if images else None
        main_images.append(image)
    return render_template("index.html", properties=properties_list, current_user=current_user, main_images=main_images)

@app.route("/listings.html")
@forms.seller_required
def listings():
    owner_id = session.get("owner_id")
    if not owner_id:
        return redirect(url_for("index"))
    properties_list = models.getPropertyByOwner(owner_id)
    enquiries = models.getEnquiriesForOwner(owner_id)
    unanswered = sum(1 for e in enquiries if not e["response"])
    main_images = []
    for listing in properties_list:
        images = models.getAllImagesProperty(listing["property_id"])
        image = images[0] if images else None
        main_images.append(image)
    return render_template("listings.html", properties=properties_list, main_images=main_images, enquiries=enquiries, unanswered=unanswered)


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
    return forms.login_owner(username, password)


@app.route("/tourist/login", methods=["POST"])
def tourist_login():
    username = request.form.get("username")
    password = request.form.get("password")
    return forms.login_tourist(username, password)


@app.route("/logout")
def logout():
    return forms.logout_user()


# ------------------ Registration ------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    errors = {}
    form_data = {}

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        email = request.form.get("email", "")
        role = request.form.get("role", "")

        form_data = {"username": username, "email": email, "role": role}

        if "@" not in email:
            errors["email"] = "Email must contain @"  #Added input validation

        if models.usernameExists(username, role):
            errors["username"] = "Username already exists"

        if "@" in email and models.emailExists(email, role):
            errors["email"] = "Email already exists"

        if not errors:
            success, message = forms.register_user(username, password, email, role)
            if success:
                flash("Account created successfully!", "success")
                return redirect(url_for("index"))
            else:
                flash(message, "danger")

    return render_template("register.html", errors=errors, form_data=form_data)


@app.route("/property/<int:property_id>/enquiry", methods=["POST"])
def send_enquiry(property_id):
    tourist_id = session.get("tourist_id")
    if not tourist_id:
        return redirect(url_for("index"))

    text = request.form.get("text")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    today = date.today().isoformat()

    #Input validation for requested date in the enquiry
    if start_date < today: 
        flash("Check-in date must be today or later", "danger") 
        return redirect(url_for("property_details", property_id=property_id))

    if end_date <= start_date:
        flash("Check-out date must be after check-in date", "danger")
        return redirect(url_for("property_details", property_id=property_id))

    models.create_enquiry(tourist_id=tourist_id, property_id=property_id, text=text, start_date=start_date, end_date=end_date)
    return redirect(url_for("property_details", property_id=property_id))



@app.route("/property/<int:property_id>/bookmark", methods=["POST"])
def addBookmark(property_id):
    tourist_id = session.get("tourist_id") #To get the correct bookmark list for this sessions tourist, same logic as listings (owner)
    if not tourist_id:
        return redirect(url_for("index"))

    models.addBookmark(session.get("tourist_id"), property_id, request.form.get("notes", ""))

    return redirect(url_for("property_details", property_id=property_id))

@app.route("/property/<int:property_id>/bookmark/remove", methods=["POST"])
def removeBookmark(property_id):
    tourist_id = session.get("tourist_id")
    if not tourist_id:
        return redirect(url_for("index"))
    models.removeBookmark(tourist_id, property_id)
    return redirect(url_for("getBookmarks"))


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
@forms.seller_required
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



#EnquieryResponse
@app.route("/enquiry/<int:enquiry_id>/respond", methods=["POST"])
@forms.seller_required
def respondToEnquiry(enquiry_id):
    response = request.form.get("response")
    accepted = 1 if request.form.get("accepted") else 0
    models.respondToEnquiry(enquiry_id, response, accepted)
    return redirect(url_for("owner_enquiries"))

#methods for error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500