import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Norway2001",
    "database": "RWD"
}


def getConnection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def getOwner(owner_id):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM owners WHERE owner_id = %s", (owner_id,))
    owner = cursor.fetchone()
    conn.close()
    return owner


def getTourist(tourist_id):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tourists WHERE tourist_id = %s", (tourist_id,))
    tourist = cursor.fetchone()
    conn.close()
    return tourist


## def getAllProperties(): NOT IN USE ANYMORE, USING FILTERING INSEAD.
##   conn = getConnection()
##   cursor = conn.cursor(dictionary=True)
##    cursor.execute("SELECT * FROM properties")
##    properties = cursor.fetchall()
##    conn.close()
##    return properties

def filtering(search='', property_type=None, min_bedrooms=None, has_boat=None, has_sauna=None, has_parking=None, has_wifi=None, has_fireplace=None, has_kitchen=None, has_tv=None, has_washer=None):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM properties WHERE 1=1"
    params = []

    if search:
        query += " AND (name LIKE %s OR location LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    if property_type:
        query += " AND property_type_id = %s"
        params.append(property_type)

    if min_bedrooms:
        query += " AND bedrooms >= %s"
        params.append(min_bedrooms)

    if has_boat:
        query += " AND has_boat = 1"

    if has_sauna:
        query += " AND has_sauna = 1"

    if has_parking:
        query += " AND has_parking = 1"
    if has_wifi:
        query += " AND has_wifi = 1"
    if has_fireplace:
        query += " AND has_fireplace = 1"
    if has_kitchen:
        query += " AND has_kitchen = 1"
    if has_tv:
        query += " AND has_tv = 1"
    if has_washer:
        query += " AND has_washer = 1"

    cursor.execute(query, params)
    properties = cursor.fetchall()
    conn.close()
    return properties

def getPropertyById(property_id):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM properties WHERE property_id = %s", (property_id,))
    property = cursor.fetchone()
    conn.close()
    return property

def getPropertyByOwner(owner_id):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM properties WHERE owner_id = %s", (owner_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def getAllImagesProperty(property_id):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM images WHERE property_id = %s", (property_id,))
    images = cursor.fetchall()
    conn.close()
    return images


def ownerLoginVal(username, password):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM owners WHERE username = %s AND password = %s",
        (username, password)
    )
    owner = cursor.fetchone()
    conn.close()
    return owner


def touristLoginVal(username, password):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM tourists WHERE username = %s AND password = %s",
        (username, password)
    )
    tourist = cursor.fetchone()
    conn.close()
    return tourist


def create_enquiry(tourist_id, property_id, text, start_date, end_date):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enquiries (tourist_id, property_id, text, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (tourist_id, property_id, text, start_date, end_date))
    conn.commit()
    conn.close()

def addBookmark(tourist_id, property_id, notes):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookmarks (tourist_id, property_id, notes)
        VALUES (%s, %s, %s)
    """, (tourist_id, property_id, notes))
    conn.commit()
    conn.close()

def removeBookmark(tourist_id, property_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM bookmarks WHERE tourist_id = %s AND property_id = %s
    """, (tourist_id, property_id))
    conn.commit()
    conn.close()

def getBookmarks(tourist_id):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT properties.*, bookmarks.notes FROM bookmarks
        JOIN properties ON bookmarks.property_id = properties.property_id
        WHERE bookmarks.tourist_id = %s
    """, (tourist_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def addProperty(owner_id, name, price_per_night, property_type_id, address,
                location, beds, bedrooms, bathrooms, area, description,
                has_parking, has_wifi, has_kitchen, has_boat, has_fireplace,
                has_tv, has_washer, has_lounge, has_sauna, has_grill,
                is_pet_friendly, has_board_games):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (
            owner_id, name, price_per_night, property_type_id, address,
            location, beds, bedrooms, bathrooms, area, description,
            has_parking, has_wifi, has_kitchen, has_boat, has_fireplace,
            has_tv, has_washer, has_lounge, has_sauna, has_grill,
            is_pet_friendly, has_board_games
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        owner_id, name, price_per_night, property_type_id, address,
        location, beds, bedrooms, bathrooms, area, description,
        has_parking, has_wifi, has_kitchen, has_boat, has_fireplace,
        has_tv, has_washer, has_lounge, has_sauna, has_grill,
        is_pet_friendly, has_board_games
    ))
    conn.commit()
    conn.close()


def respondToEnquiry(enquiry_id, response, accepted):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE enquiries SET response = %s, accepted = %s WHERE enquiry_id = %s
    """, (response, accepted, enquiry_id))
    conn.commit()
    conn.close()

def getEnquiriesForOwner(owner_id):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT enquiries.*, properties.name as property_name
        FROM enquiries
        JOIN properties ON enquiries.property_id = properties.property_id
        WHERE properties.owner_id = %s
    """, (owner_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

#methods for input validation:
def usernameExists(username, role):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    if role == "seller":
        cursor.execute("SELECT owner_id FROM owners WHERE username = %s", (username,))
    else:
        cursor.execute("SELECT tourist_id FROM tourists WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def emailExists(email, role):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    if role == "seller":
        cursor.execute("SELECT owner_id FROM owners WHERE email = %s", (email,))
    else:
        cursor.execute("SELECT tourist_id FROM tourists WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None