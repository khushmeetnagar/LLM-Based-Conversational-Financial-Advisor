import customtkinter as ctk
from database.db_connection import connect_db
import sys
from tkinter import messagebox
from datetime import datetime


# --------------------------------------------------
# USER ID
# --------------------------------------------------

user_id = int(sys.argv[1])


# --------------------------------------------------
# LOAD CATEGORIES
# --------------------------------------------------

def load_categories():

    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT category_id, category_name FROM categories"
        )

        categories = cursor.fetchall()

        return categories

    finally:
        cursor.close()
        connection.close()


# --------------------------------------------------
# LOAD PAYMENT METHODS
# --------------------------------------------------

def load_payment_methods():

    connection = connect_db()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT payment_method_id, method_name FROM payment_methods"
        )

        payment_methods = cursor.fetchall()

        return payment_methods

    finally:
        cursor.close()
        connection.close()


# --------------------------------------------------
# THEME
# --------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# --------------------------------------------------
# COLORS
# --------------------------------------------------

BG_COLOR = "#0B1120"
CARD_COLOR = "#111827"
INPUT_COLOR = "#1F2937"

TEXT_COLOR = "#F9FAFB"
SECONDARY_TEXT = "#9CA3AF"

ACCENT_COLOR = "#2563EB"
ACCENT_HOVER = "#1D4ED8"

BORDER_COLOR = "#374151"

SUCCESS_COLOR = "#10B981"


# --------------------------------------------------
# MAIN WINDOW
# --------------------------------------------------

app = ctk.CTk()

app.title("Add Expense - FinVest AI")

app.geometry("1050x720")

app.minsize(900, 650)

app.configure(fg_color=BG_COLOR)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

header_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header_frame.pack(
    fill="x",
    padx=40,
    pady=(25, 10)
)


title = ctk.CTkLabel(
    header_frame,
    text="Add New Expense",
    font=("Arial", 30, "bold"),
    text_color=TEXT_COLOR
)

title.pack(anchor="w")


subtitle = ctk.CTkLabel(
    header_frame,
    text="Record your spending and keep your financial data organized.",
    font=("Arial", 14),
    text_color=SECONDARY_TEXT
)

subtitle.pack(
    anchor="w",
    pady=(5, 0)
)


# --------------------------------------------------
# MAIN SCROLLABLE AREA
# --------------------------------------------------

scroll_frame = ctk.CTkScrollableFrame(
    app,
    fg_color="transparent"
)

scroll_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


# --------------------------------------------------
# EXPENSE CARD
# --------------------------------------------------

form_frame = ctk.CTkFrame(
    scroll_frame,
    fg_color=CARD_COLOR,
    corner_radius=18,
    border_width=1,
    border_color=BORDER_COLOR
)

form_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


# --------------------------------------------------
# CARD HEADER
# --------------------------------------------------

form_title = ctk.CTkLabel(
    form_frame,
    text="Expense Details",
    font=("Arial", 21, "bold"),
    text_color=TEXT_COLOR
)

form_title.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=35,
    pady=(30, 5),
    sticky="w"
)


form_subtitle = ctk.CTkLabel(
    form_frame,
    text="Enter the details of your expense below.",
    font=("Arial", 13),
    text_color=SECONDARY_TEXT
)

form_subtitle.grid(
    row=1,
    column=0,
    columnspan=2,
    padx=35,
    pady=(0, 25),
    sticky="w"
)


# --------------------------------------------------
# GRID CONFIGURATION
# --------------------------------------------------

form_frame.grid_columnconfigure(0, weight=1)
form_frame.grid_columnconfigure(1, weight=2)


# --------------------------------------------------
# CATEGORY
# --------------------------------------------------

