
from flask import Flask, jsonify, request
from db_connection import get_db_connection, close_db_connection

app = Flask(__name__)

# Route to fetch all medications
@app.route('/medications', methods=['GET'])
def get_medications():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Medications")
        medications = cursor.fetchall()
        return jsonify([dict(row) for row in medications]), 200
    finally:
        close_db_connection(connection)

# Route to add a new medication
@app.route('/medications', methods=['POST'])
def add_medication():
    data = request.get_json()
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO Medications (Name, Description, Dosage, Interactions, Side_Effects)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (data['Name'], data['Description'], data['Dosage'], 
                               data['Interactions'], data['Side_Effects']))
        connection.commit()
        return jsonify({"message": "Medication added successfully"}), 201
    finally:
        close_db_connection(connection)

# Route to fetch symptoms associated with a disease
@app.route('/symptoms/<disease>', methods=['GET'])
def get_symptoms_by_disease(disease):
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = connection.cursor()
        query = """
        SELECT Name FROM Symptoms WHERE Associated_Disease = ?
        """
        cursor.execute(query, (disease,))
        symptoms = cursor.fetchall()
        return jsonify([row['Name'] for row in symptoms]), 200
    finally:
        close_db_connection(connection)

if __name__ == '__main__':
    app.run(debug=True)
