import sqlite3 #this file is about the functionality to the app, connects frontend to the SQLite database trough the Routes in views.py

DB_NAME = "RWD.db"

def getConnection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def getOwner(owner_id): #not yet in use, but im not sure if we need it or not later
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM owners WHERE owner_id = ?", (owner_id,))
    owner = cursor.fetchone()
    conn.close()
    return owner


def getTourist(tourist_id): #not yet in use, but not sure if we need it or not for later, maybe 
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tourists WHERE tourist_id = ?", (tourist_id,))
    tourist = cursor.fetchone()
    conn.close()
    return tourist


# Getting all properties
def getAllProperties():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties")
    properties = cursor.fetchall()
    conn.close()
    return properties


# Get one property
def getPropertyById(property_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties WHERE property_id = ?", (property_id,))
    property = cursor.fetchone()
    conn.close()
    return property

def getPropertyByOwner(owner_id):
    conn = getConnection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM properties WHERE owner_id = ?""", (owner_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Get all images from one property
def getAllImagesProperty(property_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE property_id = ?", (property_id,))
    images = cursor.fetchall()
    conn.close()
    return images


# Validation for owner login
def ownerLoginVal(username, password):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM owners WHERE username = ? AND password = ?",
        (username, password)
    )
    owner = cursor.fetchone()
    conn.close()
    return owner


# Validation for tourist login
def touristLoginVal(username, password):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tourists WHERE username = ? AND password = ?",
        (username, password)
    )
    tourist = cursor.fetchone()
    conn.close()
    return tourist


# template Function
def create_enquiry(tourist_id, property_id, text, start_date, end_date):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enquiries (tourist_id, property_id, text, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    """, (tourist_id, property_id, text, start_date, end_date))
    conn.commit()
    conn.close()

def addBookmark(tourist_id, property_id, notes):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookmarks (tourist_id, property_id, notes)
        VALUES (?, ?)
    """, (tourist_id, property_id, notes))
    conn.commit()
    conn.close()

def getBookmarks(tourist_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT properties.* FROM bookmarks
        JOIN properties ON bookmarks.property_id = properties.property_id
        WHERE bookmarks.tourist_id = ?
    """, (tourist_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# must add: def updateProperty(propery_id):
    