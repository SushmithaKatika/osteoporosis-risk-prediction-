from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import pickle
import pandas as pd

app = Flask(__name__)

# Load the saved model
with open('osteoporosis_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER, 
                gender INTEGER, 
                calcium_intake REAL, 
                bone_density REAL, 
                risk INTEGER, 
                risk_text TEXT)''')  # Updated to include risk_text

    conn.close()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Prediction form route
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            gender = int(request.form['gender'])
            calcium_intake = float(request.form['calcium_intake'])
            bone_density = float(request.form['bone_density'])

            # Create input DataFrame
            input_data = pd.DataFrame([[age, gender, calcium_intake, bone_density]],
                                      columns=['age', 'gender', 'calcium_intake', 'bone_density'])

            # Make prediction
            prediction = model.predict(input_data)[0]
            risk_text = 'High Risk' if prediction == 1 else 'Low Risk'  # Convert to readable label

            # Store result in database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO predictions 
                          (age, gender, calcium_intake, bone_density, risk, risk_text) 
                          VALUES (?, ?, ?, ?, ?, ?)""", 
                       (age, gender, calcium_intake, bone_density, prediction, risk_text))
            conn.commit()
            conn.close()

            return jsonify({'prediction': risk_text})
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('predict.html')

# Route to display predictions
@app.route('/show_predictions')
def show_predictions():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM predictions")
        rows = cursor.fetchall()
        conn.close()

        return render_template('show_predictions.html', rows=rows)
    except Exception as e:
        return str(e)

# Run Flask app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
