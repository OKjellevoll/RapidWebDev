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


def getAllProperties():
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM properties")
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