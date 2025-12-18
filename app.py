from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

# Remplacez par votre clé API de WeatherAPI.com (gratuit)
API_KEY = "37d002cff3974941883141248252910"
BASE_URL = "https://api.weatherapi.com/v1/current.json"

# Traduction des jours en français
JOURS_FR = {
    'Monday': 'Lun',
    'Tuesday': 'Mar',
    'Wednesday': 'Mer',
    'Thursday': 'Jeu',
    'Friday': 'Ven',
    'Saturday': 'Sam',
    'Sunday': 'Dim'
}

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    """Endpoint pour la météo actuelle"""
    city = request.args.get('city', '')
    
    if not city:
        return jsonify({'error': 'Veuillez spécifier une ville'}), 400
    
    try:
        # Appel à l'API WeatherAPI pour la météo actuelle
        url = f"{BASE_URL}/current.json"
        params = {
            'key': API_KEY,
            'q': city,
            'lang': 'fr'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Formater la réponse
        weather_data = {
            'ville': data['location']['name'],
            'pays': data['location']['country'],
            'temperature': round(data['current']['temp_c']),
            'condition': data['current']['condition']['text'],
            'icone': f"https:{data['current']['condition']['icon']}",
            'vent_kph': round(data['current']['wind_kph']),
            'humidite': data['current']['humidity']
        }
        
        return jsonify(weather_data)
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            return jsonify({'error': 'Ville introuvable'}), 404
        return jsonify({'error': 'Erreur lors de la récupération des données'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/forecast')
def get_forecast():
    """Endpoint pour les prévisions sur 7 jours"""
    city = request.args.get('city', '')
    
    if not city:
        return jsonify({'error': 'Veuillez spécifier une ville'}), 400
    
    try:
        # Appel à l'API WeatherAPI pour les prévisions
        url = f"{BASE_URL}/forecast.json"
        params = {
            'key': API_KEY,
            'q': city,
            'days': 7,
            'lang': 'fr'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Formater les prévisions
        previsions = []
        for day in data['forecast']['forecastday']:
            date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
            jour_anglais = date_obj.strftime('%A')
            jour_fr = JOURS_FR.get(jour_anglais, jour_anglais[:3])
            
            previsions.append({
                'jour': jour_fr,
                'temp_max': round(day['day']['maxtemp_c']),
                'temp_min': round(day['day']['mintemp_c']),
                'condition': day['day']['condition']['text'],
                'icone': f"https:{day['day']['condition']['icon']}"
            })
        
        return jsonify({'previsions': previsions})
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            return jsonify({'error': 'Ville introuvable'}), 404
        return jsonify({'error': 'Erreur lors de la récupération des prévisions'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)