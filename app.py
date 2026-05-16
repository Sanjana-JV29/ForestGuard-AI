from flask import Flask, render_template, request
import joblib
import numpy as np
import requests

app = Flask(__name__)

# =====================================================
# LOAD TRAINED ML MODEL
# =====================================================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "forest_fire_model.pkl")

model = joblib.load(model_path)

# =====================================================
# n8n WEBHOOK URL
# =====================================================

WEBHOOK_URL = "https://sanjanajv.app.n8n.cloud/webhook/fire-alert"


# =====================================================
# HOME PAGE
# =====================================================

# HOME PAGE

@app.route('/')
def home():

    return render_template(

        'index.html',

        prediction_text=None,

        alert_class=None,

        alert_message=None,

        temp=None,

        RH=None,

        wind=None,

        rain=None
    )


# =====================================================
# PREDICTION ROUTE
# =====================================================

@app.route('/predict', methods=['POST'])
def predict():

    try:

        # =====================================================
        # GET INPUT VALUES FROM FORM
        # =====================================================

        temperature = float(request.form['temp'])

        humidity = float(request.form['RH'])

        wind_speed = float(request.form['wind'])

        rainfall = float(request.form['rain'])

        # =====================================================
        # CONVERT INPUTS FOR ML MODEL
        # =====================================================

        features = np.array([[
            temperature,
            humidity,
            wind_speed,
            rainfall
        ]])

        # =====================================================
        # MACHINE LEARNING PREDICTION
        # =====================================================

        prediction = model.predict(features)

        # =====================================================
        # FIRE RISK ANALYSIS LOGIC
        # =====================================================

        if (
            temperature >= 35 and
            humidity <= 20 and
            wind_speed >= 7 and
            rainfall == 0
        ):

            risk = "HIGH"

        elif (
            temperature >= 25 and
            humidity <= 50 and
            wind_speed >= 3
        ):

            risk = "MEDIUM"

        else:

            risk = "LOW"

        # =====================================================
        # ALERT UI STYLING
        # =====================================================

        if risk == "HIGH":

            alert_class = "high"

            prediction_text = "HIGH WILDFIRE RISK DETECTED"

        elif risk == "MEDIUM":

            alert_class = "medium"

            prediction_text = "MODERATE FIRE RISK CONDITIONS"

        else:

            alert_class = "low"

            prediction_text = "ENVIRONMENT CONDITIONS SAFE"

        # =====================================================
        # n8n WEBHOOK INTEGRATION
        # =====================================================

        alert_message = ""

        if risk == "HIGH":

            print("HIGH RISK DETECTED")
            print("Sending webhook to n8n...")

            webhook_payload = {

                "risk": risk,

                "temperature": temperature,

                "humidity": humidity,

                "wind_speed": wind_speed,

                "rainfall": rainfall
            }

            try:

                response = requests.post(
                    WEBHOOK_URL,
                    json=webhook_payload,
                    timeout=10
                )

                print("Webhook Response:", response.status_code)

                print("Webhook Output:", response.text)

                if response.status_code == 200:

                    alert_message = "Emergency Alert Successfully Sent"

                else:

                    alert_message = "Alert System Failed"

            except requests.exceptions.RequestException as webhook_error:

                print("Webhook Error:", webhook_error)

                alert_message = "Alert System Offline"

        else:

            alert_message = ""

        # =====================================================
        # SEND RESULTS TO FRONTEND
        # =====================================================

        return render_template(

            'index.html',

            prediction_text=prediction_text,

            temp=temperature,

            RH=humidity,

            wind=wind_speed,

            rain=rainfall,

            alert_class=alert_class,

            alert_message=alert_message
        )

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        print("Application Error:", error)

        return render_template(

            'index.html',

            prediction_text="SYSTEM ERROR OCCURRED",

            alert_class="medium",

            alert_message="Backend Processing Failed"
        )


# =====================================================
# RUN FLASK APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)