import customtkinter as ctk
import sys
from database.db_connection import connect_db
from tkinter import messagebox
from ui.navigation import open_dashboard


# Get logged-in user's ID
if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("View Expenses")
app.geometry("900x600")


# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    app,
    text="View Expenses",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# ---------------- TABLE FRAME ----------------

table_frame = ctk.CTkFrame(
    app,
    width=800,
    height=400
)

table_frame.pack(pady=20)
table_frame.pack_propagate(False)


# ---------------- HEADERS ----------------

category_header = ctk.CTkLabel(
    table_frame,
    text="Category",
    font=("Arial", 16, "bold")
)

category_header.grid(
    row=0,
    column=0,
    padx=35,
    pady=20
)


amount_header = ctk.CTkLabel(
    table_frame,
    text="Amount",
    font=("Arial", 16, "bold")
)

amount_header.grid(
    row=0,
    column=1,
    padx=35,
    pady=20
)


description_header = ctk.CTkLabel(
    table_frame,
    text="Description",
    font=("Arial", 16, "bold")
)

description_header.grid(
    row=0,
    column=2,
    padx=35,
    pady=20
)


date_header = ctk.CTkLabel(
    table_frame,
    text="Date",
    font=("Arial", 16, "bold")
)

date_header.grid(
    row=0,
    column=3,
    padx=35,
    pady=20
)


# ---------------- SEPARATOR ----------------

separator = ctk.CTkFrame(
    table_frame,
    height=2
)

separator.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="ew",
    padx=10,
    pady=5
)


# ---------------- NO DATA LABEL ----------------

no_data = ctk.CTkLabel(
    table_frame,
    text="No expenses found",
    font=("Arial", 14)
)


# ---------------- LOAD EXPENSES ----------------

def load_expenses():

    connection = None
    cursor = None

    try:

        connection = connect_db()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Database connection failed!"
            )
            return

        cursor = connection.cursor()

        query = """
        SELECT
            categories.category_name,
            expenses.amount,
            expenses.description,
            expenses.expense_date
        FROM expenses
        JOIN categories
            ON expenses.category_id = categories.category_id
        WHERE expenses.user_id = %s
        ORDER BY expenses.expense_date DESC
        """

        cursor.execute(query, (user_id,))

        expenses = cursor.fetchall()


        # ---------------- DISPLAY DATA ----------------

        if len(expenses) == 0:

            no_data.grid(
                row=2,
                column=0,
                columnspan=4,
                pady=30
            )

        else:

            no_data.grid_forget()

            row_number = 2

            for expense in expenses:

                category = expense[0]
                amount = expense[1]
                description = expense[2]
                expense_date = expense[3]


                # Category
                category_label = ctk.CTkLabel(
                    table_frame,
                    text=category,
                    font=("Arial", 14)
                )

                category_label.grid(
                    row=row_number,
                    column=0,
                    padx=35,
                    pady=8
                )


                # Amount
                amount_label = ctk.CTkLabel(
                    table_frame,
                    text=f"₹{amount:.2f}",
                    font=("Arial", 14)
                )

                amount_label.grid(
                    row=row_number,
                    column=1,
                    padx=35,
                    pady=8
                )


                # Description
                description_label = ctk.CTkLabel(
                    table_frame,
                    text=description if description else "-",
                    font=("Arial", 14)
                )

                description_label.grid(
                    row=row_number,
                    column=2,
                    padx=35,
                    pady=8
                )


                # Date
                date_label = ctk.CTkLabel(
                    table_frame,
                    text=str(expense_date),
                    font=("Arial", 14)
                )

                date_label.grid(
                    row=row_number,
                    column=3,
                    padx=35,
                    pady=8
                )


                row_number += 1


    except Exception as e:

        print("VIEW EXPENSES ERROR:", repr(e))

        messagebox.showerror(
            "Error",
            repr(e)
        )


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ---------------- BACK BUTTON ----------------

def go_back():

    app.destroy()
    open_dashboard(user_id)


back_button = ctk.CTkButton(
    app,
    text="Back",
    width=180,
    command=go_back
)

back_button.pack(pady=20)


# Load expenses when window opens
load_expenses()


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":
    app.mainloop()