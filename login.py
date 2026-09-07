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
# LOGIN FUNCTION
# ==========================================

def login():
    email = email_entry.get().strip()
    password = password_entry.get()

    if email == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter email and password."
        )
        return

    try:
        con = get_connection()
        cur = con.cursor()

        # First check email
        cur.execute(
            """
            SELECT UserID, Name, Email, Password
            FROM users
            WHERE Email=%s
            """,
            (email,)
        )

        user = cur.fetchone()

        cur.close()
        con.close()

        # Email not found
        if user is None:
            messagebox.showwarning(
                "Account Not Found",
                "No account found with this email.\n\n"
                "Please register first."
            )
            return

        # Check password
        stored_password = str(user[3])

        if password != stored_password:
            messagebox.showwarning(
                "Wrong Password",
                "Email is correct, but password is incorrect."
            )
            return

        # Login successful
        messagebox.showinfo(
            "Login Successful",
            f"Welcome {user[1]}!"
        )

        login_window.withdraw()

        try:
            import dashboard
            dashboard.open_dashboard()

        except Exception as e:
            login_window.deiconify()
            messagebox.showerror(
                "Dashboard Error",
                str(e)
            )

    except mysql.connector.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )
        # ==================================
        # LOGIN SUCCESS
        # ==================================

        if user:

            messagebox.showinfo(
                "Login Successful",
                "Welcome to Crop Recommendation System!"
            )

            login_window.withdraw()

            try:

                import dashboard
                dashboard.open_dashboard()

            except Exception as e:

                login_window.deiconify()

                messagebox.showerror(
                    "Dashboard Error",
                    str(e)
                )

        # ==================================
        # ACCOUNT NOT FOUND
        # ==================================

        else:

            messagebox.showwarning(
                "Account Not Found",
                "No account found with this email.\n\n"
                "If you are a new user, please click "
                "'Register Here' and create an account first."
            )

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==========================================
# OPEN REGISTRATION
# ==========================================

def open_registration():

    login_window.withdraw()

    try:

        import registration

        registration.open_registration(login_window)

    except Exception as e:

        login_window.deiconify()

        messagebox.showerror(
            "Registration Error",
            str(e)
        )


# ==========================================
# MAIN WINDOW
# ==========================================

login_window = tk.Tk()

login_window.title(
    "Login | Crop Recommendation System"
)

login_window.geometry("900x550")

login_window.resizable(False, False)

login_window.configure(
    bg="white"
)


# ==========================================
# LEFT PANEL
# ==========================================

left_frame = tk.Frame(
    login_window,
    bg="#2E7D32",
    width=430,
    height=550
)

left_frame.pack(
    side="left",
    fill="both"
)

left_frame.pack_propagate(False)


# ==========================================
# LOGO
# ==========================================

tk.Label(
    left_frame,
    text="🌱",
    font=("Arial", 55),
    bg="#2E7D32",
    fg="white"
).pack(
    pady=(80, 10)
)


# ==========================================
# TITLE
# ==========================================

tk.Label(
    left_frame,
    text="Crop Recommendation",
    font=("Arial", 25, "bold"),
    bg="#2E7D32",
    fg="white"
).pack()


tk.Label(
    left_frame,
    text="System",
    font=("Arial", 25, "bold"),
    bg="#2E7D32",
    fg="white"
).pack()


# ==========================================
# SUBTITLE
# ==========================================

tk.Label(
    left_frame,
    text="Smart Farming • Better Crops",
    font=("Arial", 12),
    bg="#2E7D32",
    fg="#E8F5E9"
).pack(
    pady=15
)


# ==========================================
# DESCRIPTION
# ==========================================

tk.Label(
    left_frame,
    text="Make better farming decisions\n"
         "with intelligent crop recommendations.",
    font=("Arial", 11),
    bg="#2E7D32",
    fg="white",
    justify="center"
).pack(
    pady=10
)


# ==========================================
# RIGHT PANEL
# ==========================================

right_frame = tk.Frame(
    login_window,
    bg="white",
    width=470,
    height=550
)

right_frame.pack(
    side="right",
    fill="both"
)

right_frame.pack_propagate(False)


# ==========================================
# WELCOME
# ==========================================

tk.Label(
    right_frame,
    text="Welcome Back!",
    font=("Arial", 25, "bold"),
    bg="white",
    fg="#222222"
).pack(
    pady=(65, 5)
)


tk.Label(
    right_frame,
    text="Login to continue",
    font=("Arial", 11),
    bg="white",
    fg="#777777"
).pack(
    pady=(0, 12)
)


# ==========================================
# NEW USER MESSAGE - RED
# ==========================================

tk.Label(
    right_frame,
    text="New user? Create an account first.",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="red"
).pack(
    pady=(0, 20)
)


# ==========================================
# EMAIL
# ==========================================

tk.Label(
    right_frame,
    text="Email",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#333333"
).pack(
    anchor="w",
    padx=75
)


email_entry = tk.Entry(
    right_frame,
    font=("Arial", 12),
    width=32,
    bd=1,
    relief="solid"
)

email_entry.pack(
    padx=75,
    pady=(7, 20),
    ipady=8
)


# ==========================================
# PASSWORD
# ==========================================

tk.Label(
    right_frame,
    text="Password",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#333333"
).pack(
    anchor="w",
    padx=75
)


password_entry = tk.Entry(
    right_frame,
    font=("Arial", 12),
    width=32,
    show="*",
    bd=1,
    relief="solid"
)

password_entry.pack(
    padx=75,
    pady=(7, 25),
    ipady=8
)


# ==========================================
# LOGIN BUTTON
# ==========================================

tk.Button(
    right_frame,
    text="LOGIN",
    font=("Arial", 11, "bold"),
    bg="#2E7D32",
    fg="white",
    activebackground="#1B5E20",
    activeforeground="white",
    width=28,
    height=2,
    bd=0,
    cursor="hand2",
    command=login
).pack(
    pady=5
)


# ==========================================
# REGISTER LINK
# ==========================================

register_frame = tk.Frame(
    right_frame,
    bg="white"
)

register_frame.pack(
    pady=15
)


tk.Label(
    register_frame,
    text="Don't have an account?",
    font=("Arial", 10),
    bg="white",
    fg="#777777"
).pack(
    side="left"
)


tk.Button(
    register_frame,
    text="Register Here",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#2E7D32",
    activeforeground="#1B5E20",
    bd=0,
    cursor="hand2",
    command=open_registration
).pack(
    side="left",
    padx=5
)


# ==========================================
# FOOTER
# ==========================================

tk.Label(
    right_frame,
    text="Secure Login",
    font=("Arial", 9),
    bg="white",
    fg="#999999"
).pack(
    pady=15
)


# ==========================================
# ENTER KEY = LOGIN
# ==========================================

login_window.bind(
    "<Return>",
    lambda event: login()
)


# ==========================================
# START APPLICATION
# ==========================================

login_window.mainloop()
