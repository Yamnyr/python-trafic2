# import pandas as pd
# from matplotlib import pyplot as plt
# import seaborn as sns

# path="C:/Users/bejao/Onedrive/data/airports.xlsx"
# data = pd.read_csv(path, skiprows=2, index_col='customerid')
# data


#------------------importation du csv-----------------------------------------------

sqlite3 nom_de_la_base_de_donnees.db

.mode csv

.import /chemin/vers/votre_fichier.csv nom_de_la_table

#Assurez-vous d'avoir installé la bibliothèque pandas pour faciliter la manipulation des données CSV. Vous pouvez l'installer avec pip :
# pip install pandas

import sqlite3
import pandas as pd

# Chemin vers le fichier CSV
csv_file = '/path/to/airports.csv'

# Connexion à la base de données SQLite (création si elle n'existe pas)
conn = sqlite3.connect('mydatabase.db')

# Lecture du fichier CSV dans un DataFrame pandas
df = pd.read_csv(csv_file)

# Importation du DataFrame dans la table SQLite
df.to_sql('airports', conn, if_exists='replace', index=False)

# Fermeture de la connexion
conn.close()




#------------------Creation tables--------------------------------------------------


CREATE TABLE airports (
    faa VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    lat FLOAT,
    lon FLOAT,
    tz VARCHAR(50),
    dst INT
);

CREATE TABLE airlines (
    carrier VARCHAR(2) PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE planes (
    tailnum VARCHAR(10) PRIMARY KEY,
    model VARCHAR(100),
    manufacturer VARCHAR(100)
);

CREATE TABLE flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INT,
    month INT,
    day INT,
    hour INT,
    origin VARCHAR(3),
    dest VARCHAR(3),
    carrier VARCHAR(2),
    tailnum VARCHAR(10),
    cancelled INT,
    FOREIGN KEY (origin) REFERENCES airports(faa),
    FOREIGN KEY (dest) REFERENCES airports(faa),
    FOREIGN KEY (carrier) REFERENCES airlines(carrier),
    FOREIGN KEY (tailnum) REFERENCES planes(tailnum)
);

#------------------------------Requete de base------------------------------------------------------------------


SELECT * FROM flights 
WHERE carrier IN ('UA', 'AA', 'DL');


SELECT dest, carrier 
FROM flights 
GROUP BY dest, carrier 
HAVING COUNT(DISTINCT carrier) = 1;


SELECT carrier, COUNT(DISTINCT origin) AS origin_count 
FROM flights 
GROUP BY carrier 
HAVING origin_count < (SELECT COUNT(DISTINCT faa) FROM airports);


SELECT dest, COUNT(*) AS flight_count 
FROM flights 
GROUP BY dest 
ORDER BY flight_count DESC;


SELECT COUNT(*) AS flight_count, 
       COUNT(DISTINCT carrier) AS company_count, 
       COUNT(DISTINCT tailnum) AS unique_planes 
FROM flights 
WHERE origin IN ('JFK', 'LGA', 'EWR') AND dest = 'SEA';

SELECT * FROM flights 
WHERE dest IN ('IAH', 'HOU');

SELECT carrier, COUNT(DISTINCT dest) AS destination_count 
FROM flights 
GROUP BY carrier;


SELECT tailnum, COUNT(*) AS departure_count 
FROM flights 
GROUP BY tailnum 
ORDER BY departure_count DESC 
LIMIT 10;


SELECT dest, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM flights) AS percentage 
FROM flights 
GROUP BY dest 
ORDER BY percentage DESC 
LIMIT 10;


SELECT dest, COUNT(*) AS flight_count 
FROM flights 
GROUP BY dest 
ORDER BY flight_count DESC 
LIMIT 10;


SELECT origin, COUNT(*) AS flight_count 
FROM flights 
GROUP BY origin 
ORDER BY flight_count DESC 
LIMIT 1;


SELECT COUNT(DISTINCT carrier) AS total_companies, 
       COUNT(DISTINCT tailnum) AS total_planes, 
       COUNT(*) AS total_cancelled_flights 
FROM flights WHERE cancelled = 1;

SELECT COUNT(DISTINCT tzone) AS timezones FROM airports;


SELECT COUNT(DISTINCT faa) AS non_dst_airports FROM airports WHERE dst != 23;


SELECT COUNT(DISTINCT origin) AS total_departure_airports, COUNT(DISTINCT dest) AS total_destination_airports FROM flights;


SELECT COUNT(DISTINCT faa) AS total_airports FROM airports;



#le lien chatgpt avec tout ca bien ecrit https://chatgpt.com/share/67053321-2918-800e-8868-6257e12fdaf1