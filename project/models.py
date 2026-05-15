import sqlite3

DB_NAME = "RWD.db"

def getConnection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  
    return conn


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


# Get all images from one property
def getAllImagesProperty(property_id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE property_id = ?", (property_id,))
    images = cursor.fetchall()
    conn.close()
    return images


# Checking for username and Password for Owner 
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