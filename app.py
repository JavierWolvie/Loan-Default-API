from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

model = pickle.load(open("loan_default_model.pkl", "rb"))

@app.route("/")
def home():
    return "Loan Default API is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    prediction = model.predict([list(data.values())])
    return jsonify({"prediction": int(prediction[0])})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)