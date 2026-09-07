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
# REGISTRATION WINDOW
# ==========================================

def open_registration(login_window):

    registration_window = tk.Toplevel(login_window)

    registration_window.title(
        "Registration | Crop Recommendation System"
    )

    registration_window.geometry("900x550")

    registration_window.resizable(False, False)

    registration_window.configure(
        bg="white"
    )


    GREEN = "#2E7D32"
    DARK_GREEN = "#1B5E20"


    # ==========================================
    # REGISTER FUNCTION
    # ==========================================

    def register():

        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()


        # --------------------------------------
        # EMPTY CHECK
        # --------------------------------------

        if name == "" or email == "" or password == "":

            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )

            return


        # --------------------------------------
        # EMAIL CHECK
        # --------------------------------------

        if "@" not in email or "." not in email:

            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address."
            )

            return


        # --------------------------------------
        # PASSWORD CHECK
        # --------------------------------------

        if len(password) < 6:

            messagebox.showwarning(
                "Invalid Password",
                "Password must contain at least 6 characters."
            )

            return


        try:

            con = get_connection()
            cur = con.cursor()


            # ----------------------------------
            # CHECK EMAIL
            # ----------------------------------

            cur.execute(
                """
                SELECT UserID
                FROM users
                WHERE Email=%s
                """,
                (email,)
            )

            existing_user = cur.fetchone()


            if existing_user:

                messagebox.showerror(
                    "Registration Failed",
                    "This email is already registered."
                )

                cur.close()
                con.close()

                return


            # ----------------------------------
            # INSERT USER
            # ----------------------------------
            #
            # Username column exists in your
            # current database.
            #
            # We don't show Username on screen.
            # Email is stored as hidden Username
            # only to satisfy the existing table.
            #

            cur.execute(
                """
                INSERT INTO users
                (Name, Email, Username, Password)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    email,
                    password
                )
            )


            con.commit()


            cur.close()
            con.close()


            # ----------------------------------
            # SUCCESS
            # ----------------------------------

            messagebox.showinfo(
                "Registration Successful",
                "Account created successfully!"
            )


            # ----------------------------------
            # CLOSE REGISTRATION
            # ----------------------------------

            registration_window.destroy()


            # ----------------------------------
            # KEEP LOGIN HIDDEN
            # ----------------------------------

            login_window.withdraw()


            # ----------------------------------
            # OPEN DASHBOARD DIRECTLY
            # ----------------------------------

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


    # ==========================================
    # BACK TO LOGIN
    # ==========================================

    def back_to_login():

        registration_window.destroy()

        login_window.deiconify()


    # ==========================================
    # LEFT GREEN PANEL
    # ==========================================

    left_frame = tk.Frame(
        registration_window,
        bg=GREEN,
        width=430,
        height=550
    )

    left_frame.pack(
        side="left",
        fill="both"
    )

    left_frame.pack_propagate(False)


    tk.Label(
        left_frame,
        text="🌱",
        font=("Arial", 55),
        bg=GREEN,
        fg="white"
    ).pack(
        pady=(80, 10)
    )


    tk.Label(
        left_frame,
        text="Crop Recommendation",
        font=("Arial", 25, "bold"),
        bg=GREEN,
        fg="white"
    ).pack()


    tk.Label(
        left_frame,
        text="System",
        font=("Arial", 25, "bold"),
        bg=GREEN,
        fg="white"
    ).pack()


    tk.Label(
        left_frame,
        text="Smart Farming • Better Crops",
        font=("Arial", 12),
        bg=GREEN,
        fg="#E8F5E9"
    ).pack(
        pady=15
    )


    tk.Label(
        left_frame,
        text="Create your account and start\n"
             "using smart crop recommendations.",
        font=("Arial", 11),
        bg=GREEN,
        fg="white",
        justify="center"
    ).pack(
        pady=10
    )


    # ==========================================
    # RIGHT PANEL
    # ==========================================

    right_frame = tk.Frame(
        registration_window,
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
    # TITLE
    # ==========================================

    tk.Label(
        right_frame,
        text="Create Account",
        font=("Arial", 25, "bold"),
        bg="white",
        fg="#222222"
    ).pack(
        pady=(55, 5)
    )


    tk.Label(
        right_frame,
        text="Register to continue",
        font=("Arial", 11),
        bg="white",
        fg="#777777"
    ).pack(
        pady=(0, 25)
    )


    # ==========================================
    # FULL NAME
    # ==========================================

    tk.Label(
        right_frame,
        text="Full Name",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#333333"
    ).pack(
        anchor="w",
        padx=75
    )


    name_entry = tk.Entry(
        right_frame,
        font=("Arial", 12),
        width=32,
        bd=1,
        relief="solid"
    )

    name_entry.pack(
        padx=75,
        pady=(7, 15),
        ipady=7
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
        pady=(7, 15),
        ipady=7
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
        pady=(7, 20),
        ipady=7
    )


    # ==========================================
    # REGISTER BUTTON
    # ==========================================

    tk.Button(
        right_frame,
        text="REGISTER",
        font=("Arial", 11, "bold"),
        bg=GREEN,
        fg="white",
        activebackground=DARK_GREEN,
        activeforeground="white",
        width=28,
        height=2,
        bd=0,
        cursor="hand2",
        command=register
    ).pack(
        pady=5
    )


    # ==========================================
    # LOGIN LINK
    # ==========================================

    back_frame = tk.Frame(
        right_frame,
        bg="white"
    )

    back_frame.pack(
        pady=15
    )


    tk.Label(
        back_frame,
        text="Already have an account?",
        font=("Arial", 10),
        bg="white",
        fg="#777777"
    ).pack(
        side="left"
    )


    tk.Button(
        back_frame,
        text="Login Here",
        font=("Arial", 10, "bold"),
        bg="white",
        fg=GREEN,
        activeforeground=DARK_GREEN,
        bd=0,
        cursor="hand2",
        command=back_to_login
    ).pack(
        side="left",
        padx=5
    )


    # ==========================================
    # FOOTER
    # ==========================================

    tk.Label(
        right_frame,
        text="Secure Registration",
        font=("Arial", 9),
        bg="white",
        fg="#999999"
    ).pack(
        pady=2
    )


    # ==========================================
    # CLOSE BUTTON
    # ==========================================

    registration_window.protocol(
        "WM_DELETE_WINDOW",
        back_to_login
    )
