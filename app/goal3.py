from flask import Flask, redirect, render_template, request, jsonify, session, url_for ,flash
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split  
from . import app


# Load the dataset
data = pd.read_csv("dataset/Dataset.csv")

# Drop rows with missing values in the 'Net Ground Water Availability for future use' column
data.dropna(subset=['Net Ground Water Availability for future use'], inplace=True)

# Define the input column
input_column = 'Recharge from rainfall During Monsoon Season'

# Selecting input (X) and output (y) columns after dropping NaN rows
X = data[['Recharge from rainfall During Monsoon Season',
          'Recharge from rainfall During Non Monsoon Season',
          'Total Annual Ground Water Recharge',
          'Total Natural Discharges']]

y = data['Net Ground Water Availability for future use']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the ANN model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, verbose=2)

@app.route('/goal3', methods=['GET', 'POST'])
def goal3():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('goal3.html')
    elif request.method == 'POST':
        input_value = float(request.json['rainfall_monsoon'])
        matched_row = data[data[input_column] == input_value]
        if matched_row.empty:
            return jsonify({'retrievedData': 'No matching row found for the input value.',
                            'prediction': '',
                            'statement': ''})
        else:
            remaining_inputs = matched_row[['Recharge from rainfall During Monsoon Season',
                                            'Recharge from rainfall During Non Monsoon Season',
                                            'Total Annual Ground Water Recharge',
                                            'Total Natural Discharges']].values.flatten()
            remaining_inputs_scaled = scaler.transform([remaining_inputs])
            prediction = model.predict(remaining_inputs_scaled)
            predicted_value = float(prediction[0][0])
            if predicted_value < 0:
                prediction_text = "The predicted Net Ground Water Availability for future use is negative, indicating an alarming shortage."
            elif predicted_value < 50:
                prediction_text = "The predicted Net Ground Water Availability for future use is relatively low, suggesting potential water scarcity."
            else:
                prediction_text = "The predicted Net Ground Water Availability for future use is relatively high, indicating sufficient water availability."

            matched_row_dict = matched_row.to_dict(orient='records')

            return jsonify({'retrievedData': matched_row_dict,
                            'prediction': predicted_value,
                            'statement': prediction_text})


