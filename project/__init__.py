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
        ("Orjan",  generate_password_hash("Password123", method="pbkdf2:sha256"),  "Ok@gmail.com"),
        ("Jens",   generate_password_hash("Secret",      method="pbkdf2:sha256"),  "jens@hotmail.com"),
        ("Johan",  generate_password_hash("Secret1",     method="pbkdf2:sha256"),  "johan@example.com"),
        ("Theo",   generate_password_hash("TheoTennis",  method="pbkdf2:sha256"),  "Theo@gmail.com"),
        ("Jeppe1", generate_password_hash("JeppeisBest", method="pbkdf2:sha256"),  "Jeppe@outlook.com"),
    ])

    cursor.executemany("""
        INSERT IGNORE INTO tourists (username, password, email) VALUES (%s, %s, %s)
    """, [
        ("MagnusT",   generate_password_hash("Secret",    method="pbkdf2:sha256"), "Magnus@gmail.com"),
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
        (1,  1, 4, "Sogne",        "Island cabin in the south of Norway",              150, "Risoya 14",           "Sogne",        14, 6, 2, 120, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0),
        (2,  2, 1, "Varstol",      "Cozy mountain cabin with great views",             200, "Hustunet 3",          "Sauda",         9, 4, 1,  80, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0),
        (3,  3, 2, "Nordefjell",   "Rustic cabin in the heart of the woods",           800, "Nordfjellivegen 12",  "Nordefjell",   11, 4, 1, 110, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1),
        (4,  1, 3, "Lofoten",      "Peaceful cabin with stunning mountain views",      600, "Lofotenvegen 43",     "Lofoten",      15, 5, 3, 160, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1),
        (5,  4, 4, "Kragerø",      "Beautiful seaside cabin in the Telemark coast",   350, "Strandvegen 5",       "Kragerø",       6, 3, 1,  90, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0),
        (6,  2, 4, "Kristiansand", "Sunny coastal cabin close to Sørlandet beaches",  280, "Kystveien 12",        "Kristiansand",  8, 3, 2, 100, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1),
        (7,  3, 5, "Kviteseid",    "Lakeside cabin perfect for fishing and kayaking", 220, "Kviteseidsveien 8",   "Kviteseid",     5, 2, 1,  70, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0),
        (8,  5, 4, "Risør",        "Charming white-painted cabin by the sea",         310, "Havnegata 3",         "Risør",         4, 2, 1,  65, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0),
        (9,  1, 1, "Røros",        "Historic mountain cabin near Røros town center",  400, "Bergmannsgata 7",     "Røros",         6, 3, 1,  85, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1),
        (10, 2, 4, "Senja",        "Remote island cabin with dramatic scenery",       500, "Senjakvegen 22",      "Senja",        10, 4, 2, 130, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0),
        (11, 3, 3, "Sirdal",       "Fjord cabin with private dock and boat access",   450, "Sirdalsvegen 18",     "Sirdal",        8, 3, 2, 105, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1),
        (12, 4, 2, "Skien",        "Quiet forest cabin close to Telemark canal",      180, "Skogsveien 4",        "Skien",         4, 2, 1,  60, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0),
        (13, 5, 3, "Suldal",       "Scenic fjord cabin with panoramic water views",   380, "Suldalsvegen 9",      "Suldal",        7, 3, 1,  95, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0),
        (14, 1, 1, "Tromsø",       "Arctic cabin with northern lights experience",    700, "Polarvegen 11",       "Tromsø",        8, 3, 2, 110, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1),
        (15, 2, 4, "Tvedestrand",  "Idyllic archipelago cabin on the south coast",   260, "Øyvegen 6",           "Tvedestrand",   5, 2, 1,  75, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0),
    ])

    cursor.executemany("""
        INSERT IGNORE INTO images (property_id, image_url) VALUES (%s, %s)
    """, [
        (1,  "img/SogneDrone.jpg"),
        (1,  "img/SogneAneks.jpg"),
        (1,  "img/SogneUte.jpg"),
        (1,  "img/SogneStue.jpg"),
        (2,  "img/DroneVarstol.jpg"),
        (2,  "img/VarstolPeis.png"),
        (2,  "img/VarstolTerrase.jpg"),
        (3,  "img/NorefjellDrone.jpg"),
        (3,  "img/NorefjellMain.jpg"),
        (3,  "img/NorefjellStue.jpg"),
        (4,  "img/LofotenDrone.jpg"),
        (4,  "img/LofotenMain.jpg"),
        (4,  "img/LofotenStue.jpg"),
        (5,  "img/KragerøMain.png"),
        (5,  "img/KragerøStue.png"),
        (6,  "img/KristiansandMain.png"),
        (6,  "img/KristiansandStue.png"),
        (7,  "img/KviteseidMain.png"),
        (7,  "img/KviteseidStue.png"),
        (8,  "img/RisørMain.png"),
        (8,  "img/RisørView.png"),
        (9,  "img/RorosMain.png"),
        (9,  "img/RorosStue.png"),
        (10, "img/SenjaMain.png"),
        (10, "img/SenjaStue.png"),
        (11, "img/SirdalMain.png"),
        (11, "img/SirdalStue.png"),
        (12, "img/SkienMain.png"),
        (12, "img/SkienStue.png"),
        (13, "img/SuldalMain.png"),
        (13, "img/SuldalUtsikt.png"),
        (14, "img/TromsøMain.png"),
        (14, "img/TromsøStue.png"),
        (15, "img/TvedestrandMain.png"),
        (15, "img/TvedestrandStue.png"),
    ])

    conn.commit()
    conn.close()


conn2 = mysql.connector.connect(**DB_CONFIG)
cursor2 = conn2.cursor()
cursor2.execute("SELECT COUNT(*) FROM owners")
count = cursor2.fetchone()[0]
conn2.close()

if count == 0:
    print("Database is empty - running createData()")
    createData()
else:
    print("Database already has data - skipping createData()")

from project import views