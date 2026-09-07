import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

from ml_model import recommend_crop, get_model_accuracy


# =========================================================
# MYSQL CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="crop_recommendation_system"
    )


# =========================================================
# OPEN RECOMMENDATION WINDOW
# =========================================================

def open_recommendation():

    win = tk.Toplevel()
    win.title("Crop Recommendation")
    win.geometry("950x700")
    win.configure(bg="#f4f7f5")
    win.resizable(False, False)

    # =====================================================
    # HEADER
    # =====================================================

    header = tk.Frame(
        win,
        bg="#198754",
        height=85
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="🌱 CROP RECOMMENDATION",
        font=("Arial", 22, "bold"),
        bg="#198754",
        fg="white"
    ).pack(pady=(18, 2))

    tk.Label(
        header,
        text="AI-powered crop recommendation based on soil and weather",
        font=("Arial", 10),
        bg="#198754",
        fg="white"
    ).pack()


    # =====================================================
    # MAIN CONTAINER
    # =====================================================

    main = tk.Frame(
        win,
        bg="#f4f7f5"
    )
    main.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=25
    )


    # =====================================================
    # INPUT CARD
    # =====================================================

    input_card = tk.LabelFrame(
        main,
        text="  Recommendation Details  ",
        font=("Arial", 13, "bold"),
        bg="white",
        fg="#198754",
        bd=1,
        relief="solid",
        padx=25,
        pady=20
    )

    input_card.pack(
        fill="x"
    )


    # =====================================================
    # VARIABLES
    # =====================================================

    farmer_var = tk.StringVar()
    soil_var = tk.StringVar()
    weather_var = tk.StringVar()


    # =====================================================
    # FARMER
    # =====================================================

    tk.Label(
        input_card,
        text="Select Farmer",
        font=("Arial", 11, "bold"),
        bg="white"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    farmer_combo = ttk.Combobox(
        input_card,
        textvariable=farmer_var,
        width=38,
        state="readonly",
        font=("Arial", 11)
    )

    farmer_combo.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )


    # =====================================================
    # SOIL
    # =====================================================

    tk.Label(
        input_card,
        text="Select Soil",
        font=("Arial", 11, "bold"),
        bg="white"
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    soil_combo = ttk.Combobox(
        input_card,
        textvariable=soil_var,
        width=38,
        state="readonly",
        font=("Arial", 11)
    )

    soil_combo.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )


    # =====================================================
    # WEATHER
    # =====================================================

    tk.Label(
        input_card,
        text="Select Weather",
        font=("Arial", 11, "bold"),
        bg="white"
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=10,
        pady=10
    )

    weather_combo = ttk.Combobox(
        input_card,
        textvariable=weather_var,
        width=38,
        state="readonly",
        font=("Arial", 11)
    )

    weather_combo.grid(
        row=2,
        column=1,
        padx=10,
        pady=10
    )


    # =====================================================
    # RESULT CARD
    # =====================================================

    result_card = tk.Frame(
        main,
        bg="#e9f7ef",
        bd=1,
        relief="solid"
    )

    result_card.pack(
        fill="x",
        pady=20
    )


    tk.Label(
        result_card,
        text="Recommended Crop",
        font=("Arial", 12, "bold"),
        bg="#e9f7ef",
        fg="#198754"
    ).pack(
        pady=(15, 2)
    )


    result_label = tk.Label(
        result_card,
        text="---",
        font=("Arial", 24, "bold"),
        bg="#e9f7ef",
        fg="#14532d"
    )

    result_label.pack(
        pady=(0, 15)
    )


    # =====================================================
    # MODEL ACCURACY
    # =====================================================

    accuracy_label = tk.Label(
        main,
        text="Model Accuracy: --",
        font=("Arial", 10, "bold"),
        bg="#f4f7f5",
        fg="#555555"
    )

    accuracy_label.pack(
        pady=(0, 10)
    )


    try:

        accuracy = get_model_accuracy()

        if accuracy > 0:

            accuracy_label.config(
                text=f"Model Accuracy: {accuracy}%"
            )

    except Exception:

        pass


    # =====================================================
    # LOAD DATABASE DATA
    # =====================================================

    farmer_data = []
    soil_data = []
    weather_data = []


    def load_data():

        nonlocal farmer_data
        nonlocal soil_data
        nonlocal weather_data

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()


            # -------------------------------------------------
            # FARMERS
            # -------------------------------------------------

            cursor.execute("""
                SELECT FarmerID, Name
                FROM Farmer
                ORDER BY FarmerID
            """)

            farmer_data = cursor.fetchall()

            farmer_combo["values"] = [
                f"{row[0]} - {row[1]}"
                for row in farmer_data
            ]


            # -------------------------------------------------
            # SOIL
            # -------------------------------------------------

            cursor.execute("""
                SELECT SoilID, pH, Soil_Type
                FROM Soil
                ORDER BY SoilID
            """)

            soil_data = cursor.fetchall()

            soil_combo["values"] = [
                f"{row[0]} - pH: {row[1]} - {row[2]}"
                for row in soil_data
            ]


            # -------------------------------------------------
            # WEATHER
            # -------------------------------------------------

            cursor.execute("""
                SELECT WeatherID, Temperature, Rainfall
                FROM Weather
                ORDER BY WeatherID
            """)

            weather_data = cursor.fetchall()

            weather_combo["values"] = [
                f"{row[0]} - Temp: {row[1]}°C - Rain: {row[2]} mm"
                for row in weather_data
            ]


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=win
            )

        finally:

            if connection:
                connection.close()


    # =====================================================
    # RECOMMEND CROP
    # =====================================================

    def recommend():

        if not farmer_var.get():

            messagebox.showwarning(
                "Missing Information",
                "Please select a farmer.",
                parent=win
            )
            return


        if not soil_var.get():

            messagebox.showwarning(
                "Missing Information",
                "Please select soil information.",
                parent=win
            )
            return


        if not weather_var.get():

            messagebox.showwarning(
                "Missing Information",
                "Please select weather information.",
                parent=win
            )
            return


        try:

            # -------------------------------------------------
            # GET SELECTED INDEX
            # -------------------------------------------------

            farmer_index = farmer_combo.current()
            soil_index = soil_combo.current()
            weather_index = weather_combo.current()


            # -------------------------------------------------
            # DATABASE VALUES
            # -------------------------------------------------

            farmer_id = farmer_data[farmer_index][0]

            soil_id = soil_data[soil_index][0]
            ph = float(soil_data[soil_index][1])
            soil_type = str(soil_data[soil_index][2]).strip()

            weather_id = weather_data[weather_index][0]
            temperature = float(
                weather_data[weather_index][1]
            )
            rainfall = float(
                weather_data[weather_index][2]
            )


            # -------------------------------------------------
            # ML PREDICTION
            # -------------------------------------------------

            crop_name = recommend_crop(
                ph,
                soil_type,
                temperature,
                rainfall
            )


            # -------------------------------------------------
            # FIND CROP ID
            # -------------------------------------------------

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT CropID
                FROM Crop
                WHERE LOWER(TRIM(Crop_Name))
                = LOWER(TRIM(%s))
                LIMIT 1
            """, (crop_name,))

            crop_result = cursor.fetchone()


            if not crop_result:

                connection.close()

                messagebox.showerror(
                    "Crop Not Found",
                    f"Recommended crop '{crop_name}' "
                    "is not available in the Crop table.\n\n"
                    "Please add this crop first.",
                    parent=win
                )

                return


            crop_id = crop_result[0]


            # -------------------------------------------------
            # SAVE RECOMMENDATION
            # -------------------------------------------------

            cursor.execute("""
                INSERT INTO Recommendation
                (
                    FarmerID,
                    SoilID,
                    WeatherID,
                    CropID
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                farmer_id,
                soil_id,
                weather_id,
                crop_id
            ))


            connection.commit()
            connection.close()


            # -------------------------------------------------
            # SHOW RESULT
            # -------------------------------------------------

            result_label.config(
                text=f"🌾 {crop_name}"
            )


            messagebox.showinfo(
                "Recommendation Successful",
                f"Recommended Crop: {crop_name}\n\n"
                "Recommendation saved successfully.",
                parent=win
            )


        except Exception as e:

            messagebox.showerror(
                "Recommendation Error",
                str(e),
                parent=win
            )


    # =====================================================
    # BUTTON FRAME
    # =====================================================

    button_frame = tk.Frame(
        main,
        bg="#f4f7f5"
    )

    button_frame.pack(
        pady=5
    )


    # =====================================================
    # RECOMMEND BUTTON
    # =====================================================

    tk.Button(
        button_frame,
        text="🤖  Recommend Crop",
        command=recommend,
        font=("Arial", 11, "bold"),
        bg="#198754",
        fg="white",
        activebackground="#146c43",
        activeforeground="white",
        bd=0,
        padx=25,
        pady=10,
        cursor="hand2"
    ).pack(
        side="left",
        padx=8
    )


    # =====================================================
    # CLEAR BUTTON
    # =====================================================

    def clear_fields():

        farmer_var.set("")
        soil_var.set("")
        weather_var.set("")

        result_label.config(
            text="---"
        )


    tk.Button(
        button_frame,
        text="Clear",
        command=clear_fields,
        font=("Arial", 11, "bold"),
        bg="#6c757d",
        fg="white",
        activebackground="#5c636a",
        activeforeground="white",
        bd=0,
        padx=25,
        pady=10,
        cursor="hand2"
    ).pack(
        side="left",
        padx=8
    )


    # =====================================================
    # CLOSE BUTTON
    # =====================================================

    tk.Button(
        button_frame,
        text="Close",
        command=win.destroy,
        font=("Arial", 11, "bold"),
        bg="#dc3545",
        fg="white",
        activebackground="#bb2d3b",
        activeforeground="white",
        bd=0,
        padx=25,
        pady=10,
        cursor="hand2"
    ).pack(
        side="left",
        padx=8
    )


    # =====================================================
    # LOAD DATA
    # =====================================================

    load_data()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    open_recommendation()

    root.mainloop()
