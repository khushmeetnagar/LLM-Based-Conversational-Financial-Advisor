import customtkinter as ctk
import mysql.connector
from database.db_connection import connect_db
from tkinter import messagebox
from datetime import datetime
import bcrypt

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
def register_user():

    full_name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    dob = dob_entry.get()
    try:
        formatted_dob = datetime.strptime(dob, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Error",
            "Date of Birth must be in DD-MM-YYYY format."
        )
        return
    income = income_entry.get()
    savings = savings_entry.get()

    # Validation
    if (
        full_name == "" or
        email == "" or
        phone == "" or
        password == "" or
        confirm_password == "" or
        dob == "" or
        income == "" or
        savings == ""
    ):
        messagebox.showerror("Error", "All fields are required!")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()
    try:
        connection = connect_db()

        if connection is None:
            messagebox.showerror("Error", "Database connection failed!")
            return

        cursor = connection.cursor()

        query = """
        INSERT INTO users
        (full_name, email, phone_number, password_hash, date_of_birth, monthly_income, monthly_savings)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                full_name,
                email,
                phone,
                hashed_password,
                formatted_dob,
                income,
                savings
            )
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Registration Successful!"
        )
        name_entry.delete(0, "end")
        email_entry.delete(0, "end")
        phone_entry.delete(0, "end")
        password_entry.delete(0, "end")
        confirm_password_entry.delete(0, "end")
        dob_entry.delete(0, "end")
        income_entry.delete(0, "end")
        savings_entry.delete(0, "end")

    except mysql.connector.IntegrityError:
        messagebox.showerror(
            "Registration Failed",
            "Email or Phone Number already exists."
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:
        if connection:
            cursor.close()
            connection.close()


app = ctk.CTk()
app.title("LLM-Based Conversational Financial Advisor")
app.geometry("900x600")

title = ctk.CTkLabel(
    app,
    text="User Registration",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)
# Registration Frame
form_frame = ctk.CTkFrame(app, width=500, height=450)
form_frame.pack(pady=20)

form_frame.pack_propagate(False)
name_label = ctk.CTkLabel(
    form_frame,
    text="Full Name",
    font=("Arial", 16)
)
name_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

name_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter your full name"
)
name_entry.grid(row=0, column=1, padx=20, pady=15)
email_label = ctk.CTkLabel(
    form_frame,
    text="Email",
    font=("Arial", 16)
)
email_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")

email_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter your email"
)
email_entry.grid(row=1, column=1, padx=20, pady=15)
phone_label = ctk.CTkLabel(
    form_frame,
    text="Phone Number",
    font=("Arial", 16)
)
phone_label.grid(row=2, column=0, padx=20, pady=15, sticky="w")

phone_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter your phone number"
)
phone_entry.grid(row=2, column=1, padx=20, pady=15)
password_label = ctk.CTkLabel(
    form_frame,
    text="Password",
    font=("Arial", 16)
)
password_label.grid(row=3, column=0, padx=20, pady=15, sticky="w")

password_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    show="*",
    placeholder_text="Enter password"
)
password_entry.grid(row=3, column=1, padx=20, pady=15)
confirm_password_label = ctk.CTkLabel(
    form_frame,
    text="Confirm Password",
    font=("Arial", 16)
)
confirm_password_label.grid(row=4, column=0, padx=20, pady=15, sticky="w")

confirm_password_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    show="*",
    placeholder_text="Confirm password"
)
confirm_password_entry.grid(row=4, column=1, padx=20, pady=15)
dob_label = ctk.CTkLabel(
    form_frame,
    text="Date of Birth",
    font=("Arial", 16)
)
dob_label.grid(row=5, column=0, padx=20, pady=15, sticky="w")

dob_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="DD-MM-YYYY"
)
dob_entry.grid(row=5, column=1, padx=20, pady=15)
income_label = ctk.CTkLabel(
    form_frame,
    text="Monthly Income",
    font=("Arial", 16)
)
income_label.grid(row=6, column=0, padx=20, pady=15, sticky="w")

income_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter monthly income"
)
income_entry.grid(row=6, column=1, padx=20, pady=15)
savings_label = ctk.CTkLabel(
    form_frame,
    text="Monthly Savings",
    font=("Arial", 16)
)
savings_label.grid(row=7, column=0, padx=20, pady=15, sticky="w")

savings_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter monthly savings"
)
savings_entry.grid(row=7, column=1, padx=20, pady=15)
register_button = ctk.CTkButton(
    form_frame,
    text="Register",
    width=180,
    command=register_user
)

register_button.grid(row=8, column=0, columnspan=2, pady=30)
def open_register_window():
    app.mainloop()

