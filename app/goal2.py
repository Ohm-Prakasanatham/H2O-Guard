from flask import Flask, redirect, render_template, request, jsonify, session, url_for ,flash
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from . import app

# Load the dataset
data = pd.read_csv("dataset/Dataset.csv")

# Drop rows with missing values in the 'Stage of Ground Water Extraction (%)' column
data.dropna(subset=['Stage of Ground Water Extraction (%)'], inplace=True)

@app.route('/goal2', methods=['GET', 'POST'])
def index():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))  # Redirect to the login route

    if request.method == 'GET':
        return render_template('goal2.html')
    elif request.method == 'POST':
        # Load the user input
        Annual_Ground_Water_Recharge = float(request.json['Annual_Ground_Water_Recharge'])
        
        # Find the row in the dataset where the input value matches the 'Total Annual Ground Water Recharge'
        matched_row = data[data['Total Annual Ground Water Recharge'] == Annual_Ground_Water_Recharge]

        if len(matched_row) == 0:
            return jsonify({'retrievedData': 'No matching data found for the input value.', 'prediction': '', 'overview': ''})
        else:
            # Extract the remaining input values from the matched row
            remaining_inputs = matched_row[['Total Natural Discharges',
                                            'Annual Extractable Ground Water Resource',
                                            'Current Annual Ground Water Extraction For Irrigation',
                                            'Current Annual Ground Water Extraction For Domestic & Industrial Use']]

            # Extract the output value from the matched row
            output_value = matched_row['Stage of Ground Water Extraction (%)'].values[0]

            # Scale the remaining input values
            scaler = StandardScaler()
            remaining_inputs_scaled = scaler.fit_transform(remaining_inputs)

            # Build the ANN model
            model = keras.Sequential([
                layers.Dense(64, activation='relu', input_shape=(remaining_inputs_scaled.shape[1],)),
                layers.Dense(64, activation='relu'),
                layers.Dense(1)
            ])

            # Compile the model
            model.compile(optimizer='adam', loss='mean_squared_error')

            # Train the model (for demonstration purpose, we'll use the entire dataset)
            X = remaining_inputs_scaled
            y = np.array([output_value])  # Convert to numpy array
            model.fit(X, y, epochs=100, batch_size=32, verbose=2)

            # Scale the user input
            user_input_scaled = scaler.transform([remaining_inputs.values.flatten()])

            # Predict the output
            prediction = model.predict(user_input_scaled)
            predicted_value = float(prediction[0][0])
            # Overview about the prediction
            if prediction[0][0] < output_value:
                overview = "The predicted Net Ground Water Availability for future use is indicating a potential shortage."
            elif prediction[0][0] > output_value:
                overview = "The predicted Net Ground Water Availability for future use is suggesting a surplus."
            else:
                overview = "The predicted Net Ground Water Availability for future use indicating equilibrium."

            return jsonify({'TotalNaturalDischarges': remaining_inputs['Total Natural Discharges'].values[0],
                            'Annual Extractable Ground Water Resource': remaining_inputs['Annual Extractable Ground Water Resource'].values[0],
                            'Current Annual Ground Water Extraction For Irrigation': remaining_inputs['Current Annual Ground Water Extraction For Irrigation'].values[0],
                            'Current Annual Ground Water Extraction For Domestic & Industrial Use': remaining_inputs['Current Annual Ground Water Extraction For Domestic & Industrial Use'].values[0],
                            'prediction': predicted_value,
                            'overview': overview})



