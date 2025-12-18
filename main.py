import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not API_KEY or not BASE_URL:
    print("❌ Clé API ou URL manquante dans le fichier .env")
    exit()

def get_weather(city):
    """Appelle l'API WeatherAPI pour obtenir la météo"""
    params = {
        "key": API_KEY,
        "q": city,
        "lang": "fr"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ Ville introuvable ou erreur API : {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau : {e}")
        return None

def get_weather_emoji(condition):
    """Renvoie un emoji selon la condition météo"""
    condition = condition.lower()
    if "soleil" in condition or "clair" in condition:
        return "☀️"
    elif "pluie" in condition:
        return "🌧️"
    elif "neige" in condition:
        return "❄️"
    elif "nuage" in condition:
        return "☁️"
    elif "orage" in condition:
        return "⛈️"
    else:
        return "🌤️"

def afficher_meteo(data):
    """Affiche la météo joliment formatée"""
    if not data:
        print("⚠️ Impossible d'afficher la météo.")
        return

    ville = data["location"]["name"]
    pays = data["location"]["country"]
    condition = data["current"]["condition"]["text"]
    temperature = data["current"]["temp_c"]
    humidite = data["current"]["humidity"]
    vent = data["current"]["wind_kph"]
    emoji = get_weather_emoji(condition)

    print("\n🌍 --- MÉTÉO ACTUELLE --- 🌍")
    print(f"📍 {ville}, {pays}")
    print(f"{emoji}  {condition}")
    print(f"🌡️  Température : {temperature} °C")
    print(f"💧 Humidité : {humidite}%")
    print(f"🌬️  Vent : {vent} km/h")
    print("-----------------------------")

def main():
    print("=== 🌦️  Application Météo France 🌦️ ===")
    ville = input("Entre le nom d'une ville : ").strip()
    if not ville:
        print("⚠️ Vous n'avez rien saisi. On prend Paris par défaut.")
        ville = "Paris"
    data = get_weather(ville)
    afficher_meteo(data)

if __name__ == "__main__":
    main()
