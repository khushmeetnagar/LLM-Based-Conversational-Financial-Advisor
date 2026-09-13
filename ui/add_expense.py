import customtkinter as ctk
from database.db_connection import connect_db
import sys
from tkinter import messagebox
from datetime import datetime

user_id = int(sys.argv[1])

def load_categories():
    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    cursor.execute(
        "SELECT category_id, category_name FROM categories"
    )

    categories = cursor.fetchall()

    cursor.close()
    connection.close()

    return categories




def load_payment_methods():
    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    cursor.execute(
        "SELECT payment_method_id, method_name FROM payment_methods"
    )

    payment_methods = cursor.fetchall()

    cursor.close()
    connection.close()

    return payment_methods

payment_methods = load_payment_methods()

payment_names = []

for payment in payment_methods:
    payment_names.append(payment[1])

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Add Expense")
app.geometry("900x600")

title = ctk.CTkLabel(
    app,
    text="Add Expense",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)

form_frame = ctk.CTkFrame(
    app,
    width=500,
    height=450
)

form_frame.pack(pady=20)
form_frame.pack_propagate(False)
category_label = ctk.CTkLabel(
    form_frame,
    text="Category",
    font=("Arial", 16)
)
category_label.grid(
    row=0,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

categories = load_categories()

category_names = []

for category in categories:
    category_names.append(category[1])

category_entry = ctk.CTkComboBox(
    form_frame,
    width=250,
    values=category_names
)

category_entry.grid(
    row=0,
    column=1,
    padx=20,
    pady=15
)


payment_methods = load_payment_methods()

payment_names = []

for payment in payment_methods:
    payment_names.append(payment[1])


payment_label = ctk.CTkLabel(
    form_frame,
    text="Payment Method",
    font=("Arial", 16)
)

payment_label.grid(
    row=1,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

payment_entry = ctk.CTkComboBox(
    form_frame,
    width=250,
    values=payment_names
)

payment_entry.grid(
    row=1,
    column=1,
    padx=20,
    pady=15
)

amount_label = ctk.CTkLabel(
    form_frame,
    text="Amount",
    font=("Arial", 16)
)
amount_label.grid(
    row=2,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

amount_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter amount"
)
amount_entry.grid(
    row=2,
    column=1,
    padx=20,
    pady=15
)
description_label = ctk.CTkLabel(
    form_frame,
    text="Description",
    font=("Arial", 16)
)
description_label.grid(
    row=3,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

description_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter description"
)
description_entry.grid(
    row=3,
    column=1,
    padx=20,
    pady=15
)
date_label = ctk.CTkLabel(
    form_frame,
    text="Date",
    font=("Arial", 16)
)
date_label.grid(
    row=4,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

date_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="DD-MM-YYYY"
)
date_entry.grid(
    row=4,
    column=1,
    padx=20,
    pady=15
)

def save_expense():

    category = category_entry.get()
    payment_method = payment_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()
    expense_date = date_entry.get()

    # Validation
    if category == "" or payment_method == "" or amount == "" or expense_date == "":
        messagebox.showerror(
            "Error",
            "Please fill all required fields!"
        )
        return

    # Validate amount
    try:
        amount = float(amount)

        if amount <= 0:
            messagebox.showerror(
                "Error",
                "Amount must be greater than 0."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid amount."
        )
        return

    # Convert date DD-MM-YYYY → YYYY-MM-DD
    try:
        formatted_date = datetime.strptime(
            expense_date,
            "%d-%m-%Y"
        ).strftime("%Y-%m-%d")

    except ValueError:
        messagebox.showerror(
            "Error",
            "Date must be in DD-MM-YYYY format."
        )
        return

    connection = None
    cursor = None

    try:

        connection = connect_db()

        if connection is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        cursor = connection.cursor()

        # Get category_id
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = %s
            """,
            (category,)
        )

        category_result = cursor.fetchone()

        if category_result is None:
            messagebox.showerror(
                "Error",
                "Category not found!"
            )
            return

        category_id = category_result[0]

        # Get payment_method_id
        cursor.execute(
            """
            SELECT payment_method_id
            FROM payment_methods
            WHERE method_name = %s
            """,
            (payment_method,)
        )

        payment_result = cursor.fetchone()

        if payment_result is None:
            messagebox.showerror(
                "Error",
                "Payment method not found!"
            )
            return

        payment_method_id = payment_result[0]

        # Insert expense
        query = """
        INSERT INTO expenses
        (
            user_id,
            category_id,
            payment_method_id,
            amount,
            expense_date,
            place,
            description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                category_id,
                payment_method_id,
                amount,
                formatted_date,
                None,
                description
            )
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Expense saved successfully!"
        )

        # Clear form
        category_entry.set("")
        payment_entry.set("")
        amount_entry.delete(0, "end")
        description_entry.delete(0, "end")
        date_entry.delete(0, "end")

    except Exception as e:

        if connection:
            connection.rollback()

        messagebox.showerror(
            "Error",
            str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

save_button = ctk.CTkButton(
    form_frame,
    text="Save Expense",
    width=180,
    command=save_expense
)

save_button.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=20
)

back_button = ctk.CTkButton(
    form_frame,
    text="Back",
    width=180
)

back_button.grid(
    row=6,
    column=0,
    columnspan=2,
    pady=10
)
if __name__ == "__main__":
    app.mainloop()