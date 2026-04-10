from flask import Flask, render_template, request
import numpy as np
import joblib
import os

# Initialize Flask app
app = Flask(__name__)

# -------------------------------
# Load Model
# -------------------------------
try:
    model_path = os.path.join("model", "loan_default_model.pkl")
    model = joblib.load(model_path)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


# -------------------------------
# Home Route
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Prediction Route
# -------------------------------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None
    probability = None

    if request.method == "POST":
        if model is None:
            prediction = "Model not loaded. Check your model file."
            return render_template("predict.html", prediction=prediction)

        try:
            # -------------------------------
            # Get User Input
            # -------------------------------
            income = float(request.form.get("income"))
            loan_amount = float(request.form.get("loan_amount"))
            credit_score = float(request.form.get("credit_score"))
            age = float(request.form.get("age"))

            # -------------------------------
            # Prepare Features
            # ⚠️ Must match training order
            # -------------------------------
            features = np.array([[income, loan_amount, credit_score, age]])

            # -------------------------------
            # Make Prediction
            # -------------------------------
            prob = model.predict_proba(features)[0][1]

            # -------------------------------
            # Apply Threshold
            # -------------------------------
            threshold = 0.5  # 🔁 Change based on your model tuning

            if prob > threshold:
                prediction = "⚠️ High Risk: Likely to Default"
            else:
                prediction = "✅ Low Risk: Safe Applicant"

            probability = round(prob, 2)

        except ValueError:
            prediction = "⚠️ Invalid input. Please enter valid numbers."
        except Exception as e:
            prediction = f"❌ Error: {str(e)}"

    return render_template(
        "predict.html",
        prediction=prediction,
        probability=probability
    )


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)