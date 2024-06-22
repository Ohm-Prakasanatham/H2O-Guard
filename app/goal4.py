from flask import Flask, redirect, render_template, request, jsonify, session, url_for ,flash
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from . import app

# Load the dataset
data = pd.read_csv("dataset/Dataset.csv")

# Remove rows with missing values in the 'Annual GW Allocation for Domestic Use as on 2025' column
data.dropna(subset=['Annual GW Allocation for Domestic Use as on 2025'], inplace=True)

# Select features (X) and target (y)
X = data[['Total Annual Ground Water Recharge',
          'Annual Extractable Ground Water Resource',
          'Current Annual Ground Water Extraction For Irrigation',
          'Current Annual Ground Water Extraction For Domestic & Industrial Use']]
y = data['Annual GW Allocation for Domestic Use as on 2025']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Build and train the model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_scaled.shape[1],)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)])

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_scaled, y, epochs=100, batch_size=32, verbose=2)

@app.route('/goal4', methods=['GET', 'POST'])
def goal4():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('goal4.html')
    elif request.method == 'POST':
        Total_Annual_Ground_Water_Recharge = float(request.json['total_annual_ground_water_recharge'])
        matching_row = data[data['Total Annual Ground Water Recharge'] == Total_Annual_Ground_Water_Recharge]
        if matching_row.empty:
            return jsonify({'retrievedData': 'No matching row found for the input value.',
                            'prediction': '',
                            'statement': ''})
        else:
            Annual_Extractable_Ground_Water_Resource = matching_row['Annual Extractable Ground Water Resource'].values[0]
            Current_Annual_Ground_Water_Extraction_For_Irrigation = matching_row['Current Annual Ground Water Extraction For Irrigation'].values[0]
            Current_Annual_Ground_Water_Extraction_For_Domestic_And_Industrial_Use = matching_row['Current Annual Ground Water Extraction For Domestic & Industrial Use'].values[0]

            user_input_dict = {
                'Total Annual Ground Water Recharge': Total_Annual_Ground_Water_Recharge,
                'Annual Extractable Ground Water Resource': Annual_Extractable_Ground_Water_Resource,
                'Current Annual Ground Water Extraction For Irrigation': Current_Annual_Ground_Water_Extraction_For_Irrigation,
                'Current Annual Ground Water Extraction For Domestic & Industrial Use': Current_Annual_Ground_Water_Extraction_For_Domestic_And_Industrial_Use
            }

            user_input_df = pd.DataFrame(user_input_dict, index=[0])
            user_input_scaled = scaler.transform(user_input_df)

            prediction = model.predict(user_input_scaled)
            if prediction[0][0] > 0:
                prediction_text ="This predicted value suggests a positive trend in the annual groundwater allocation for domestic use."
            else:
                prediction_text ="This predicted value indicates a potential decline in the annual groundwater allocation for domestic use."

            matched_row_dict = matching_row.to_dict(orient='records')
            predicted_value = float(prediction[0][0])
            return jsonify({'retrievedData': matched_row_dict,
                            'prediction': predicted_value,
                            'statement': prediction_text})
