import customtkinter as ctk
import mysql.connector
from database.db_connection import connect_db
from tkinter import messagebox
from datetime import datetime
import bcrypt
from ui.navigation import open_login


# =========================================================
# APPEARANCE
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# REGISTER USER
# =========================================================

def register_user():
    print("REGISTER BUTTON CLICKED")

    # Get values
    full_name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    dob = dob_entry.get().strip()
    income = income_entry.get().strip()
    savings = savings_entry.get().strip()

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    fields = {
        "Full Name": full_name,
        "Email": email,
        "Phone": phone,
        "Password": password,
        "Confirm Password": confirm_password,
        "Date of Birth": dob,
        "Monthly Income": income,
        "Monthly Savings": savings
    }

    empty_fields = [
        field_name
        for field_name, value in fields.items()
        if value == ""
    ]

    if empty_fields:
        messagebox.showerror(
            "Error",
            "Please fill these fields:\n\n" + "\n".join(empty_fields)
        )
        return

    # Password confirmation
    if password != confirm_password:
        messagebox.showerror(
            "Error",
            "Passwords do not match!"
        )
        return

    # -----------------------------------------------------
    # DATE VALIDATION
    # -----------------------------------------------------

    try:

        formatted_dob = datetime.strptime(
            dob,
            "%d-%m-%Y"
        ).strftime("%Y-%m-%d")

    except ValueError:

        messagebox.showerror(
            "Error",
            "Date of Birth must be in DD-MM-YYYY format."
        )

        return

    # -----------------------------------------------------
    # INCOME VALIDATION
    # -----------------------------------------------------

    try:

        income_value = float(income)

        if income_value <= 0:
            messagebox.showerror(
                "Error",
                "Monthly income must be greater than 0."
            )
            return

    except ValueError:

        messagebox.showerror(
            "Error",
            "Monthly income must be a valid number."
        )

        return

    # -----------------------------------------------------
    # SAVINGS VALIDATION
    # -----------------------------------------------------

    try:

        savings_value = float(savings)

        if savings_value < 0:
            messagebox.showerror(
                "Error",
                "Monthly savings cannot be negative."
            )
            return

        if savings_value > income_value:
            messagebox.showerror(
                "Error",
                "Monthly savings cannot be greater than income."
            )
            return

    except ValueError:

        messagebox.showerror(
            "Error",
            "Monthly savings must be a valid number."
        )

        return

    # -----------------------------------------------------
    # HASH PASSWORD
    # -----------------------------------------------------

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # -----------------------------------------------------
    # DATABASE VARIABLES
    # -----------------------------------------------------

    connection = None
    cursor = None

    # -----------------------------------------------------
    # DATABASE INSERT
    # -----------------------------------------------------

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
        INSERT INTO users
        (
            full_name,
            email,
            phone_number,
            password_hash,
            date_of_birth,
            monthly_income,
            monthly_savings
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            full_name,
            email,
            phone,
            hashed_password,
            formatted_dob,
            income_value,
            savings_value
        )

        cursor.execute(
            query,
            values
        )

        # VERY IMPORTANT
        connection.commit()

        # Get newly created user ID
        new_user_id = cursor.lastrowid

        print("--------------------------------")
        print("REGISTRATION SUCCESS")
        print("New User ID:", new_user_id)
        print("Name:", full_name)
        print("Email:", email)
        print("Phone:", phone)
        print("--------------------------------")

        messagebox.showinfo(
            "Success",
            f"Registration Successful!\n\n"
            f"Your User ID is: {new_user_id}"
        )

        # -------------------------------------------------
        # CLEAR FORM
        # -------------------------------------------------

        name_entry.delete(0, "end")
        email_entry.delete(0, "end")
        phone_entry.delete(0, "end")
        password_entry.delete(0, "end")
        confirm_password_entry.delete(0, "end")
        dob_entry.delete(0, "end")
        income_entry.delete(0, "end")
        savings_entry.delete(0, "end")

        # -------------------------------------------------
        # GO TO LOGIN
        # -------------------------------------------------

        app.destroy()
        open_login()

    except mysql.connector.IntegrityError as e:

        print("INTEGRITY ERROR:", repr(e))

        messagebox.showerror(
            "Registration Failed",
            "Email or Phone Number already exists."
        )

    except mysql.connector.Error as e:

        print("MYSQL ERROR:", repr(e))

        messagebox.showerror(
            "Database Error",
            f"MySQL Error:\n{e}"
        )

    except Exception as e:

        print("REGISTER ERROR:", repr(e))

        messagebox.showerror(
            "Registration Error",
            f"Something went wrong:\n{e}"
        )

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# =========================================================
# MAIN WINDOW
# =========================================================

