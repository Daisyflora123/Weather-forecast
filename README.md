WeatherPro Dashboard

WeatherPro is a modern, responsive weather application featuring dynamic environmental effects, smart health recommendations, and real-time air quality tracking. The interface adapts visually to current weather conditions, providing an immersive experience while delivering critical meteorological data.

🌟 Key Features

1. Dynamic Environmental Themes

The dashboard's appearance changes based on the actual weather in the searched city:

Clear Skies: Bright blue gradients with high-contrast text.

Rain/Drizzle: Darker slate tones with an animated CSS rain-drop overlay.

Snow: Soft white and light grey themes for high readability in "winter" modes.

Thunderstorm: Deep navy themes with a triggered "flash" animation to simulate lightning.

Clouds: Neutral grey-blue professional interface.

2. Smart Recommendations

Clothing Advice: Automatically suggests appropriate attire based on the current temperature (e.g., suggesting cotton for 30°C+ or thermal layers for sub-5°C).

Air Quality Guidance: Provides actionable health tips based on the AQI (Air Quality Index) level, ranging from "Perfect for outdoor activities" to "Hazardous - Stay indoors."

3. Comprehensive Weather Data

Real-time Metrics: Temperature, "Feels Like" conditions, pressure, and UV index.

Hourly Forecast: A horizontally scrollable list of conditions for the next 24 hours.

5-Day Outlook: A summarized daily forecast for long-term planning.

Solar Times: Dedicated cards for Sunrise and Sunset with distinct iconography.

Lifestyle Tips: Contextual suggestions for daily activities based on the overall forecast.

🚀 Tech Stack

Frontend: HTML5, Tailwind CSS, Font Awesome icons.

Animations: Custom CSS Keyframes and JavaScript-driven SVG/DOM injection.

Backend: Python/Flask (expected).

API Integration: OpenWeatherMap (Current, Forecast, and Air Pollution APIs).

🛠️ Installation & Setup

Clone the repository:

git clone [https://github.com/your-username/weatherpro-dashboard.git](https://github.com/your-username/weatherpro-dashboard.git)
cd weatherpro-dashboard


Backend Setup:
Ensure you have a Flask server (or similar) set up to handle the /get_weather POST request. The backend should return a JSON object structured with current, aqi, hourly, daily, and tips keys.

API Key:
Configure your OpenWeatherMap API key in your backend environment variables.

Run the application:

python app.py


Access the dashboard at http://localhost:5000.

📂 Project Structure

app.py: Backend logic and API handling.

templates/index.html: The core UI, styling, and dynamic rendering logic.
