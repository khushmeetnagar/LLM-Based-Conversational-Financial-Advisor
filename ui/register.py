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
# COLORS
# =========================================================

BG_COLOR = "#0B1120"
CARD_COLOR = "#111827"
INPUT_COLOR = "#1F2937"
TEXT_COLOR = "#F9FAFB"
SECONDARY_TEXT = "#9CA3AF"
ACCENT_COLOR = "#2563EB"
ACCENT_HOVER = "#1D4ED8"
BORDER_COLOR = "#374151"
SUCCESS_COLOR = "#22C55E"


# =========================================================
# REGISTER USER
# =========================================================

def register_user():

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
    # REQUIRED FIELDS
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
            "Missing Information",
            "Please fill these fields:\n\n" +
            "\n".join(empty_fields)
        )
        return


    # -----------------------------------------------------
    # PASSWORD CONFIRMATION
    # -----------------------------------------------------

    if password != confirm_password:
        messagebox.showerror(
            "Password Error",
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
            "Invalid Date",
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
                "Invalid Income",
                "Monthly income must be greater than 0."
            )
            return

    except ValueError:

        messagebox.showerror(
            "Invalid Income",
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
                "Invalid Savings",
                "Monthly savings cannot be negative."
            )
            return

        if savings_value > income_value:
            messagebox.showerror(
                "Invalid Savings",
                "Monthly savings cannot be greater than income."
            )
            return

    except ValueError:

        messagebox.showerror(
            "Invalid Savings",
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

        cursor.execute(query, values)

        connection.commit()

        new_user_id = cursor.lastrowid

        print("--------------------------------")
        print("REGISTRATION SUCCESS")
        print("New User ID:", new_user_id)
        print("Name:", full_name)
        print("Email:", email)
        print("Phone:", phone)
        print("--------------------------------")

        messagebox.showinfo(
            "Account Created",
            f"Registration Successful!\n\n"
            f"Welcome, {full_name}!\n\n"
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
# BACK TO LOGIN
# =========================================================

def go_to_login():

    app.destroy()
    open_login()


# =========================================================
# MAIN WINDOW
# =========================================================

app = ctk.CTk()

app.title(
    "LLM-Based Conversational Financial Advisor"
)

app.geometry("1100x720")
app.minsize(850, 600)

app.configure(
    fg_color=BG_COLOR
)


# =========================================================
# MAIN CONTAINER
# =========================================================

main_frame = ctk.CTkFrame(
    app,
    fg_color=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=20
)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)


# =========================================================
# LEFT BRANDING SECTION
# =========================================================

left_frame = ctk.CTkFrame(
    main_frame,
    fg_color=BG_COLOR,
    corner_radius=0
)

left_frame.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(15, 25),
    pady=10
)


# ---------------------------------------------------------
# LOGO
# ---------------------------------------------------------

logo = ctk.CTkLabel(
    left_frame,
    text="💰",
    font=("Segoe UI Emoji", 50)
)

logo.pack(
    pady=(50, 12)
)


# ---------------------------------------------------------
# APP NAME
# ---------------------------------------------------------

brand_title = ctk.CTkLabel(
    left_frame,
    text="FinVest AI",
    font=("Arial", 34, "bold"),
    text_color=TEXT_COLOR
)

brand_title.pack(
    pady=(0, 8)
)


# ---------------------------------------------------------
# TAGLINE
# ---------------------------------------------------------

brand_subtitle = ctk.CTkLabel(
    left_frame,
    text="Your Smart Financial Companion",
    font=("Arial", 16, "bold"),
    text_color=ACCENT_COLOR
)

brand_subtitle.pack(
    pady=(0, 22)
)


# ---------------------------------------------------------
# DESCRIPTION
# ---------------------------------------------------------

description = ctk.CTkLabel(
    left_frame,
    text=(
        "Create your account and take control\n"
        "of your financial journey.\n\n"
        "Track expenses, manage goals and get\n"
        "AI-powered financial guidance."
    ),
    font=("Arial", 14),
    text_color=SECONDARY_TEXT,
    justify="center"
)

description.pack(
    pady=8
)


# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------

features_frame = ctk.CTkFrame(
    left_frame,
    fg_color=CARD_COLOR,
    corner_radius=16,
    border_width=1,
    border_color=BORDER_COLOR
)

features_frame.pack(
    fill="x",
    padx=10,
    pady=35
)


features_title = ctk.CTkLabel(
    features_frame,
    text="Why create an account?",
    font=("Arial", 15, "bold"),
    text_color=TEXT_COLOR
)

features_title.pack(
    anchor="w",
    padx=18,
    pady=(16, 10)
)


features = [
    "✓  Track your daily expenses",
    "✓  Set and monitor investment goals",
    "✓  Analyze your financial habits",
    "✓  Get personalized AI guidance"
]

for feature in features:

    label = ctk.CTkLabel(
        features_frame,
        text=feature,
        font=("Arial", 13),
        text_color=SECONDARY_TEXT,
        anchor="w"
    )

    label.pack(
        anchor="w",
        padx=18,
        pady=5
    )


ctk.CTkLabel(
    features_frame,
    text="",
    height=8
).pack()


# =========================================================
# RIGHT REGISTRATION CARD
# =========================================================

right_frame = ctk.CTkFrame(
    main_frame,
    fg_color=CARD_COLOR,
    corner_radius=20,
    border_width=1,
    border_color=BORDER_COLOR
)

