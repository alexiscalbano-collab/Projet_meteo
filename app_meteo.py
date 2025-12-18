import os
import requests
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not API_KEY or not BASE_URL:
    messagebox.showerror("Erreur", "Clé API ou URL manquante dans le fichier .env")
    exit()

# Fonction pour récupérer la météo
def get_weather(city):
    params = {"key": API_KEY, "q": city, "lang": "fr"}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        messagebox.showerror("Erreur API", f"Ville introuvable : {city}")
        return None
    except requests.exceptions.RequestException:
        messagebox.showerror("Erreur Réseau", "Impossible de se connecter à l'API")
        return None

# Fonction pour afficher la météo avec emoji
def get_weather_emoji(condition):
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
    if not data:
        return ""
    ville = data["location"]["name"]
    pays = data["location"]["country"]
    condition = data["current"]["condition"]["text"]
    temperature = data["current"]["temp_c"]
    humidite = data["current"]["humidity"]
    vent = data["current"]["wind_kph"]
    emoji = get_weather_emoji(condition)
    return (f"📍 {ville}, {pays}\n"
            f"{emoji}  {condition}\n"
            f"🌡️  Température : {temperature} °C\n"
            f"💧 Humidité : {humidite}%\n"
            f"🌬️  Vent : {vent} km/h")

# Fonction déclenchée par le bouton
def chercher():
    ville = ville_entry.get().strip()
    if not ville:
        messagebox.showwarning("Attention", "Veuillez entrer une ville")
        return
    data = get_weather(ville)
    resultat = afficher_meteo(data)
    resultat_label.config(text=resultat)

# Création de la fenêtre principale
root = tk.Tk()
root.title("🌦️ Application Météo France 🌦️")
root.geometry("450x350")

# Widgets
titre = tk.Label(root, text="🌦️ Application Météo France 🌦️", font=("Helvetica", 16))
titre.pack(pady=10)

ville_entry = tk.Entry(root, font=("Helvetica", 14))
ville_entry.pack(pady=10)
ville_entry.insert(0, "Paris")  # Valeur par défaut

chercher_btn = tk.Button(root, text="Chercher la météo", command=chercher, font=("Helvetica", 12))
chercher_btn.pack(pady=10)

resultat_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left")
resultat_label.pack(pady=10)

# Lancer la boucle principale Tkinter
root.mainloop()
