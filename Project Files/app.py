from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# ===============================
# LOAD MODEL
# ===============================
with open("payments.pkl", "rb") as f:
    model = pickle.load(f)

print("Model loaded successfully:", type(model))


# HOME PAGE

@app.route("/")
def home():
    return render_template("home.html")






# SHOW FORM PAGE

@app.route("/predict_page")
def predict_page():
    return render_template("predict.html")



# PREDICTION ROUTE


@app.route("/predict", methods=["POST"])
def predict():


    step = float(request.form["step"])
    type_enc = float(request.form["type"])
    amount = float(request.form["amount"])
    oldbalanceOrg = float(request.form["oldbalanceOrg"])
    newbalanceOrig = float(request.form["newbalanceOrig"])
    oldbalanceDest = float(request.form["oldbalanceDest"])
    newbalanceDest = float(request.form["newbalanceDest"])
    isFlaggedFraud = float(request.form["isFlaggedFraud"])

    sample_df = pd.DataFrame([[step, type_enc, amount,
                               oldbalanceOrg, newbalanceOrig,
                               oldbalanceDest, newbalanceDest,
                               isFlaggedFraud]],
                             columns=['step','type','amount',
                                      'oldbalanceOrg','newbalanceOrig',
                                      'oldbalanceDest','newbalanceDest',
                                      'isFlaggedFraud'])

    prediction = model.predict(sample_df)

    if prediction[0] == 1:
        result = "⚠ Fraudulent Transaction"
    else:
        result = "✅ Legitimate Transaction"

    return render_template("result.html", prediction_text=result)


# ===============================
# PREDICTION LOGIC
# ===============================
# @app.route("/predict", methods=["POST"])
# def predict():

#     step = float(request.form["step"])
#     type_enc = float(request.form["type"])
#     amount = float(request.form["amount"])
#     oldbalanceOrg = float(request.form["oldbalanceOrg"])
#     newbalanceOrig = float(request.form["newbalanceOrig"])
#     oldbalanceDest = float(request.form["oldbalanceDest"])
#     newbalanceDest = float(request.form["newbalanceDest"])
#     isFlaggedFraud = float(request.form["isFlaggedFraud"])

#     sample_df = pd.DataFrame([[ 
#         step, type_enc, amount, oldbalanceOrg,
#         newbalanceOrig, oldbalanceDest,
#         newbalanceDest, isFlaggedFraud
#     ]],
#     columns=[
#         'step','type','amount','oldbalanceOrg',
#         'newbalanceOrig','oldbalanceDest',
#         'newbalanceDest','isFlaggedFraud'
#     ])

#     prediction = model.predict(sample_df)

#     if prediction[0] == 1:
#         result = "⚠ Fraudulent Transaction"
#     else:
#         result = "✅ Legitimate Transaction"

#     return render_template("result.html",
#                            prediction_text=result)


# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
