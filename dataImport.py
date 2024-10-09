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

print("Contenu de airlines.json :")
airlines_data = pd.read_json(airlines_path)
print(airlines_data.head())

print("\nContenu de airports.xlsx :")
airports_path = pd.read_excel(airports_path)
print(airports_path.head())

print("\nContenu de flights.xlsx :")
flights_data = pd.read_excel(flights_path)
print(flights_data.head())


print("\nContenu du tableau HTML planes.html :")
planes_data = pd.read_html(planes_path)[0]
print(planes_data.head())

print("\nContenu de weather.pdf :")

with pdfplumber.open(weather_path) as pdf:
    for i, page in enumerate(pdf.pages[:1]):
        text = page.extract_text()
        print(f"\nContenu de la page {i + 1} :")
        print(text if text else "Pas de texte trouvé sur cette page.")