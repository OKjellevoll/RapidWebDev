CREATE DATABASE IF NOT EXISTS RWD;
USE RWD;

CREATE TABLE IF NOT EXISTS owners (
    owner_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tourists (
    tourist_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS property_types (
    property_type_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS properties (
    property_id INTEGER PRIMARY KEY AUTO_INCREMENT,
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
);

CREATE TABLE IF NOT EXISTS images (
    image_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    property_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,

    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

CREATE TABLE IF NOT EXISTS enquiries (
    enquiry_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    tourist_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,

    text TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    response TEXT,
    accepted BOOLEAN DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (tourist_id) REFERENCES tourists(tourist_id),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

CREATE TABLE IF NOT EXISTS bookmarks (
    tourist_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,
    notes TEXT,

    FOREIGN KEY (tourist_id) REFERENCES tourists(tourist_id),
    FOREIGN KEY (property_id) REFERENCES properties(property_id),

    UNIQUE(tourist_id, property_id)
);