from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set up the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get("prompt")

    try:
        # Update to use ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the model, like "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return jsonify({"generated_text": generated_text})

    except Exception as e:
        print(f"Error in /generate endpoint: {str(e)}")
        return jsonify({"error": "An internal server error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
