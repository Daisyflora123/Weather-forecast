from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Replace with your actual OpenWeatherMap API Key
API_KEY = "49cc2657045897a77135f364263fe308" 

def get_lifestyle_tips(data, aqi):
    temp = data['main']['temp']
    condition = data['weather'][0]['main'].lower()
    humidity = data['main']['humidity']
    
    tips = []
    # Temperature based
    if temp > 32:
        tips.append("Stay hydrated! Drink at least 3L of water today 🥤")
    elif temp < 15:
        tips.append("Keep yourself warm with hot beverages ☕")
    
    # Air Quality based
    if aqi >= 4:
        tips.append("Air quality is poor. Wear a mask outdoors 😷")
    
    # Humidity/Rain based
    if 'rain' in condition:
        tips.append("High humidity. Use antifungal powder if needed 🧴")
    elif humidity < 30:
        tips.append("Air is dry. Use a good moisturizer 🧴")
        
    if 'clear' in condition:
        tips.append("Perfect for outdoor exercise or a park visit 🏃‍♂️")
        
    return tips

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.json.get('city', 'Mumbai') # Default to Mumbai
    
    try:
        # 1. Geocoding
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        geo_data = requests.get(geo_url).json()
        if not geo_data: return jsonify({"error": "City not found"}), 404
        
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        city_full_name = f"{geo_data[0]['name']}, {geo_data[0].get('country', '')}"

        # 2. Current Weather
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        curr = requests.get(current_url).json()

        # 3. Forecast (5 Days / 3 Hours)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        fore = requests.get(forecast_url).json()

        # 4. Air Quality
        air_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        air = requests.get(air_url).json()

        # Process Forecasts
        hourly = []
        for item in fore['list'][:8]: # Next 24 hours (3-hour steps)
            hourly.append({
                "time": datetime.fromtimestamp(item['dt']).strftime('%I %p'),
                "temp": round(item['main']['temp']),
                "icon": item['weather'][0]['icon']
            })

        daily = []
        # Extract one forecast per day (approx noon)
        for i in range(0, len(fore['list']), 8):
            item = fore['list'][i]
            daily.append({
                "day": datetime.fromtimestamp(item['dt']).strftime('%a'),
                "temp": round(item['main']['temp']),
                "desc": item['weather'][0]['main'],
                "icon": item['weather'][0]['icon']
            })

        aqi_val = air['list'][0]['main']['aqi']
        aqi_label = ["Good", "Fair", "Moderate", "Poor", "Very Poor"][aqi_val-1]

        result = {
            "city": city_full_name,
            "current": {
                "temp": round(curr['main']['temp']),
                "feels_like": round(curr['main']['feels_like']),
                "humidity": curr['main']['humidity'],
                "pressure": curr['main']['pressure'],
                "wind": curr['wind']['speed'],
                "desc": curr['weather'][0]['description'],
                "main": curr['weather'][0]['main'],
                "icon": curr['weather'][0]['icon'],
                "sunrise": datetime.fromtimestamp(curr['sys']['sunrise']).strftime('%I:%M %p'),
                "sunset": datetime.fromtimestamp(curr['sys']['sunset']).strftime('%I:%M %p'),
            },
            "aqi": {"val": aqi_val, "label": aqi_label},
            "hourly": hourly,
            "daily": daily,
            "tips": get_lifestyle_tips(curr, aqi_val)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
