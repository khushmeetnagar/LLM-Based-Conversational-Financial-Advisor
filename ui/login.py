import customtkinter as ctk
import mysql.connector
import bcrypt

from tkinter import messagebox
from database.db_connection import connect_db
from ui.dashboard import app as dashboard_app
from ui.register import open_register_window

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
def login_user():

    user = user_entry.get().strip()
    password = password_entry.get()

    if user == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields!"
        )
        return
    try:
        connection = connect_db()

        if connection is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        cursor = connection.cursor()
        query = """
        SELECT user_id,
               full_name,
               password_hash
        FROM users
        WHERE email = %s
           OR phone_number = %s
        """

        cursor.execute(query, (user, user))

        result = cursor.fetchone()
        if result is None:
            messagebox.showerror(
                "Login Failed",
                "User not found!"
            )
            return
        user_id = result[0]
        full_name = result[1]
        stored_password = result[2]

        if bcrypt.checkpw(password.encode(), stored_password.encode()):
            messagebox.showinfo(
                "Success",
                f"Welcome {full_name}"
            )

            app.destroy()  # Login window close
            dashboard_app.mainloop()  # Dashboard window open

        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect Password!"
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



def open_register():
    app.destroy()
    open_register_window()

app = ctk.CTk()
app.title("LLM-Based Conversational Financial Advisor")
app.geometry("700x500")

title = ctk.CTkLabel(
    app,
    text="Welcome Back",
    font=("Arial", 28, "bold")
)
title.pack(pady=30)
login_frame = ctk.CTkFrame(app, width=450, height=250)
login_frame.pack(pady=20)

login_frame.pack_propagate(False)
user_label = ctk.CTkLabel(
    login_frame,
    text="Email / Phone Number",
    font=("Arial", 16)
)
user_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

user_entry = ctk.CTkEntry(
    login_frame,
    width=250,
    placeholder_text="Enter email or phone number"
)
user_entry.grid(row=0, column=1, padx=20, pady=20)
password_label = ctk.CTkLabel(
    login_frame,
    text="Password",
    font=("Arial", 16)
)
password_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")

password_entry = ctk.CTkEntry(
    login_frame,
    width=250,
    show="*",
    placeholder_text="Enter password"
)
password_entry.grid(row=1, column=1, padx=20, pady=20)
login_button = ctk.CTkButton(
    login_frame,
    text="Login",
    width=180,
    command=login_user
)

login_button.grid(row=2, column=0, columnspan=2, pady=30)
register_button = ctk.CTkButton(
    login_frame,
    text="Create New Account",
    width=180,
    command=open_register
)

register_button.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10
)
def open_login():
    app.mainloop()
