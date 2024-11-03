# app.py
from flask import Flask, request, jsonify, render_template
import openai
import os

# Initialize the Flask app
app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for security

@app.route('/')
def index():
    return render_template('index.html')  # Serves the frontend page

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get("prompt")

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    generated_text = response.choices[0].text.strip()
    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    app.run(debug=True)
