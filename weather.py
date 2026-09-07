import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="crop_recommendation_system"
    )


# ==========================================
# WEATHER MANAGEMENT
# ==========================================

def open_weather():

    win = tk.Toplevel()
    win.title("Weather Management")
    win.geometry("850x620")
    win.resizable(False, False)
    win.configure(bg="#F4F6F9")

    GREEN = "#2E7D32"
    DARK_GREEN = "#1B5E20"
    WHITE = "#FFFFFF"
    BG = "#F4F6F9"
    TEXT = "#222222"
    SUBTEXT = "#666666"
    RED = "#D32F2F"

    # ==========================================
    # HEADER
    # ==========================================

    header = tk.Frame(
        win,
        bg=GREEN,
        height=85
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="☁",
        font=("Arial", 30),
        bg=GREEN,
        fg=WHITE
    ).pack(
        side="left",
        padx=(30, 12)
    )

    title_frame = tk.Frame(
        header,
        bg=GREEN
    )
    title_frame.pack(
        side="left",
        pady=12
    )

    tk.Label(
        title_frame,
        text="Weather Management",
        font=("Arial", 20, "bold"),
        bg=GREEN,
        fg=WHITE
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Manage temperature and rainfall records",
        font=("Arial", 10),
        bg=GREEN,
        fg="#E8F5E9"
    ).pack(anchor="w")

    # ==========================================
    # MAIN CONTENT
    # ==========================================

    content = tk.Frame(
        win,
        bg=BG
    )

    content.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    # ==========================================
    # ADD WEATHER CARD
    # ==========================================

    add_card = tk.Frame(
        content,
        bg=WHITE,
        bd=1,
        relief="solid"
    )

    add_card.pack(
        fill="x"
    )

    tk.Label(
        add_card,
        text="Add Weather Record",
        font=("Arial", 14, "bold"),
        bg=WHITE,
        fg=TEXT
    ).grid(
        row=0,
        column=0,
        columnspan=5,
        sticky="w",
        padx=20,
        pady=(15, 15)
    )

    # ==========================================
    # TEMPERATURE
    # ==========================================

    tk.Label(
        add_card,
        text="Temperature (°C)",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=SUBTEXT
    ).grid(
        row=1,
        column=0,
        padx=(20, 8),
        pady=(0, 15)
    )

    temperature_entry = tk.Entry(
        add_card,
        font=("Arial", 11),
        width=18,
        bd=1,
        relief="solid"
    )

    temperature_entry.grid(
        row=1,
        column=1,
        padx=5,
        pady=(0, 15),
        ipady=6
    )

    # ==========================================
    # RAINFALL
    # ==========================================

    tk.Label(
        add_card,
        text="Rainfall (mm)",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=SUBTEXT
    ).grid(
        row=1,
        column=2,
        padx=(20, 8),
        pady=(0, 15)
    )

    rainfall_entry = tk.Entry(
        add_card,
        font=("Arial", 11),
        width=18,
        bd=1,
        relief="solid"
    )

    rainfall_entry.grid(
        row=1,
        column=3,
        padx=5,
        pady=(0, 15),
        ipady=6
    )

    # ==========================================
    # TABLE CARD
    # ==========================================

    table_card = tk.Frame(
        content,
        bg=WHITE,
        bd=1,
        relief="solid"
    )

    table_card.pack(
        fill="both",
        expand=True,
        pady=(20, 0)
    )

    # ==========================================
    # TABLE STYLE
    # ==========================================

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=TEXT,
        rowheight=35,
        fieldbackground=WHITE,
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        background=GREEN,
        foreground=WHITE,
        font=("Arial", 10, "bold"),
        padding=8
    )

    style.map(
        "Treeview",
        background=[
            ("selected", "#E8F5E9")
        ],
        foreground=[
            ("selected", TEXT)
        ]
    )

    # ==========================================
    # SCROLLBAR
    # ==========================================

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ==========================================
    # WEATHER TABLE
    # ==========================================

    tree = ttk.Treeview(
        table_card,
        columns=("id", "temperature", "rainfall"),
        show="headings",
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(
        command=tree.yview
    )

    tree.heading(
        "id",
        text="WEATHER ID"
    )

    tree.heading(
        "temperature",
        text="TEMPERATURE (°C)"
    )

    tree.heading(
        "rainfall",
        text="RAINFALL (mm)"
    )

    tree.column(
        "id",
        width=180,
        anchor="center"
    )

    tree.column(
        "temperature",
        width=220,
        anchor="center"
    )

    tree.column(
        "rainfall",
        width=300,
        anchor="center"
    )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # ==========================================
    # LOAD WEATHER DATA
    # ==========================================

    def load_weather():

        for item in tree.get_children():
            tree.delete(item)

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                SELECT WeatherID, Temperature, Rainfall
                FROM Weather
                ORDER BY WeatherID
                """
            )

            records = cur.fetchall()

            for row in records:

                tree.insert(
                    "",
                    tk.END,
                    values=row
                )

            cur.close()
            con.close()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=win
            )

    # ==========================================
    # ADD WEATHER
    # ==========================================

    def add_weather():

        temperature = temperature_entry.get().strip()
        rainfall = rainfall_entry.get().strip()

        if temperature == "" or rainfall == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter temperature and rainfall.",
                parent=win
            )

            return

        # Temperature validation
        try:

            temperature_value = float(temperature)

        except ValueError:

            messagebox.showwarning(
                "Invalid Temperature",
                "Please enter a valid numeric temperature.",
                parent=win
            )

            return

        # Rainfall validation
        try:

            rainfall_value = float(rainfall)

        except ValueError:

            messagebox.showwarning(
                "Invalid Rainfall",
                "Please enter a valid numeric rainfall.",
                parent=win
            )

            return

        if rainfall_value < 0:

            messagebox.showwarning(
                "Invalid Rainfall",
                "Rainfall cannot be negative.",
                parent=win
            )

            return

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO Weather
                (Temperature, Rainfall)
                VALUES (%s, %s)
                """,
                (
                    temperature_value,
                    rainfall_value
                )
            )

            con.commit()

            cur.close()
            con.close()

            temperature_entry.delete(
                0,
                tk.END
            )

            rainfall_entry.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Success",
                "Weather record added successfully!",
                parent=win
            )

            load_weather()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=win
            )

    # ==========================================
    # DELETE WEATHER
    # ==========================================

    def delete_weather():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select a weather record from the table.",
                parent=win
            )

            return

        item = tree.item(
            selected[0]
        )

        weather_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Delete Weather Record",
            f"Are you sure you want to delete\n\n"
            f"Weather ID: {weather_id}?",
            parent=win
        )

        if not confirm:
            return

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                DELETE FROM Weather
                WHERE WeatherID=%s
                """,
                (weather_id,)
            )

            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Deleted",
                "Weather record deleted successfully!",
                parent=win
            )

            load_weather()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=win
            )

    # ==========================================
    # BUTTONS
    # ==========================================

    button_frame = tk.Frame(
        add_card,
        bg=WHITE
    )

    button_frame.grid(
        row=2,
        column=0,
        columnspan=5,
        pady=(0, 15)
    )

    tk.Button(
        button_frame,
        text="＋  ADD WEATHER",
        font=("Arial", 10, "bold"),
        bg=GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        width=18,
        height=2,
        cursor="hand2",
        command=add_weather
    ).pack(
        side="left",
        padx=10
    )

    tk.Button(
        button_frame,
        text="🗑  DELETE SELECTED",
        font=("Arial", 10, "bold"),
        bg=RED,
        fg=WHITE,
        activebackground="#B71C1C",
        activeforeground=WHITE,
        bd=0,
        width=20,
        height=2,
        cursor="hand2",
        command=delete_weather
    ).pack(
        side="left",
        padx=10
    )

    tk.Button(
        button_frame,
        text="CLOSE",
        font=("Arial", 10, "bold"),
        bg="#607D8B",
        fg=WHITE,
        activebackground="#455A64",
        activeforeground=WHITE,
        bd=0,
        width=12,
        height=2,
        cursor="hand2",
        command=win.destroy
    ).pack(
        side="left",
        padx=10
    )

    # ==========================================
    # LOAD EXISTING DATA
    # ==========================================

    load_weather()

    temperature_entry.bind(
        "<Return>",
        lambda event: add_weather()
    )

    rainfall_entry.bind(
        "<Return>",
        lambda event: add_weather()
    )
