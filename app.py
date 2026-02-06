from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Note: In a production environment, use environment variables for API keys
# Empty string as requested for potential environment injection
API_KEY = "49cc2657045897a77135f364263fe308" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')
    if not city:
        return jsonify({"error": "City name is required"}), 400

    # Step 1: Get coordinates for the city (Geocoding)
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    
    try:
        geo_resp = requests.get(geo_url)
        geo_data = geo_resp.json()
        
        if not geo_data:
            return jsonify({"error": "City not found"}), 404
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        city_name = geo_data[0]['name']

        # Step 2: Get detailed weather data using One Call API (or standard if One Call isn't active)
        # Using current weather + forecast for maximum features
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        data = requests.get(weather_url).json()

        # Add logic for clothing and recommendations on the backend
        temp = data['main']['temp']
        condition = data['weather'][0]['main'].lower()
        
        clothing = []
        recommendation = ""
        
        # Clothing Logic
        if temp >= 30:
            clothing.append("Wear light cotton clothes 👕")
            recommendation = "Stay hydrated and avoid direct sun."
        elif 20 <= temp < 30:
            clothing.append("Comfortable casual wear 👖")
            recommendation = "Great weather for outdoor activities!"
        elif 10 <= temp < 20:
            clothing.append("Wear a light jacket 🧥")
            recommendation = "A bit chilly, keep a layer handy."
        else:
            clothing.append("Wear warm clothes and jacket 🧣")
            recommendation = "Freezing temperatures! Bundle up."

        if 'rain' in condition:
            recommendation = "Don't forget to carry an umbrella! ☔"
        elif 'snow' in condition:
            recommendation = "Be careful, roads might be slippery! ❄️"

        # Constructing the final response
        result = {
            "city": city_name,
            "temp": round(temp),
            "feels_like": round(data['main']['feels_like']),
            "humidity": data['main']['humidity'],
            "visibility": data.get('visibility', 0) / 1000, # km
            "wind_speed": data['wind']['speed'],
            "description": data['weather'][0]['description'],
            "main_condition": condition,
            "clothing": clothing,
            "recommendation": recommendation,
            "icon": data['weather'][0]['icon']
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)