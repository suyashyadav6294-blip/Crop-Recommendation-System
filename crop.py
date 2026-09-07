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
# CROP MANAGEMENT
# ==========================================

def open_crop():

    win = tk.Toplevel()
    win.title("Crop Management")
    win.geometry("800x600")
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
        text="🌾",
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
        text="Crop Management",
        font=("Arial", 20, "bold"),
        bg=GREEN,
        fg=WHITE
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Manage crop records",
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
    # ADD CROP CARD
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
        text="Add New Crop",
        font=("Arial", 14, "bold"),
        bg=WHITE,
        fg=TEXT
    ).grid(
        row=0,
        column=0,
        columnspan=3,
        sticky="w",
        padx=20,
        pady=(15, 12)
    )

    tk.Label(
        add_card,
        text="Crop Name",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=SUBTEXT
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=(20, 8),
        pady=(0, 15)
    )

    crop_entry = tk.Entry(
        add_card,
        font=("Arial", 11),
        width=38,
        bd=1,
        relief="solid"
    )

    crop_entry.grid(
        row=1,
        column=1,
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
    # CROP TABLE
    # ==========================================

    tree = ttk.Treeview(
        table_card,
        columns=("id", "name"),
        show="headings",
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(
        command=tree.yview
    )

    tree.heading(
        "id",
        text="CROP ID"
    )

    tree.heading(
        "name",
        text="CROP NAME"
    )

    tree.column(
        "id",
        width=180,
        anchor="center"
    )

    tree.column(
        "name",
        width=450,
        anchor="w"
    )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # ==========================================
    # LOAD CROPS
    # ==========================================

    def load_crops():

        for item in tree.get_children():
            tree.delete(item)

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                SELECT CropID, Crop_Name
                FROM Crop
                ORDER BY CropID
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
    # ADD CROP
    # ==========================================

    def add_crop():

        name = crop_entry.get().strip()

        if name == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter crop name.",
                parent=win
            )

            crop_entry.focus()

            return

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO Crop (Crop_Name)
                VALUES (%s)
                """,
                (name,)
            )

            con.commit()

            cur.close()
            con.close()

            crop_entry.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Success",
                "Crop added successfully!",
                parent=win
            )

            load_crops()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=win
            )

    # ==========================================
    # DELETE CROP
    # ==========================================

    def delete_crop():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Crop",
                "Please select a crop from the table.",
                parent=win
            )

            return

        item = tree.item(
            selected[0]
        )

        crop_id = item["values"][0]
        crop_name = item["values"][1]

        confirm = messagebox.askyesno(
            "Delete Crop",
            f"Are you sure you want to delete\n\n"
            f"Crop: {crop_name}\n"
            f"ID: {crop_id}?",
            parent=win
        )

        if not confirm:
            return

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                DELETE FROM Crop
                WHERE CropID=%s
                """,
                (crop_id,)
            )

            con.commit()

            cur.close()
            con.close()

            messagebox.showinfo(
                "Deleted",
                "Crop deleted successfully!",
                parent=win
            )

            load_crops()

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
        columnspan=3,
        pady=(0, 15)
    )

    tk.Button(
        button_frame,
        text="＋  ADD CROP",
        font=("Arial", 10, "bold"),
        bg=GREEN,
        fg=WHITE,
        activebackground=DARK_GREEN,
        activeforeground=WHITE,
        bd=0,
        width=18,
        height=2,
        cursor="hand2",
        command=add_crop
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
        command=delete_crop
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

    load_crops()

    crop_entry.bind(
        "<Return>",
        lambda event: add_crop()
    )
