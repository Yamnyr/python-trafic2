import sqlite3
# import pandas as pd

# Connexion à la base de données SQLite
try:
    conn = sqlite3.connect('trafic.db')
    print("Connexion à la base de données réussie.")
except Exception as e:
    print(f"Erreur de connexion à la base de données : {e}")

cursor = conn.cursor()

# Création de la table 'airports'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS airports (
        faa VARCHAR(3) PRIMARY KEY,
        name VARCHAR(100),
        lat FLOAT,
        lon FLOAT,
        alt INT,            -- Altitude en pieds
        tz VARCHAR(50),
        dst INT,
        tzone VARCHAR(50)   -- Nom du fuseau horaire
    );
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS airlines (
        carrier VARCHAR(2) PRIMARY KEY,
        name VARCHAR(100)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS planes (
        tailnum VARCHAR(10) PRIMARY KEY,
        year INT,
        type VARCHAR(100),
        manufacturer VARCHAR(100),
        model VARCHAR(100),
        engines INT,
        seats INT,
        speed FLOAT,
        engine VARCHAR(100)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INT,
        month INT,
        day INT,
        dep_time INT,
        sched_dep_time INT,
        dep_delay INT,
        arr_time INT,
        sched_arr_time INT,
        arr_delay INT,
        carrier VARCHAR(2),
        flight VARCHAR(10),
        tailnum VARCHAR(10),
        origin VARCHAR(3),
        dest VARCHAR(3),
        air_time INT,
        distance INT,
        hour INT,
        minute INT,
        time_hour DATETIME,
        FOREIGN KEY (origin) REFERENCES airports(faa),
        FOREIGN KEY (dest) REFERENCES airports(faa),
        FOREIGN KEY (carrier) REFERENCES airlines(carrier),
        FOREIGN KEY (tailnum) REFERENCES planes(tailnum)
    );
''')


# Création de la table weather (si elle n'existe pas déjà)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin VARCHAR(3),
        year INT,
        month INT,
        day INT,
        hour INT,
        temp FLOAT,
        dewp FLOAT,
        humid FLOAT,
        wind_dir FLOAT,
        wind_speed FLOAT,
        wind_gust FLOAT,
        precip FLOAT,
        pressure FLOAT,
        visib FLOAT,
        time_hour DATETIME,
        FOREIGN KEY (origin) REFERENCES airports(faa)
    );
''')


# Sauvegarde des changements
conn.commit()

# Fermeture de la connexion à la base de données
conn.close()
