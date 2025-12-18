from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "37d002cff3974941883141248252910"
BASE_URL = "https://api.weatherapi.com/v1/current.json"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Veuillez entrer une ville"}), 400

    params = {"key": API_KEY, "q": city, "lang": "fr"}
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            return jsonify({"error": data["error"]["message"]}), 404
        
        weather_info = {
            "ville": data["location"]["name"],
            "pays": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "icone": data["current"]["condition"]["icon"],
            "vent_kph": data["current"]["wind_kph"],
            "humidite": data["current"]["humidity"]
        }
        return jsonify(weather_info)
    except requests.exceptions.RequestException:
        return jsonify({"error": "Impossible de récupérer la météo"}), 500

if __name__ == "__main__":
    app.run(debug=True)
