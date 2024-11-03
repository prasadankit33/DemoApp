from flask import Flask, request, jsonify, render_template
import openai
import os
from datetime import datetime

app = Flask(__name__)

# Set up the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.json
    location = data.get("location")

    if not location:
        return jsonify({"error": "Please provide a location"}), 400

    try:
        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ask OpenAI for weather information in a specific location
        prompt = f"Provide the current weather in {location} along with the date and time. Use plausible weather data."
        response = openai.ChatCompletion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        
        # Extract the generated response
        weather_info = response.choices[0].text.strip()

        # Return the date and weather information
        return jsonify({
            "date": current_date,
            "weather_info": weather_info
        })

    except Exception as e:
        # Log and return any errors
        print(f"Error in /weather endpoint: {str(e)}")
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
