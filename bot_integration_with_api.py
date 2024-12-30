
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Endpoint to simulate the bot receiving symptoms and sending them to the prediction API
@app.route('/bot/diagnose', methods=['POST'])
def bot_diagnose():
    data = request.get_json()
    symptoms = data.get('symptoms', [])

    # Send symptoms to the prediction API
    prediction_api_url = 'http://127.0.0.1:5000/predict_disease'  # Local API URL
    response = requests.post(prediction_api_url, json={'symptoms': symptoms})
    
    if response.status_code == 200:
        result = response.json()
        return jsonify({"Bot Response": f"The predicted disease is: {result['Predicted Disease']}"}), 200
    else:
        return jsonify({"error": "Failed to connect to the prediction API"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=6000)  # Bot runs on a different port
