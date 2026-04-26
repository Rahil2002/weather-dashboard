from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

# Load the API key from your .env file
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Read the API key from environment
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ── Home route ─────────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Weather Dashboard API",
        "usage": "GET /weather?city=London",
        "endpoints": ["/weather", "/health"]
    })


# ── Weather route ───────────────────────────────────────────
@app.route("/weather")
def get_weather():
    # Get the city name from the URL: /weather?city=London
    city = request.args.get("city")

    # If no city was provided, return a helpful error
    if not city:
        return jsonify({
            "error": "Please provide a city name",
            "example": "/weather?city=Hyderabad"
        }), 400

    # Call the OpenWeatherMap API
    response = requests.get(BASE_URL, params={
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    })

    # If city not found or API error, return the error clearly
    if response.status_code != 200:
        return jsonify({
            "error": f"Could not fetch weather for '{city}'",
            "details": response.json().get("message", "Unknown error")
        }), response.status_code

    # Pull out only the useful data from the API response
    data = response.json()

    weather = {
        "city":        data["name"],
        "country":     data["sys"]["country"],
        "temperature": f"{data['main']['temp']}°C",
        "feels_like":  f"{data['main']['feels_like']}°C",
        "humidity":    f"{data['main']['humidity']}%",
        "wind_speed":  f"{data['wind']['speed']} m/s",
        "condition":   data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
    }

    return jsonify(weather)


# ── Health check route ──────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "weather-dashboard"
    }), 200


# ── Run the app ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)