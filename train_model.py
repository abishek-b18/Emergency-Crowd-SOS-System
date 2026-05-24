import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


os.makedirs(
    "models",
    exist_ok=True
)


df = pd.read_excel(
    "datasets/emergency_data.xlsx"
)


encoder = LabelEncoder()

df["incident_type"] = encoder.fit_transform(
    df["incident_type"]
)

df["weather"] = encoder.fit_transform(
    df["weather"]
)

df["time_of_day"] = encoder.fit_transform(
    df["time_of_day"]
)

df["severity"] = encoder.fit_transform(
    df["severity"]
)



X = df[
[
"incident_type",
"user_age",
"response_time(min)",
"nearby_responders"
]
]


y = df["severity"]


model = RandomForestClassifier()

model.fit(
    X,
    y
)


joblib.dump(

model,

"models/emergency_model.pkl"

)


print(

"Emergency AI Model Saved"

)