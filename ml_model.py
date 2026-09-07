import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import mysql.connector

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="crop_recommendation_system"
    )


# =========================================================
# LOAD TRAINING DATA
# =========================================================

def load_training_data():

    connection = None

    try:

        connection = get_connection()

        query = """
        SELECT
            s.pH,
            s.Soil_Type,
            w.Temperature,
            w.Rainfall,
            c.Crop_Name

        FROM Recommendation r

        JOIN Soil s
            ON r.SoilID = s.SoilID

        JOIN Weather w
            ON r.WeatherID = w.WeatherID

        JOIN Crop c
            ON r.CropID = c.CropID
        """

        data = pd.read_sql(query, connection)

        return data

    except Exception as e:

        print("Database Error:", e)

        return pd.DataFrame()

    finally:

        if connection is not None:
            connection.close()


# =========================================================
# TRAIN MODEL
# =========================================================

def train_model():

    print("\n==========================================")
    print("       CROP RECOMMENDATION ML MODEL")
    print("==========================================")

    # -----------------------------------------------------
    # GET DATA
    # -----------------------------------------------------

    data = load_training_data()

    if data.empty:

        print("\nNo training data found.")

        return None, None, None, None, 0


    print("\nTraining Data:")
    print(data)


    # -----------------------------------------------------
    # REMOVE EMPTY VALUES
    # -----------------------------------------------------

    data = data.dropna()

    if data.empty:

        print("\nTraining data contains no valid records.")

        return None, None, None, None, 0


    # -----------------------------------------------------
    # CHECK NUMBER OF RECORDS
    # -----------------------------------------------------

    if len(data) < 5:

        print("\nNot enough data for proper ML training.")
        print("Minimum recommended records: 5")
        print("Current records:", len(data))

        return None, None, None, None, 0


    # -----------------------------------------------------
    # CHECK CROP CLASSES
    # -----------------------------------------------------

    if data["Crop_Name"].nunique() < 2:

        print("\nML model needs at least 2 different crops.")

        return None, None, None, None, 0


    # -----------------------------------------------------
    # SOIL TYPE ENCODER
    # -----------------------------------------------------

    soil_encoder = LabelEncoder()

    data["Soil_Type"] = soil_encoder.fit_transform(
        data["Soil_Type"].astype(str)
    )


    # -----------------------------------------------------
    # CROP ENCODER
    # -----------------------------------------------------

    crop_encoder = LabelEncoder()

    data["Crop_Name"] = crop_encoder.fit_transform(
        data["Crop_Name"].astype(str)
    )


    # -----------------------------------------------------
    # INPUT FEATURES
    # -----------------------------------------------------

    X = data[
        [
            "pH",
            "Soil_Type",
            "Temperature",
            "Rainfall"
        ]
    ]


    # -----------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------

    y = data["Crop_Name"]


    # -----------------------------------------------------
    # TRAIN TEST SPLIT
    # -----------------------------------------------------

    # If dataset is very small, use all data for training
    # instead of creating an unreliable test set.

    if len(data) >= 10:

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

    else:

        X_train = X
        y_train = y

        X_test = X
        y_test = y


    # -----------------------------------------------------
    # RANDOM FOREST
    # -----------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )


    # -----------------------------------------------------
    # TRAIN
    # -----------------------------------------------------

    try:

        model.fit(X_train, y_train)

    except Exception as e:

        print("\nModel Training Error:", e)

        return None, None, None, None, 0


    # -----------------------------------------------------
    # ACCURACY
    # -----------------------------------------------------

    try:

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            y_pred
        )

        accuracy = round(
            accuracy * 100,
            2
        )

    except Exception:

        accuracy = 0


    print("\n==========================================")
    print("MODEL TRAINING COMPLETED")
    print("Model Accuracy:", accuracy, "%")
    print("==========================================")


    return (
        model,
        soil_encoder,
        crop_encoder,
        data,
        accuracy
    )


# =========================================================
# TRAIN MODEL
# =========================================================

model = None
soil_encoder = None
crop_encoder = None
training_data = None
model_accuracy = 0


def initialize_model():

    global model
    global soil_encoder
    global crop_encoder
    global training_data
    global model_accuracy

    (
        model,
        soil_encoder,
        crop_encoder,
        training_data,
        model_accuracy
    ) = train_model()


# =========================================================
# RECOMMEND CROP
# =========================================================

def recommend_crop(
    pH,
    soil_type,
    temperature,
    rainfall
):

    global model
    global soil_encoder
    global crop_encoder


    # -----------------------------------------------------
    # CHECK MODEL
    # -----------------------------------------------------

    if model is None:

        raise Exception(
            "ML model is not trained yet. "
            "Please add at least 5 recommendation records "
            "with at least 2 different crops."
        )


    # -----------------------------------------------------
    # CLEAN SOIL TYPE
    # -----------------------------------------------------

    soil_type = str(soil_type).strip()


    # -----------------------------------------------------
    # CHECK SOIL TYPE
    # -----------------------------------------------------

    if soil_type not in soil_encoder.classes_:

        available_soils = ", ".join(
            soil_encoder.classes_
        )

        raise Exception(
            "Unknown soil type: "
            + soil_type
            + "\nAvailable soil types: "
            + available_soils
        )


    # -----------------------------------------------------
    # ENCODE SOIL TYPE
    # -----------------------------------------------------

    soil_type_encoded = soil_encoder.transform(
        [soil_type]
    )[0]


    # -----------------------------------------------------
    # CREATE INPUT DATAFRAME
    # -----------------------------------------------------

    input_data = pd.DataFrame(
        [[
            float(pH),
            soil_type_encoded,
            float(temperature),
            float(rainfall)
        ]],

        columns=[
            "pH",
            "Soil_Type",
            "Temperature",
            "Rainfall"
        ]
    )


    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    prediction = model.predict(
        input_data
    )


    # -----------------------------------------------------
    # CONVERT CROP NUMBER TO CROP NAME
    # -----------------------------------------------------

    crop = crop_encoder.inverse_transform(
        prediction
    )[0]


    return crop


# =========================================================
# GET MODEL ACCURACY
# =========================================================

def get_model_accuracy():

    return model_accuracy


# =========================================================
# GET AVAILABLE SOIL TYPES
# =========================================================

def get_soil_types():

    global soil_encoder

    if soil_encoder is None:

        return []

    return list(
        soil_encoder.classes_
    )


# =========================================================
# GET AVAILABLE CROPS
# =========================================================

def get_available_crops():

    global crop_encoder

    if crop_encoder is None:

        return []

    return list(
        crop_encoder.classes_
    )


# =========================================================
# INITIALIZE MODEL
# =========================================================

initialize_model()