right_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(5, 5),
    pady=0
)


# =========================================================
# REGISTRATION HEADER
# =========================================================

register_title = ctk.CTkLabel(
    right_frame,
    text="Create Account",
    font=("Arial", 27, "bold"),
    text_color=TEXT_COLOR
)

register_title.pack(
    pady=(20, 3)
)


register_subtitle = ctk.CTkLabel(
    right_frame,
    text="Start your smarter financial journey",
    font=("Arial", 12),
    text_color=SECONDARY_TEXT
)

register_subtitle.pack(
    pady=(0, 12)
)


# =========================================================
# SCROLLABLE FORM
# =========================================================

scroll_container = ctk.CTkScrollableFrame(
    right_frame,
    fg_color="transparent",
    scrollbar_fg_color=CARD_COLOR,
    scrollbar_button_color=BORDER_COLOR,
    scrollbar_button_hover_color=ACCENT_COLOR
)

scroll_container.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=(0, 10)
)


# =========================================================
# FORM
# =========================================================

form_frame = ctk.CTkFrame(
    scroll_container,
    fg_color="transparent"
)

form_frame.pack(
    fill="x",
    padx=15,
    pady=5
)


# =========================================================
# FULL NAME
# =========================================================

name_label = ctk.CTkLabel(
    form_frame,
    text="Full Name",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

name_label.pack(
    fill="x",
    pady=(5, 4)
)


name_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="Enter your full name",
    text_color=TEXT_COLOR
)

name_entry.pack(
    fill="x",
    pady=(0, 9)
)


# =========================================================
# EMAIL
# =========================================================

email_label = ctk.CTkLabel(
    form_frame,
    text="Email Address",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

email_label.pack(
    fill="x",
    pady=(5, 4)
)


email_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="Enter your email",
    text_color=TEXT_COLOR
)

email_entry.pack(
    fill="x",
    pady=(0, 9)
)


# =========================================================
# PHONE
# =========================================================

phone_label = ctk.CTkLabel(
    form_frame,
    text="Phone Number",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

phone_label.pack(
    fill="x",
    pady=(5, 4)
)


phone_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="Enter phone number",
    text_color=TEXT_COLOR
)

phone_entry.pack(
    fill="x",
    pady=(0, 9)
)


# =========================================================
# PASSWORD
# =========================================================

password_label = ctk.CTkLabel(
    form_frame,
    text="Password",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

password_label.pack(
    fill="x",
    pady=(5, 4)
)


password_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="Create a password",
    show="*",
    text_color=TEXT_COLOR
)

password_entry.pack(
    fill="x",
    pady=(0, 9)
)


# =========================================================
# CONFIRM PASSWORD
# =========================================================

confirm_password_label = ctk.CTkLabel(
    form_frame,
    text="Confirm Password",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

confirm_password_label.pack(
    fill="x",
    pady=(5, 4)
)


confirm_password_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="Confirm your password",
    show="*",
    text_color=TEXT_COLOR
)

confirm_password_entry.pack(
    fill="x",
    pady=(0, 9)
)


# =========================================================
# DATE OF BIRTH
# =========================================================

dob_label = ctk.CTkLabel(
    form_frame,
    text="Date of Birth",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

dob_label.pack(
    fill="x",
    pady=(5, 4)
)


dob_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="DD-MM-YYYY",
    text_color=TEXT_COLOR
)

dob_entry.pack(
    fill="x",
    pady=(0, 9)
)


# =========================================================
# MONTHLY INCOME
# =========================================================

income_label = ctk.CTkLabel(
    form_frame,
    text="Monthly Income",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

income_label.pack(
    fill="x",
    pady=(5, 4)
)


income_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="Enter monthly income",
    text_color=TEXT_COLOR
)

income_entry.pack(
    fill="x",
    pady=(0, 9)
)


# =========================================================
# MONTHLY SAVINGS
# =========================================================

savings_label = ctk.CTkLabel(
    form_frame,
    text="Monthly Savings",
    font=("Arial", 13, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

savings_label.pack(
    fill="x",
    pady=(5, 4)
)


savings_entry = ctk.CTkEntry(
    form_frame,
    height=38,
    corner_radius=8,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    placeholder_text="Enter monthly savings",
    text_color=TEXT_COLOR
)

savings_entry.pack(
    fill="x",
    pady=(0, 14)
)


# =========================================================
# CREATE ACCOUNT BUTTON
# =========================================================

register_button = ctk.CTkButton(
    form_frame,
    text="Create Account",
    height=42,
    corner_radius=8,
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    font=("Arial", 14, "bold"),
    command=register_user
)

register_button.pack(
    fill="x",
    pady=(2, 10)
)


# =========================================================
# LOGIN BUTTON
# =========================================================

login_button = ctk.CTkButton(
    form_frame,
    text="Already have an account?  Login",
    height=36,
    corner_radius=8,
    fg_color="transparent",
    hover_color=INPUT_COLOR,
    border_width=1,
    border_color=BORDER_COLOR,
    text_color=SECONDARY_TEXT,
    font=("Arial", 12),
    command=go_to_login
)

login_button.pack(
    fill="x",
    pady=(0, 15)
)


# =========================================================
# KEYBOARD SUPPORT
# =========================================================

app.bind(
    "<Return>",
    lambda event: register_user()
)


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    print("REGISTER WINDOW STARTED")

    app.mainloop()

    print("REGISTER WINDOW CLOSED")