app = ctk.CTk()

app.title(
    "LLM-Based Conversational Financial Advisor"
)

app.geometry("900x650")


# =========================================================
# TITLE
# =========================================================

title = ctk.CTkLabel(
    app,
    text="User Registration",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# =========================================================
# FORM FRAME
# =========================================================

form_frame = ctk.CTkFrame(
    app,
    width=550,
    height=500
)

form_frame.pack(pady=10)

form_frame.pack_propagate(False)


# =========================================================
# FULL NAME
# =========================================================

name_label = ctk.CTkLabel(
    form_frame,
    text="Full Name",
    font=("Arial", 16)
)

name_label.grid(
    row=0,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

name_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter your full name"
)

name_entry.grid(
    row=0,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# EMAIL
# =========================================================

email_label = ctk.CTkLabel(
    form_frame,
    text="Email",
    font=("Arial", 16)
)

email_label.grid(
    row=1,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

email_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter your email"
)

email_entry.grid(
    row=1,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# PHONE
# =========================================================

phone_label = ctk.CTkLabel(
    form_frame,
    text="Phone Number",
    font=("Arial", 16)
)

phone_label.grid(
    row=2,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

phone_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter phone number"
)

phone_entry.grid(
    row=2,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# PASSWORD
# =========================================================

password_label = ctk.CTkLabel(
    form_frame,
    text="Password",
    font=("Arial", 16)
)

password_label.grid(
    row=3,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

password_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    show="*",
    placeholder_text="Enter password"
)

password_entry.grid(
    row=3,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# CONFIRM PASSWORD
# =========================================================

confirm_password_label = ctk.CTkLabel(
    form_frame,
    text="Confirm Password",
    font=("Arial", 16)
)

confirm_password_label.grid(
    row=4,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

confirm_password_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    show="*",
    placeholder_text="Confirm password"
)

confirm_password_entry.grid(
    row=4,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# DATE OF BIRTH
# =========================================================

dob_label = ctk.CTkLabel(
    form_frame,
    text="Date of Birth",
    font=("Arial", 16)
)

dob_label.grid(
    row=5,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

dob_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="DD-MM-YYYY"
)

dob_entry.grid(
    row=5,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# MONTHLY INCOME
# =========================================================

income_label = ctk.CTkLabel(
    form_frame,
    text="Monthly Income",
    font=("Arial", 16)
)

income_label.grid(
    row=6,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

income_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter monthly income"
)

income_entry.grid(
    row=6,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# MONTHLY SAVINGS
# =========================================================

savings_label = ctk.CTkLabel(
    form_frame,
    text="Monthly Savings",
    font=("Arial", 16)
)

savings_label.grid(
    row=7,
    column=0,
    padx=20,
    pady=12,
    sticky="w"
)

savings_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter monthly savings"
)

savings_entry.grid(
    row=7,
    column=1,
    padx=20,
    pady=12
)


# =========================================================
# REGISTER BUTTON
# =========================================================

register_button = ctk.CTkButton(
    form_frame,
    text="Register",
    width=180,
    height=40,
    command=register_user
)

register_button.grid(
    row=8,
    column=0,
    columnspan=2,
    pady=25
)


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    print("REGISTER WINDOW STARTED")
    app.mainloop()
    print("REGISTER WINDOW CLOSED")