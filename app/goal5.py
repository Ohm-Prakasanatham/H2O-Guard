from flask import Flask, redirect, render_template, request, jsonify, session, url_for ,flash
import pandas as pd
from .import app

# Load the dataset
dataset = pd.read_csv("dataset/Dataset.csv")

# Define a function to recommend irrigation type based on extraction-recharge ratio
def recommend_irrigation_type(state, district):
    # Calculate the ratio of groundwater extraction for irrigation to total annual groundwater recharge
    extraction_recharge_ratio = dataset.loc[(dataset['Name of State'] == state) & (dataset['Name of District'] == district), 'Current Annual Ground Water Extraction For Irrigation'].values[0] / dataset.loc[(dataset['Name of State'] == state) & (dataset['Name of District'] == district), 'Total Annual Ground Water Recharge'].values[0]

    irrigation_types_overview = {
        "High-Efficiency Micro Irrigation (Drip or Sprinkler)": {
            "Benefits": "This type of irrigation is recommended in areas where the extraction-recharge ratio is very low, indicating limited groundwater availability relative to irrigation needs.",
            "Advantages": "Provides precise water delivery directly to the roots of plants, minimizing water wastage and maximizing efficiency."
        },
        "Drip Irrigation": {
            "Benefits": "Recommended when the extraction-recharge ratio is relatively low, suggesting moderate groundwater availability compared to irrigation demand.",
            "Advantages": "Delivers water directly to the root zone of plants, reducing water use and promoting water conservation."
        },
        "Sprinkler Irrigation": {
            "Benefits": "Suitable for regions with moderate extraction-recharge ratios, indicating sufficient groundwater availability for irrigation purposes.",
            "Advantages": "Sprinklers distribute water over the soil surface, simulating natural rainfall and providing uniform coverage to the entire area."
        },
        "Center Pivot Irrigation": {
            "Benefits": "Recommended in areas with higher extraction-recharge ratios, where groundwater availability is relatively high compared to irrigation requirements.",
            "Advantages": "Uses rotating sprinklers mounted on wheeled towers to irrigate large circular areas efficiently, ideal for crops such as grains and vegetables."
        },
        "Surface Irrigation": {
            "Benefits": "Appropriate for regions with higher extraction-recharge ratios, indicating abundant groundwater resources relative to irrigation demands.",
            "Advantages": "Involves flooding or furrowing the field with water, allowing it to flow over the soil surface and infiltrate into the root zone of crops."
        },
        "Furrow Irrigation": {
            "Benefits": "Recommended when the extraction-recharge ratio is very high, suggesting ample groundwater availability compared to irrigation needs.",
            "Advantages": "Involves creating small channels or furrows along the crop rows and filling them with water, allowing for efficient water distribution to the root zone."
        },
        "Flood Irrigation": {
            "Benefits": "Used when groundwater availability is extremely high relative to irrigation demands, as indicated by a very high extraction-recharge ratio.",
            "Advantages": "Involves flooding the entire field with water, often used in rice paddies or forage crops, but can result in water wastage if not managed properly."
        }
    }

    if extraction_recharge_ratio < 0.05:
        irrigation_type = "High-Efficiency Micro Irrigation (Drip or Sprinkler)"
    elif extraction_recharge_ratio < 0.2:
        irrigation_type = "Drip Irrigation"
    elif extraction_recharge_ratio < 0.4:
        irrigation_type = "Sprinkler Irrigation"
    elif extraction_recharge_ratio < 0.6:
        irrigation_type = "Center Pivot Irrigation"
    elif extraction_recharge_ratio < 0.8:
        irrigation_type = "Surface Irrigation"
    elif extraction_recharge_ratio < 0.9:
        irrigation_type = "Furrow Irrigation"
    else:
        irrigation_type = "Flood Irrigation"

    benefits = irrigation_types_overview[irrigation_type]["Benefits"]
    advantages = irrigation_types_overview[irrigation_type]["Advantages"]

    return {
        "Irrigation Type": irrigation_type,
        "Benefits": benefits,
        "Advantages": advantages
    }

@app.route('/goal5', methods=['GET', 'POST'])
def goal5():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('goal5.html')
    elif request.method == 'POST':
        data = request.json
        state = data['state']
        district = data['district']
        recommendation = recommend_irrigation_type(state, district)
        return jsonify(recommendation)


