
from flask import Flask, jsonify, request
from db_connection import get_db_connection, close_db_connection

app = Flask(__name__)

# Route to fetch all patients
@app.route('/patients', methods=['GET'])
def get_patients():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Patients")
        patients = cursor.fetchall()
        return jsonify([dict(row) for row in patients]), 200
    finally:
        close_db_connection(connection)

# Route to add a new patient
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO Patients (Name, Date_of_Birth, Gender, Contact_Info)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (data['Name'], data['Date_of_Birth'], data['Gender'], data['Contact_Info']))
        connection.commit()
        return jsonify({"message": "Patient added successfully"}), 201
    finally:
        close_db_connection(connection)

if __name__ == '__main__':
    app.run(debug=True)
