"""Database initialization and operations"""

import sqlite3
import os
from typing import List, Dict, Any

DB_PATH = "database/tripadvisor.db"


def init_db():
    """Initialize database with schema and sample data"""
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Cities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            country TEXT
        )
    """)

    # Attractions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY,
            city_id INTEGER,
            name TEXT,
            description TEXT,
            category TEXT,
            rating REAL,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        )
    """)

    # Insert cities
    cities_data = [
        (1, "London", "UK"),
        (2, "Paris", "France"),
        (3, "New York", "USA"),
        (4, "Bangalore", "India"),
        (5, "Chicago", "USA"),
        (6, "Florida", "USA")
    ]
    cursor.executemany("INSERT OR IGNORE INTO cities VALUES (?, ?, ?)", cities_data)

    # Insert attractions
    attractions_data = [
        # London
        (1, 1, "Big Ben", "Historic clock tower", "Monument", 4.7),
        (2, 1, "Tower of London", "Historic fortress", "Museum", 4.6),
        (3, 1, "Buckingham Palace", "Royal residence", "Palace", 4.5),
        # Paris
        (4, 2, "Eiffel Tower", "Iron tower landmark", "Monument", 4.8),
        (5, 2, "Louvre Museum", "Art museum", "Museum", 4.7),
        (6, 2, "Notre-Dame", "Cathedral", "Religious", 4.6),
        # New York
        (7, 3, "Statue of Liberty", "Famous monument", "Monument", 4.7),
        (8, 3, "Central Park", "Urban park", "Park", 4.6),
        (9, 3, "Empire State Building", "Skyscraper", "Landmark", 4.5),
        # Bangalore
        (10, 4, "Vidhana Soudha", "Government building", "Government", 4.4),
        (11, 4, "Lalbagh", "Botanical garden", "Garden", 4.3),
        (12, 4, "Bangalore Palace", "Historic palace", "Palace", 4.2),
        # Chicago
        (13, 5, "Willis Tower", "Skyscraper", "Landmark", 4.5),
        (14, 5, "Millennium Park", "Urban park", "Park", 4.6),
        (15, 5, "Art Institute", "Art museum", "Museum", 4.7),
        # Florida
        (16, 6, "Miami Beach", "Beach", "Beach", 4.6),
        (17, 6, "Kennedy Space Center", "Space center", "Museum", 4.7),
        (18, 6, "Everglades", "Nature reserve", "Nature", 4.5),
    ]
    cursor.executemany("INSERT OR IGNORE INTO attractions VALUES (?, ?, ?, ?, ?, ?)", attractions_data)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


def get_all_cities() -> List[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cities")
    cities = [row[0] for row in cursor.fetchall()]
    conn.close()
    return cities


def get_attractions(city: str) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.name, a.description, a.category, a.rating
        FROM attractions a
        JOIN cities c ON a.city_id = c.id
        WHERE c.name = ?
        LIMIT 3
    """, (city,))
    results = cursor.fetchall()
    conn.close()

    return [
        {"name": r[0], "description": r[1], "category": r[2], "rating": r[3]}
        for r in results
    ]


if __name__ == "__main__":
    init_db()
