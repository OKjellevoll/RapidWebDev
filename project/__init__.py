from flask import Flask
import mysql.connector
import os
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "RWD-secret-key"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Norway2001",
    "database": "RWD"
}

conn = mysql.connector.connect(host=DB_CONFIG["host"], user=DB_CONFIG["user"], password=DB_CONFIG["password"])
cursor = conn.cursor()
sql_path = os.path.join(os.path.dirname(__file__), "database.sql")
with open(sql_path, "r") as f:
    for statement in f.read().split(";"):
        if statement.strip():
            cursor.execute(statement)
conn.commit()
conn.close()


def createData():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT IGNORE INTO owners (username, password, email) VALUES (%s, %s, %s)
    """, [
        ("OrjanOwner",  generate_password_hash("Password1", method="pbkdf2:sha256"),  "Ok@gmail.com"),
        ("Jens",   generate_password_hash("Secret",      method="pbkdf2:sha256"),  "jens@hotmail.com"),
        ("Johan",  generate_password_hash("Secret1",     method="pbkdf2:sha256"),  "johan@example.com"),
        ("Theo",   generate_password_hash("TheoTennis",  method="pbkdf2:sha256"),  "Theo@gmail.com"),
        ("Jeppe1", generate_password_hash("JeppeisBest", method="pbkdf2:sha256"),  "Jeppe@outlook.com"),
    ])

    cursor.executemany("""
        INSERT IGNORE INTO tourists (username, password, email) VALUES (%s, %s, %s)
    """, [
        ("OrjanBuyer1",   generate_password_hash("Password1",    method="pbkdf2:sha256"), "Magnus@gmail.com"),
        ("AskTommer", generate_password_hash("Secret1",   method="pbkdf2:sha256"), "Ask@gmail.com"),
        ("Sturl",     generate_password_hash("Password2", method="pbkdf2:sha256"), "SturlaRessel@outlook.com"),
        ("Kristian",  generate_password_hash("Heihei2",   method="pbkdf2:sha256"), "KristianPen@icloud.com"),
        ("Aamund",    generate_password_hash("imsmart",   method="pbkdf2:sha256"), "AamundSmart@gmail.com"),
    ])

    cursor.executemany("""
        INSERT IGNORE INTO property_types (title, description) VALUES (%s, %s)
    """, [
        ("Mountain", "Mountain cabins are all over Norway. In the winter Norwegians love to go skiing, and in summertimes hiking from a mountain cabin is the norwegian dream"),
        ("Woods",    "The norwegian woods are mystical and remote. If you want to take some time off, this is the perfect type for you"),
        ("Fjord",    "There are no fjords like the norwegian fjords. These cabins are located in one of our many famous fjords"),
        ("Seaside",  "More famous for our mountains and fjords our coastline is really underrated. With an island archipelago all along the southern coast this is the perfect way to spend norwegian summers."),
        ("Lake",     "Norway also have a lot of lakes. If you like fishing and relaxing this type is for you"),
    ])

    cursor.executemany("""
        INSERT IGNORE INTO properties (
            property_id, owner_id, property_type_id, name, description,
            price_per_night, address, location, beds, bedrooms, bathrooms, area,
            has_parking, has_wifi, has_kitchen, has_boat, has_fireplace,
            has_tv, has_washer, has_lounge, has_sauna, has_grill,
            is_pet_friendly, has_board_games
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [
        (1, 1, 4, "Sogne",      "Island cabin in the south of Norway", 150, "Risoya 14",          "Sogne",      14, 6, 2, 120, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0),
        (2, 2, 1, "Varstol",    "Vakker hytte rett ved vannet",         200, "Hustunet 3",         "Sauda",       9, 4, 1,  80, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0),
        (3, 3, 2, "Nordefjell", "Rustikk kose midti skogen",            800, "Nordfjellivegen 12", "Nordefjell", 11, 4, 1, 110, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1),
        (4, 1, 3, "Lofoten",    "Rolig hytte med utsikt over fjellet",  600, "Lofotenvegen 43",    "Lofoten",    15, 5, 3, 160, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1),
        (5, 4, 4, "Lyngsvaag",   "Vakker hytte rett ved vannet",         300, "Farsundvegen 12",    "Farsund",     4, 2, 2, 100, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0),
    ])

    cursor.executemany("""
        INSERT IGNORE INTO images (property_id, image_url) VALUES (%s, %s)
    """, [
        (1, "img/SogneDrone.jpg"),
        (1, "img/SogneAneks.jpg"),
        (1, "img/SogneUte.jpg"),
        (2, "img/Varstolute.jpg"),
        (2, "img/DroneVårstøl.jpg"),
        (2, "img/SognePeis.jpg"),
    ])

    cursor.executemany("""
        INSERT IGNORE INTO enquiries (
            enquiry_id, tourist_id, property_id, text,
            start_date, end_date, response, accepted
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, [
        (1, 1, 1, "Hi! Im wondering if the cabin is free for easter",               "2026-04-01", "2026-04-04", "Yes it is free",             1),
        (2, 2, 2, "Hi, I would love to live here for a week",                       "2026-06-10", "2026-06-15", None,                         0),
        (3, 3, 3, "This looks nice",                                                "2026-07-20", "2026-07-27", "Accepted",                   1),
        (4, 4, 3, "We are a family of 5 and we want to stay at this place for a month", "2026-07-20", "2026-08-19", "Sorry, it is not available", 0),
        (5, 5, 3, "Please let me rent",                                             "2026-07-20", "2026-07-27", "No!",                        0),
    ])

    conn.commit()
    conn.close()


createData()

from project import views