category_label = ctk.CTkLabel(
    form_frame,
    text="Category *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

category_label.grid(
    row=2,
    column=0,
    padx=(35, 15),
    pady=(10, 8),
    sticky="w"
)


categories = load_categories()

category_names = []

for category in categories:
    category_names.append(category[1])


category_entry = ctk.CTkComboBox(
    form_frame,
    width=300,
    height=42,
    values=category_names,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    button_color=ACCENT_COLOR,
    button_hover_color=ACCENT_HOVER,
    text_color=TEXT_COLOR,
    dropdown_fg_color=CARD_COLOR,
    dropdown_text_color=TEXT_COLOR
)

category_entry.grid(
    row=2,
    column=1,
    padx=(15, 35),
    pady=(10, 8),
    sticky="ew"
)


# --------------------------------------------------
# PAYMENT METHOD
# --------------------------------------------------

payment_label = ctk.CTkLabel(
    form_frame,
    text="Payment Method *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

payment_label.grid(
    row=3,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


payment_methods = load_payment_methods()

payment_names = []

for payment in payment_methods:
    payment_names.append(payment[1])


payment_entry = ctk.CTkComboBox(
    form_frame,
    width=300,
    height=42,
    values=payment_names,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    button_color=ACCENT_COLOR,
    button_hover_color=ACCENT_HOVER,
    text_color=TEXT_COLOR,
    dropdown_fg_color=CARD_COLOR,
    dropdown_text_color=TEXT_COLOR
)

payment_entry.grid(
    row=3,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# --------------------------------------------------
# AMOUNT
# --------------------------------------------------

amount_label = ctk.CTkLabel(
    form_frame,
    text="Amount *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

amount_label.grid(
    row=4,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


amount_entry = ctk.CTkEntry(
    form_frame,
    width=300,
    height=42,
    placeholder_text="Enter amount (₹)",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

amount_entry.grid(
    row=4,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# --------------------------------------------------
# PLACE
# --------------------------------------------------

place_label = ctk.CTkLabel(
    form_frame,
    text="Place",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

place_label.grid(
    row=5,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


place_entry = ctk.CTkEntry(
    form_frame,
    width=300,
    height=42,
    placeholder_text="Where did you spend?",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

place_entry.grid(
    row=5,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# --------------------------------------------------
# DESCRIPTION
# --------------------------------------------------

description_label = ctk.CTkLabel(
    form_frame,
    text="Description",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

description_label.grid(
    row=6,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


description_entry = ctk.CTkEntry(
    form_frame,
    width=300,
    height=42,
    placeholder_text="Enter a short description",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

description_entry.grid(
    row=6,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# --------------------------------------------------
# DATE
# --------------------------------------------------

date_label = ctk.CTkLabel(
    form_frame,
    text="Expense Date *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

date_label.grid(
    row=7,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


date_entry = ctk.CTkEntry(
    form_frame,
    width=300,
    height=42,
    placeholder_text="DD-MM-YYYY",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

date_entry.grid(
    row=7,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# --------------------------------------------------
# SAVE EXPENSE FUNCTION
# --------------------------------------------------

def save_expense():

    category = category_entry.get().strip()

    payment_method = payment_entry.get().strip()

    amount = amount_entry.get().strip()

    place = place_entry.get().strip()

    description = description_entry.get().strip()

    expense_date = date_entry.get().strip()


    # ----------------------------------------------
    # REQUIRED FIELD VALIDATION
    # ----------------------------------------------

    if (
        category == ""
        or payment_method == ""
        or amount == ""
        or expense_date == ""
    ):

        messagebox.showerror(
            "Missing Information",
            "Please fill all required fields."
        )

        return


    # ----------------------------------------------
    # AMOUNT VALIDATION
    # ----------------------------------------------

    try:

        amount = float(amount)

        if amount <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Amount must be greater than 0."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid numeric amount."
        )

        return


    # ----------------------------------------------
    # DATE VALIDATION
    # ----------------------------------------------

    try:

        formatted_date = datetime.strptime(
            expense_date,
            "%d-%m-%Y"
        ).strftime("%Y-%m-%d")

    except ValueError:

        messagebox.showerror(
            "Invalid Date",
            "Date must be in DD-MM-YYYY format."
        )

        return


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


        # ------------------------------------------
        # GET CATEGORY ID
        # ------------------------------------------

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
                "Selected category was not found."
            )

            return


        category_id = category_result[0]


        # ------------------------------------------
        # GET PAYMENT METHOD ID
        # ------------------------------------------

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
                "Selected payment method was not found."
            )

            return


        payment_method_id = payment_result[0]


        # ------------------------------------------
        # INSERT EXPENSE
        # ------------------------------------------

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
                place if place else None,
                description if description else None
            )
        )


        connection.commit()


        # ------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------

        messagebox.showinfo(
            "Expense Saved",
            "Your expense has been saved successfully!"
        )


        # ------------------------------------------
        # CLEAR FORM
        # ------------------------------------------

        category_entry.set("")

        payment_entry.set("")

        amount_entry.delete(
            0,
            "end"
        )

        place_entry.delete(
            0,
            "end"
        )

        description_entry.delete(
            0,
            "end"
        )

        date_entry.delete(
            0,
            "end"
        )


        # Focus back on category

        category_entry.focus()


    except Exception as e:

        if connection:

            connection.rollback()


        messagebox.showerror(
            "Database Error",
            str(e)
        )


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()


# --------------------------------------------------
# BUTTON FRAME
# --------------------------------------------------

button_frame = ctk.CTkFrame(
    form_frame,
    fg_color="transparent"
)

button_frame.grid(
    row=8,
    column=0,
    columnspan=2,
    padx=35,
    pady=(25, 30)
)


# --------------------------------------------------
# SAVE BUTTON
# --------------------------------------------------

save_button = ctk.CTkButton(
    button_frame,
    text="Save Expense",
    width=220,
    height=45,
    corner_radius=10,
    font=("Arial", 15, "bold"),
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    command=save_expense
)

save_button.grid(
    row=0,
    column=0,
    padx=10
)


# --------------------------------------------------
# BACK BUTTON
# --------------------------------------------------

def go_back():

    from ui.dashboard import open_dashboard

    app.destroy()

    open_dashboard(user_id)


back_button = ctk.CTkButton(
    button_frame,
    text="Back to Dashboard",
    width=220,
    height=45,
    corner_radius=10,
    font=("Arial", 15, "bold"),
    fg_color=INPUT_COLOR,
    hover_color=BORDER_COLOR,
    border_width=1,
    border_color=BORDER_COLOR,
    command=go_back
)

back_button.grid(
    row=0,
    column=1,
    padx=10
)


# --------------------------------------------------
# KEYBOARD SHORTCUT
# --------------------------------------------------

app.bind(
    "<Return>",
    lambda event: save_expense()
)


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.mainloop()