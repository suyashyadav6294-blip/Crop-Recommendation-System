import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


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
# OPEN HISTORY WINDOW
# =========================================================

def open_history():

    win = tk.Toplevel()
    win.title("Recommendation History")
    win.geometry("950x600")
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
        text="📋 RECOMMENDATION HISTORY",
        font=("Arial", 22, "bold"),
        bg="#198754",
        fg="white"
    ).pack(pady=(18, 2))

    tk.Label(
        header,
        text="View all crop recommendations saved in the system",
        font=("Arial", 10),
        bg="#198754",
        fg="white"
    ).pack()


    # =====================================================
    # MAIN FRAME
    # =====================================================

    main = tk.Frame(
        win,
        bg="#f4f7f5"
    )
    main.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=25
    )


    # =====================================================
    # TABLE CARD
    # =====================================================

    table_card = tk.Frame(
        main,
        bg="white",
        bd=1,
        relief="solid"
    )
    table_card.pack(
        fill="both",
        expand=True
    )


    # =====================================================
    # TITLE
    # =====================================================

    tk.Label(
        table_card,
        text="Saved Recommendations",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#198754"
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 10)
    )


    # =====================================================
    # TABLE FRAME
    # =====================================================

    tree_frame = tk.Frame(
        table_card,
        bg="white"
    )
    tree_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


    # =====================================================
    # SCROLLBARS
    # =====================================================

    y_scroll = ttk.Scrollbar(
        tree_frame,
        orient="vertical"
    )

    x_scroll = ttk.Scrollbar(
        tree_frame,
        orient="horizontal"
    )


    # =====================================================
    # TREEVIEW
    # =====================================================

    columns = (
        "RecommendationID",
        "Farmer",
        "Soil",
        "Temperature",
        "Rainfall",
        "Crop"
    )

    history_table = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set,
        height=13
    )


    y_scroll.config(
        command=history_table.yview
    )

    x_scroll.config(
        command=history_table.xview
    )


    # =====================================================
    # COLUMN HEADINGS
    # =====================================================

    history_table.heading(
        "RecommendationID",
        text="Recommendation ID"
    )

    history_table.heading(
        "Farmer",
        text="Farmer"
    )

    history_table.heading(
        "Soil",
        text="Soil"
    )

    history_table.heading(
        "Temperature",
        text="Temperature (°C)"
    )

    history_table.heading(
        "Rainfall",
        text="Rainfall (mm)"
    )

    history_table.heading(
        "Crop",
        text="Recommended Crop"
    )


    # =====================================================
    # COLUMN WIDTHS
    # =====================================================

    history_table.column(
        "RecommendationID",
        width=150,
        anchor="center"
    )

    history_table.column(
        "Farmer",
        width=170,
        anchor="center"
    )

    history_table.column(
        "Soil",
        width=180,
        anchor="center"
    )

    history_table.column(
        "Temperature",
        width=150,
        anchor="center"
    )

    history_table.column(
        "Rainfall",
        width=130,
        anchor="center"
    )

    history_table.column(
        "Crop",
        width=180,
        anchor="center"
    )


    # =====================================================
    # TREEVIEW STYLE
    # =====================================================

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        rowheight=32,
        font=("Arial", 10),
        background="white",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold"),
        padding=8
    )

    style.map(
        "Treeview",
        background=[
            ("selected", "#198754")
        ],
        foreground=[
            ("selected", "white")
        ]
    )


    # =====================================================
    # PACK TABLE
    # =====================================================

    history_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    y_scroll.pack(
        side="right",
        fill="y"
    )

    x_scroll.pack(
        side="bottom",
        fill="x"
    )


    # =====================================================
    # LOAD HISTORY
    # =====================================================

    def load_history():

        # Clear existing rows
        for item in history_table.get_children():
            history_table.delete(item)


        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()


            query = """
            SELECT
                r.RecommendationID,
                f.Name,
                CONCAT('pH: ', s.pH, ' - ', s.Soil_Type),
                w.Temperature,
                w.Rainfall,
                c.Crop_Name

            FROM Recommendation r

            JOIN Farmer f
                ON r.FarmerID = f.FarmerID

            JOIN Soil s
                ON r.SoilID = s.SoilID

            JOIN Weather w
                ON r.WeatherID = w.WeatherID

            JOIN Crop c
                ON r.CropID = c.CropID

            ORDER BY r.RecommendationID DESC
            """


            cursor.execute(query)

            records = cursor.fetchall()


            for row in records:

                history_table.insert(
                    "",
                    "end",
                    values=row
                )


            count_label.config(
                text=f"Total Recommendations: {len(records)}"
            )


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
    # DELETE SELECTED RECORD
    # =====================================================

    def delete_record():

        selected = history_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Record",
                "Please select a recommendation to delete.",
                parent=win
            )

            return


        values = history_table.item(
            selected[0],
            "values"
        )

        recommendation_id = values[0]


        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this recommendation?",
            parent=win
        )


        if not confirm:
            return


        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()


            cursor.execute(
                """
                DELETE FROM Recommendation
                WHERE RecommendationID = %s
                """,
                (recommendation_id,)
            )


            connection.commit()


            messagebox.showinfo(
                "Deleted",
                "Recommendation deleted successfully.",
                parent=win
            )


            load_history()


        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                str(e),
                parent=win
            )

        finally:

            if connection:
                connection.close()


    # =====================================================
    # BOTTOM FRAME
    # =====================================================

    bottom = tk.Frame(
        main,
        bg="#f4f7f5"
    )
    bottom.pack(
        fill="x",
        pady=(15, 0)
    )


    # =====================================================
    # COUNT LABEL
    # =====================================================

    count_label = tk.Label(
        bottom,
        text="Total Recommendations: 0",
        font=("Arial", 10, "bold"),
        bg="#f4f7f5",
        fg="#555555"
    )

    count_label.pack(
        side="left"
    )


    # =====================================================
    # REFRESH BUTTON
    # =====================================================

    tk.Button(
        bottom,
        text="🔄 Refresh",
        command=load_history,
        font=("Arial", 10, "bold"),
        bg="#198754",
        fg="white",
        activebackground="#146c43",
        activeforeground="white",
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2"
    ).pack(
        side="right",
        padx=5
    )


    # =====================================================
    # DELETE BUTTON
    # =====================================================

    tk.Button(
        bottom,
        text="🗑 Delete",
        command=delete_record,
        font=("Arial", 10, "bold"),
        bg="#dc3545",
        fg="white",
        activebackground="#bb2d3b",
        activeforeground="white",
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2"
    ).pack(
        side="right",
        padx=5
    )


    # =====================================================
    # CLOSE BUTTON
    # =====================================================

    tk.Button(
        bottom,
        text="Close",
        command=win.destroy,
        font=("Arial", 10, "bold"),
        bg="#6c757d",
        fg="white",
        activebackground="#5c636a",
        activeforeground="white",
        bd=0,
        padx=20,
        pady=8,
        cursor="hand2"
    ).pack(
        side="right",
        padx=5
    )


    # =====================================================
    # LOAD DATA WHEN WINDOW OPENS
    # =====================================================

    load_history()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    open_history()

    root.mainloop()
