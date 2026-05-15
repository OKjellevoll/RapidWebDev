import sqlite3

DB_NAME = "RWD.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tourists (
            tourist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS property_types (
            property_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            property_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            property_type_id INTEGER NOT NULL,

            name TEXT NOT NULL,
            description TEXT,
            price_per_night REAL NOT NULL,
            address TEXT NOT NULL,
            location TEXT NOT NULL,

            beds INTEGER NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            area REAL,

            notification_count INTEGER DEFAULT 0,

            has_parking BOOLEAN DEFAULT 0,
            has_wifi BOOLEAN DEFAULT 0,
            has_kitchen BOOLEAN DEFAULT 0,
            has_boat BOOLEAN DEFAULT 0,
            has_fireplace BOOLEAN DEFAULT 0,
            has_tv BOOLEAN DEFAULT 0,
            has_washer BOOLEAN DEFAULT 0,
            has_lounge BOOLEAN DEFAULT 0,
            has_sauna BOOLEAN DEFAULT 0,
            has_grill BOOLEAN DEFAULT 0,
            is_pet_friendly BOOLEAN DEFAULT 0,
            has_board_games BOOLEAN DEFAULT 0,

            FOREIGN KEY (owner_id) REFERENCES owners(owner_id),
            FOREIGN KEY (property_type_id) REFERENCES property_types(property_type_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER NOT NULL,
            image_url TEXT NOT NULL,

            FOREIGN KEY (property_id) REFERENCES properties(property_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            enquiry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tourist_id INTEGER NOT NULL,
            property_id INTEGER NOT NULL,

            text TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            response TEXT,
            accepted BOOLEAN DEFAULT 0,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (tourist_id) REFERENCES tourists(tourist_id),
            FOREIGN KEY (property_id) REFERENCES properties(property_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            bookmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tourist_id INTEGER NOT NULL,
            property_id INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (tourist_id) REFERENCES tourists(tourist_id),
            FOREIGN KEY (property_id) REFERENCES properties(property_id),

            UNIQUE(tourist_id, property_id)
        )
    """)

    conn.commit()
    conn.close()


    def createData():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
 
    
    cursor.executemany("""
        INSERT OR IGNORE INTO owners (username, password, email) VALUES (?, ?, ?)
    """, [
        ("Orjan",  "Password123",  "Ok@gmail.com"),
        ("Jens",   "Secret",       "jens@hotmail.com"),
        ("Johan",  "Secret1",      "johan@example.com"),
        ("Theo",   "TheoTennis",   "Theo@gmail.com"),
        ("Jeppe1", "JeppeisBest",  "Jeppe@outlook.com"),
    ])
 
    # Tourists
    cursor.executemany("""
        INSERT OR IGNORE INTO tourists (username, password, email) VALUES (?, ?, ?)
    """, [
        ("MagnusT",    "Secret",     "Magnus@gmail.com"),
        ("AskTommer",  "Secret1",    "Ask@gmail.com"),
        ("Sturl",      "Password2",  "SturlaRessel@outlook.com"),
        ("Kristian",   "Heihei2",    "KristianPen@icloud.com"),
        ("Aamund",     "imsmart",    "AamundSmart@gmail.com"),
    ])
 
    # Property types
    cursor.executemany("""
        INSERT OR IGNORE INTO property_types (title, description) VALUES (?, ?)
    """, [
        ("Mountain", "Mountain cabins are all over Norway. In the winter Norwegians love to go skiing, and in summertimes hiking from a mountain cabin is the norwegian dream"),
        ("Woods",    "The norwegian woods are mystical and remote. If you want to take some time off, this is the perfect type for you"),
        ("Fjord",    "There are no fjords like the norwegian fjords. These cabins are located in one of our many famous fjords"),
        ("Seaside",  "More famous for our mountains and fjords our coastline is really underrated. With an island archipelago all along the southern coast this is the perfect way to spend norwegian summers."),
        ("Lake",     "Norway also have a lot of lakes. If you like fishing and relaxing this type is for you"),
    ])
 
    # Properties
    cursor.executemany("""
        INSERT OR IGNORE INTO properties (
            property_id, owner_id, property_type_id, name, description,
            price_per_night, address, location, beds, bedrooms, bathrooms, area,
            has_parking, has_wifi, has_kitchen, has_boat, has_fireplace,
            has_tv, has_washer, has_lounge, has_sauna, has_grill,
            is_pet_friendly, has_board_games
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (1, 1, 4, "Sogne",      "Island cabin in the south of Norway",  150, "Risoya 14",        "Sogne",    14, 6, 2, 120, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0),
        (2, 2, 1, "Varatal",    "Vakker hytte rett ved vannet",          200, "Hustunet 3",       "Sauda",     9, 4, 1,  80, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0),
        (3, 3, 2, "Nordefjell", "Rustikk kose midti skogen",             800, "Nordfjellivegen 12","Nordefjell",11,4, 1, 110, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1),
        (4, 1, 3, "Lofoten",    "Rolig hytte med utsikt over fjellet",   600, "Lofotenvegen 43",  "Lofoten",  15, 5, 3, 160, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1),
        (5, 4, 4, "Lyngsalp",   "Vakker hytte rett ved vannet",          300, "Farsundvegen 12",  "Farsund",   4, 2, 2, 100, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0),
    ])
 
    # Images
    cursor.executemany("""
        INSERT OR IGNORE INTO images (property_id, image_url) VALUES (?, ?)
    """, [
        (1, "img/SogneDrone.jpg"),
        (1, "img/SogneAneks.jpg"),
        (1, "img/SogneUte.jpg"),
        (2, "img/Varstolute.jpg"),
        (2, "img/SognePeis.jpg"),
    ])
 
    # Enquiries
    cursor.executemany("""
        INSERT OR IGNORE INTO enquiries (
            enquiry_id, tourist_id, property_id, text,
            start_date, end_date, response, accepted
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (1, 1, 1, "Hi! Im wondering if the cabin is free for easter",                          "2026-04-01", "2026-04-04", "Yes it is free",       1),
        (2, 2, 2, "Hi, I would love to live here for a week",                                  "2026-06-10", "2026-06-15", None,                   0),
        (3, 3, 3, "This looks nice",                                                            "2026-07-20", "2026-07-27", "Accepted",             1),
        (4, 4, 3, "We are a family of 5 and we want to stay at this place for a month",        "2026-07-20", "2026-08-19", "Sorry, it is not available", 0),
        (5, 5, 3, "Please let me rent",                                                        "2026-07-20", "2026-07-27", "No!",                  0),
    ])
 
    conn.commit()
    conn.close()
    print("Database seeded successfully!")



create_tables()