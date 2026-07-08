from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import traceback

app = FastAPI()

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

class InputData(BaseModel):
    features: list

@app.post("/predict")
def predict(data: InputData):

    try:
        print("STEP 1")

        x = np.array(data.features).reshape(1, -1)

        print("STEP 2")

        x = scaler.transform(x)

        print("STEP 3")

        prediction = model.predict(x)

        print("STEP 4")

        probability = model.predict_proba(x)

        print("STEP 5")

        return {
            "prediction": int(prediction[0]),
            "probability": float(probability.max())
        }

    except Exception:
        traceback.print_exc()
        raise
