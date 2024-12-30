
from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

# Function to fetch treatment recommendations from the database
def get_treatment_recommendation(disease):
    db_path = '/mnt/data/medical_ai_bot.db'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "SELECT Recommended_Treatment FROM Diseases WHERE Name = ?"
    cursor.execute(query, (disease,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else "No recommendation available"

# Function to check for drug interactions
def check_drug_interactions(prescribed_drugs):
    db_path = '/mnt/data/medical_ai_bot.db'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    warnings = []
    for i in range(len(prescribed_drugs)):
        for j in range(i + 1, len(prescribed_drugs)):
            query = '''
                SELECT Interaction_Description FROM Drug_Interactions 
                WHERE (Drug_A = ? AND Drug_B = ?) OR (Drug_A = ? AND Drug_B = ?)
            '''
            cursor.execute(query, (prescribed_drugs[i], prescribed_drugs[j], prescribed_drugs[j], prescribed_drugs[i]))
            result = cursor.fetchone()
            if result:
                warnings.append(result[0])
    connection.close()
    return warnings

# Endpoint to integrate treatment recommendations and drug interaction warnings
@app.route('/bot/extended_diagnose', methods=['POST'])
def extended_bot_diagnose():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    prescribed_drugs = data.get('drugs', [])

    # Predict disease using the API
    prediction_api_url = 'http://127.0.0.1:5000/predict_disease'  # Local API URL
    response = requests.post(prediction_api_url, json={'symptoms': symptoms})

    if response.status_code == 200:
        result = response.json()
        disease = result['Predicted Disease']

        # Get treatment recommendation
        treatment = get_treatment_recommendation(disease)

        # Check for drug interactions
        interaction_warnings = check_drug_interactions(prescribed_drugs)

        return jsonify({
            "Predicted Disease": disease,
            "Treatment Recommendation": treatment,
            "Drug Interaction Warnings": interaction_warnings
        }), 200
    else:
        return jsonify({"error": "Failed to connect to the prediction API"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7000)  # Extended bot runs on a different port
