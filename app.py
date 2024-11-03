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
        # Use OpenAI's API to simulate weather information request
        prompt = f"Provide the current weather in {location}."
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # Ensure the correct model is used
            prompt=prompt,
            max_tokens=50
        )
        weather_info = response.choices[0].text.strip()

        return jsonify({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weather_info": weather_info
        })

    except Exception as e:
        # Provide detailed error messages from the OpenAI API or other failures
        error_message = getattr(e, 'message', repr(e))
        return jsonify({"error": "An internal server error occurred", "details": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
