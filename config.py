import sqlite3
import pandas as pd
import pdfplumber
import os
from dotenv import load_dotenv

load_dotenv()

# Chemins vers les fichiers
airlines_path = os.getenv("AIRLINES_PATH")
airports_path = os.getenv("AIRPORTS_PATH")
flights_path = os.getenv("FLIGHTS_PATH")
planes_path = os.getenv("PLANES_PATH")
weather_path = os.getenv("WEATHER_PATH")

# Connexion à la base de données SQLite
try:
    conn = sqlite3.connect('trafic5.db')
    print("Connexion à la base de données réussie.")
except Exception as e:
    print(f"Erreur de connexion à la base de données : {e}")

cursor = conn.cursor()

# Création des tables (si elles n'existent pas déjà)

# Table airports
cursor.execute('''
    CREATE TABLE IF NOT EXISTS airports (
        faa VARCHAR(3) PRIMARY KEY, 
        name VARCHAR(100),
        lat FLOAT,
        lon FLOAT,
        alt INT,
        tz VARCHAR(50),
        dst INT,
        tzone VARCHAR(50)
    );
''')

# Table airlines
cursor.execute('''
    CREATE TABLE IF NOT EXISTS airlines (
        carrier VARCHAR(2) PRIMARY KEY,
        name VARCHAR(100)
    );
''')

# Table planes
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

# Table flights
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

# Table weather
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
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
        PRIMARY KEY (year, month, day, hour, origin),
        FOREIGN KEY (origin) REFERENCES airports(faa)
    );
''')

# Table de liaison airline_airport
cursor.execute('''
    CREATE TABLE IF NOT EXISTS airline_airport (
        carrier VARCHAR(2),
        faa VARCHAR(3),
        PRIMARY KEY (carrier, faa),
        FOREIGN KEY (carrier) REFERENCES airlines(carrier),
        FOREIGN KEY (faa) REFERENCES airports(faa)
    );
''')

# Sauvegarde des changements
conn.commit()

## Insérer les données dans la table 'airports'
airports_data = pd.read_excel(airports_path, header=0)
for _, row in airports_data.iterrows():
    cursor.execute('''INSERT OR REPLACE INTO airports (faa, name, lat, lon, alt, tz, dst, tzone) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?);''', 
                   (row['faa'], row['name'], row['lat'], row['lon'], 
                    row['alt'], row['tz'], row['dst'], row['tzone']))

# Insérer les données dans la table 'airlines'
airlines_data = pd.read_json(airlines_path)
for _, row in airlines_data.iterrows():
    cursor.execute('''INSERT OR REPLACE INTO airlines (carrier, name) VALUES (?, ?);''', 
                   (row['carrier'], row['name']))

# Insérer les données dans la table 'flights'
flights_data = pd.read_excel(flights_path, header=None)
_data = flights_data.iloc[:, 0].str.split(",", expand=True)
colonnes = flights_data.iloc[0, 0].split(',')
_data.columns = colonnes
flights_data_cleaned = _data.iloc[1:].reset_index(drop=True)

for col in ['dep_time', 'sched_dep_time', 'dep_delay', 'arr_time', 'sched_arr_time', 'arr_delay', 'air_time', 'distance']:
    flights_data_cleaned[col] = pd.to_numeric(flights_data_cleaned[col], errors='coerce')

# Insérer une seule fois dans la table 'flights'
for _, row in flights_data_cleaned.iterrows():
    cursor.execute('''INSERT OR REPLACE INTO flights (
            year, month, day, dep_time, sched_dep_time, dep_delay, arr_time, sched_arr_time, 
            arr_delay, carrier, flight, tailnum, origin, dest, air_time, distance, hour, 
            minute, time_hour
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', (
        row['year'], row['month'], row['day'], row['dep_time'], row['sched_dep_time'], row['dep_delay'], 
        row['arr_time'], row['sched_arr_time'], row['arr_delay'], row['carrier'], row['flight'], 
        row['tailnum'], row['origin'], row['dest'], row['air_time'], row['distance'], 
        row['hour'], row['minute'], row['time_hour']
    ))

    # Insérer dans airlines_airports pour l'origine et la destination du vol
    cursor.execute('''INSERT OR IGNORE INTO airline_airport (carrier, faa) VALUES (?, ?);''', (row['carrier'], row['origin']))
    cursor.execute('''INSERT OR IGNORE INTO airline_airport (carrier, faa) VALUES (?, ?);''', (row['carrier'], row['dest']))

# Insérer les données dans la table 'planes'
planes_data = pd.read_html(planes_path)[0]  
for _, row in planes_data.iterrows():
    cursor.execute('''INSERT OR REPLACE INTO planes (tailnum, year, type, manufacturer, model, engines, 
                      seats, speed, engine) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''', 
                   (row['tailnum'], row['year'], row['type'], 
                    row['manufacturer'], row['model'], 
                    row['engines'], row['seats'], 
                    row['speed'], row['engine']))

# Charger et traiter le tableau extrait de weather.pdf
data = []
csv_output_path = 'data/weather.csv'
with pdfplumber.open(weather_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            if line.strip():
                data.append(line.split(','))

# Création d'un DataFrame à partir des données extraites
df = pd.DataFrame(data[1:], columns=data[0])

# Convertir les colonnes au bon type
for col in ['year', 'month', 'day', 'hour', 'temp', 'dewp', 'humid', 'wind_dir', 'wind_speed', 
            'wind_gust', 'precip', 'pressure', 'visib']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Insérer les données dans la table 'weather'
for _, row in df.iterrows():
    cursor.execute('''INSERT OR REPLACE INTO weather (
        origin, year, month, day, hour, temp, dewp, humid, wind_dir, wind_speed, 
        wind_gust, precip, pressure, visib, time_hour
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (
        row['origin'], row['year'], row['month'], row['day'], row['hour'], 
        row['temp'], row['dewp'], row['humid'], row['wind_dir'], row['wind_speed'], 
        row['wind_gust'], row['precip'], row['pressure'], row['visib'], row['time_hour']
    ))

# Vérification de l'importation des données dans la table 'weather'
cursor.execute('SELECT COUNT(*) FROM weather;')
count = cursor.fetchone()[0]
print(f"Nombre d'enregistrements dans la table 'weather': {count}")

# Vérification de la table airline_airport
cursor.execute('SELECT COUNT(*) FROM airline_airport;')
count_airline_airport = cursor.fetchone()[0]
print(f"Nombre d'enregistrements dans la table 'airline_airport': {count_airline_airport}")

conn.commit()
conn.close()