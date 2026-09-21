
import pandas as pd
import pickle
from flask import Flask, request, render_template

app = Flask(__name__)

with open("model/churn_model.pkl", "rb") as file:
    saved = pickle.load(file)

model     = saved["model"]
scaler    = saved["scaler"]
encoder   = saved["encoder"]
gendermap = saved["gendermap"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    Age              = float(request.form["Age"])
    Gender           = request.form["Gender"]
    Tenure           = float(request.form["Tenure"])
    Usage_Frequency  = float(request.form["Usage_Frequency"])
    Support_Calls    = float(request.form["Support_Calls"])
    Payment_Delay    = float(request.form["Payment_Delay"])
    Subscription_Type = request.form["Subscription_Type"]
    Contract_Length  = request.form["Contract_Length"]
    Total_Spend      = float(request.form["Total_Spend"])
    Last_Interaction = float(request.form["Last_Interaction"])

    df = pd.DataFrame([[
        Age, Gender, Tenure, Usage_Frequency, Support_Calls,
        Payment_Delay, Subscription_Type, Contract_Length,
        Total_Spend, Last_Interaction
    ]], columns=[
        "Age", "Gender", "Tenure", "Usage Frequency", "Support Calls",
        "Payment Delay", "Subscription Type", "Contract Length",
        "Total Spend", "Last Interaction"
    ])

    df["Gender"] = df["Gender"].map(gendermap)

    cat_cols = list(encoder.feature_names_in_)
    encoded_data = encoder.transform(df[cat_cols])
    encoded_cols = encoder.get_feature_names_out(cat_cols)

    for i, col in enumerate(encoded_cols):
        df[col] = encoded_data[:, i]

    df = df.drop(columns=cat_cols)
    df = df[list(scaler.feature_names_in_)]

    scaled_data = scaler.transform(df)
    prediction  = model.predict(scaled_data)[0]

    if prediction == 1:
        prediction_text = "Customer is likely to churn"
    else:
        prediction_text = "Customer is not likely to churn"

    return render_template("index.html", prediction=prediction_text)


if __name__ == "__main__":
    app.run(debug=True)
