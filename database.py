import mysql.connector
from mysql.connector import Error


# ==========================================
# DATABASE CONNECTION
# ==========================================

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123"
    )

    cursor = connection.cursor()

    # Create Database
    cursor.execute("CREATE DATABASE IF NOT EXISTS crop_recommendation_system")

    print("Database created successfully!")


    # Use Database
    cursor.execute("USE crop_recommendation_system")


    # ==========================================
    # FARMER TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Farmer (
            FarmerID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(100) NOT NULL
        )
    """)

    print("Farmer table created!")


    # ==========================================
    # SOIL TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Soil (
            SoilID INT AUTO_INCREMENT PRIMARY KEY,
            pH DECIMAL(4,2) NOT NULL,
            Soil_Type VARCHAR(50) NOT NULL
        )
    """)

    print("Soil table created!")


    # ==========================================
    # WEATHER TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Weather (
            WeatherID INT AUTO_INCREMENT PRIMARY KEY,
            Temperature DECIMAL(5,2) NOT NULL,
            Rainfall DECIMAL(7,2) NOT NULL
        )
    """)

    print("Weather table created!")


    # ==========================================
    # CROP TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Crop (
            CropID INT AUTO_INCREMENT PRIMARY KEY,
            Crop_Name VARCHAR(100) NOT NULL
        )
    """)

    print("Crop table created!")


    # ==========================================
    # RECOMMENDATION TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Recommendation (
            RecommendationID INT AUTO_INCREMENT PRIMARY KEY,

            FarmerID INT NOT NULL,
            SoilID INT NOT NULL,
            WeatherID INT NOT NULL,
            CropID INT NOT NULL,

            FOREIGN KEY (FarmerID)
                REFERENCES Farmer(FarmerID),

            FOREIGN KEY (SoilID)
                REFERENCES Soil(SoilID),

            FOREIGN KEY (WeatherID)
                REFERENCES Weather(WeatherID),

            FOREIGN KEY (CropID)
                REFERENCES Crop(CropID)
        )
    """)

    print("Recommendation table created!")


    connection.commit()

    print("--------------------------------")
    print("ALL TABLES CREATED SUCCESSFULLY!")
    print("--------------------------------")


except Error as e:
    print("Error:", e)


finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
