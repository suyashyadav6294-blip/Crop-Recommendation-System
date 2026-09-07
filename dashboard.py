import tkinter as tk
from tkinter import messagebox
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
# GET DATABASE COUNTS
# ==========================================

def get_counts():

    con = None
    cur = None

    try:

        con = get_connection()
        cur = con.cursor()

        # Total Farmers
        cur.execute("SELECT COUNT(*) FROM Farmer")
        farmers = cur.fetchone()[0]

        # Total Crops
        cur.execute("SELECT COUNT(*) FROM Crop")
        crops = cur.fetchone()[0]

        # Total Soil Records
        cur.execute("SELECT COUNT(*) FROM Soil")
        soil = cur.fetchone()[0]

        # Total Recommendations
        cur.execute("SELECT COUNT(*) FROM Recommendation")
        recommendations = cur.fetchone()[0]

        return farmers, crops, soil, recommendations

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

        return 0, 0, 0, 0

    finally:

        if cur:
            cur.close()

        if con:
            con.close()


# ==========================================
# DASHBOARD
# ==========================================

def open_dashboard():

    dashboard_window = tk.Toplevel()

    dashboard_window.title(
        "Dashboard - Crop Recommendation System"
    )

    dashboard_window.geometry("1100x700")

    dashboard_window.resizable(False, False)

    dashboard_window.configure(
        bg="#F4F6F9"
    )


    # ==========================================
    # COLORS
    # ==========================================

    GREEN = "#2E7D32"
    DARK_GREEN = "#1B5E20"
    WHITE = "#FFFFFF"
    BG = "#F4F6F9"
    TEXT = "#222222"
    SUBTEXT = "#666666"


    # ==========================================
    # SIDEBAR
    # ==========================================

    sidebar = tk.Frame(
        dashboard_window,
        bg=GREEN,
        width=230,
        height=700
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)


    # ==========================================
    # LOGO / TITLE
    # ==========================================

    logo = tk.Label(
        sidebar,
        text="CROP\nRECOMMENDATION",
        font=("Arial", 17, "bold"),
        bg=GREEN,
        fg=WHITE,
        justify="center"
    )

    logo.pack(
        pady=(35, 50)
    )


    # ==========================================
    # PAGE FUNCTIONS
    # ==========================================

    def open_farmer():

        try:

            import farmer
            farmer.open_farmer()

            refresh_counts()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    def open_soil():

        try:

            import soil
            soil.open_soil()

            refresh_counts()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    def open_weather():

        try:

            import weather
            weather.open_weather()

            refresh_counts()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    def open_crop():

        try:

            import crop
            crop.open_crop()

            refresh_counts()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    def open_recommendation():

        try:

            import recommendation
            recommendation.open_recommendation()

            refresh_counts()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    def open_history():

        try:

            import history
            history.open_history()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    # ==========================================
    # SIDEBAR BUTTON
    # ==========================================

    def sidebar_button(text, command):

        button = tk.Button(
            sidebar,
            text=text,
            font=("Arial", 11, "bold"),
            bg=GREEN,
            fg=WHITE,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            bd=0,
            relief="flat",
            anchor="w",
            padx=30,
            width=20,
            height=2,
            cursor="hand2",
            command=command
        )

        button.pack(
            fill="x",
            pady=2
        )


    # ==========================================
    # SIDEBAR MENU
    # ==========================================

    sidebar_button(
        "🏠  Dashboard",
        lambda: None
    )

    sidebar_button(
        "👨‍🌾  Farmer",
        open_farmer
    )

    sidebar_button(
        "🌱  Soil",
        open_soil
    )

    sidebar_button(
        "☁  Weather",
        open_weather
    )

    sidebar_button(
        "🌾  Crop",
        open_crop
    )

    sidebar_button(
        "🔮  Recommendation",
        open_recommendation
    )

    sidebar_button(
        "📋  History",
        open_history
    )


    # ==========================================
    # LOGOUT
    # ==========================================

    def logout():

        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if result:

            dashboard_window.destroy()

            import login

            login.login_window.deiconify()


    logout_button = tk.Button(
        sidebar,
        text="🚪  Logout",
        font=("Arial", 11, "bold"),
        bg=DARK_GREEN,
        fg=WHITE,
        activebackground="#124A16",
        activeforeground=WHITE,
        bd=0,
        width=20,
        height=2,
        cursor="hand2",
        command=logout
    )

    logout_button.pack(
        side="bottom",
        pady=25
    )


    # ==========================================
    # MAIN AREA
    # ==========================================

    main_frame = tk.Frame(
        dashboard_window,
        bg=BG
    )

    main_frame.pack(
        side="right",
        fill="both",
        expand=True
    )


    # ==========================================
    # HEADER
    # ==========================================

    header = tk.Frame(
        main_frame,
        bg=WHITE,
        height=80
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)


    heading = tk.Label(
        header,
        text="Dashboard",
        font=("Arial", 25, "bold"),
        bg=WHITE,
        fg=TEXT
    )

    heading.pack(
        side="left",
        padx=30,
        pady=22
    )


    welcome = tk.Label(
        header,
        text="Welcome, Admin",
        font=("Arial", 11),
        bg=WHITE,
        fg=SUBTEXT
    )

    welcome.pack(
        side="right",
        padx=30
    )


    # ==========================================
    # DASHBOARD CONTENT
    # ==========================================

    content = tk.Frame(
        main_frame,
        bg=BG
    )

    content.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=30
    )


    intro = tk.Label(
        content,
        text="Crop Recommendation System",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=TEXT
    )

    intro.pack(
        anchor="w"
    )


    description = tk.Label(
        content,
        text="Manage farmers, soil, weather and crops to generate smart crop recommendations.",
        font=("Arial", 11),
        bg=BG,
        fg=SUBTEXT
    )

    description.pack(
        anchor="w",
        pady=(5, 25)
    )


    # ==========================================
    # STAT CARDS
    # ==========================================

    cards_frame = tk.Frame(
        content,
        bg=BG
    )

    cards_frame.pack(
        fill="x"
    )


    def create_card(parent, title):

        card = tk.Frame(
            parent,
            bg=WHITE,
            width=190,
            height=120,
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            padx=(0, 20)
        )

        card.pack_propagate(False)


        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=SUBTEXT
        )

        title_label.pack(
            pady=(20, 5)
        )


        value_label = tk.Label(
            card,
            text="0",
            font=("Arial", 25, "bold"),
            bg=WHITE,
            fg=GREEN
        )

        value_label.pack()


        return value_label


    # Create cards
    farmer_value = create_card(
        cards_frame,
        "Total Farmers"
    )

    crop_value = create_card(
        cards_frame,
        "Total Crops"
    )

    soil_value = create_card(
        cards_frame,
        "Soil Records"
    )

    recommendation_value = create_card(
        cards_frame,
        "Recommendations"
    )


    # ==========================================
    # REFRESH COUNTS
    # ==========================================

    def refresh_counts():

        farmers, crops, soil, recommendations = get_counts()

        farmer_value.config(
            text=str(farmers)
        )

        crop_value.config(
            text=str(crops)
        )

        soil_value.config(
            text=str(soil)
        )

        recommendation_value.config(
            text=str(recommendations)
        )


    # Load database counts
    refresh_counts()


    # ==========================================
    # QUICK ACTIONS
    # ==========================================

    quick_title = tk.Label(
        content,
        text="Quick Actions",
        font=("Arial", 18, "bold"),
        bg=BG,
        fg=TEXT
    )

    quick_title.pack(
        anchor="w",
        pady=(45, 15)
    )


    quick_frame = tk.Frame(
        content,
        bg=BG
    )

    quick_frame.pack(
        fill="x"
    )


    def quick_button(text, command):

        btn = tk.Button(
            quick_frame,
            text=text,
            font=("Arial", 11, "bold"),
            bg=GREEN,
            fg=WHITE,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            width=22,
            height=2,
            bd=0,
            cursor="hand2",
            command=command
        )

        btn.pack(
            side="left",
            padx=(0, 15)
        )


    quick_button(
        "Add Farmer",
        open_farmer
    )

    quick_button(
        "Add Soil Data",
        open_soil
    )

    quick_button(
        "Add Weather",
        open_weather
    )

    quick_button(
        "Get Recommendation",
        open_recommendation
    )


# ==========================================
# TEST DASHBOARD
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    open_dashboard()

    root.mainloop()
