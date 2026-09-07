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
# SOIL MANAGEMENT
# ==========================================

def open_soil():

    win = tk.Toplevel()
    win.title("Soil Management")
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
        text="🌱",
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
        text="Soil Management",
        font=("Arial", 20, "bold"),
        bg=GREEN,
        fg=WHITE
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Manage soil information and records",
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
    # ADD SOIL CARD
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
        text="Add Soil Record",
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
    # pH
    # ==========================================

    tk.Label(
        add_card,
        text="Soil pH",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=SUBTEXT
    ).grid(
        row=1,
        column=0,
        padx=(20, 8),
        pady=(0, 15)
    )

    ph_entry = tk.Entry(
        add_card,
        font=("Arial", 11),
        width=15,
        bd=1,
        relief="solid"
    )

    ph_entry.grid(
        row=1,
        column=1,
        padx=5,
        pady=(0, 15),
        ipady=6
    )

    # ==========================================
    # SOIL TYPE
    # ==========================================

    tk.Label(
        add_card,
        text="Soil Type",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=SUBTEXT
    ).grid(
        row=1,
        column=2,
        padx=(20, 8),
        pady=(0, 15)
    )

    soil_type_entry = tk.Entry(
        add_card,
        font=("Arial", 11),
        width=20,
        bd=1,
        relief="solid"
    )

    soil_type_entry.grid(
        row=1,
        column=3,
        padx=5,
        pady=(0, 15),
        ipady=6
    )

    # ==========================================
    # TABLE
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
    # TREEVIEW STYLE
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
    # SOIL TABLE
    # ==========================================

    tree = ttk.Treeview(
        table_card,
        columns=("id", "ph", "type"),
        show="headings",
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(
        command=tree.yview
    )

    tree.heading(
        "id",
        text="SOIL ID"
    )

    tree.heading(
        "ph",
        text="pH"
    )

    tree.heading(
        "type",
        text="SOIL TYPE"
    )

    tree.column(
        "id",
        width=150,
        anchor="center"
    )

    tree.column(
        "ph",
        width=180,
        anchor="center"
    )

    tree.column(
        "type",
        width=400,
        anchor="w"
    )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # ==========================================
    # LOAD SOIL DATA
    # ==========================================

    def load_soil():

        for item in tree.get_children():
            tree.delete(item)

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                SELECT SoilID, pH, Soil_Type
                FROM Soil
                ORDER BY SoilID
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
    # ADD SOIL
    # ==========================================

    def add_soil():

        ph = ph_entry.get().strip()
        soil_type = soil_type_entry.get().strip()

        if ph == "" or soil_type == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter pH and Soil Type.",
                parent=win
            )

            return

        # Check pH value
        try:

            ph_value = float(ph)

        except ValueError:

            messagebox.showwarning(
                "Invalid pH",
                "Please enter a valid numeric pH value.",
                parent=win
            )

            return

        if ph_value < 0 or ph_value > 14:

            messagebox.showwarning(
                "Invalid pH",
                "pH value must be between 0 and 14.",
                parent=win
            )

            return

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO Soil (pH, Soil_Type)
                VALUES (%s, %s)
                """,
                (ph_value, soil_type)
            )

            con.commit()

            cur.close()
            con.close()

            ph_entry.delete(
                0,
                tk.END
            )

            soil_type_entry.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Success",
                "Soil record added successfully!",
                parent=win
            )

            load_soil()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=win
            )

    # ==========================================
    # DELETE SOIL
    # ==========================================

    def delete_soil():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select a soil record from the table.",
                parent=win
            )

            return

        item = tree.item(
            selected[0]
        )

        soil_id = item["values"][0]

        confirm = messagebox.askyesno(
            "Delete Soil Record",
            f"Are you sure you want to delete\n\n"
            f"Soil ID: {soil_id}?",
            parent=win
        )

        if not confirm:
            return

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                DELETE FROM Soil
                WHERE SoilID=%s
                """,
                (soil_id,)
            )

            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Deleted",
                "Soil record deleted successfully!",
                parent=win
            )

            load_soil()

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
        text="＋  ADD SOIL",
        font=("Arial", 10, "bold"),
        bg=GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        width=18,
        height=2,
        cursor="hand2",
        command=add_soil
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
        command=delete_soil
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

    load_soil()

    ph_entry.bind(
        "<Return>",
        lambda event: add_soil()
    )

    soil_type_entry.bind(
        "<Return>",
        lambda event: add_soil()
    )
