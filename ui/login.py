import customtkinter as ctk
import bcrypt
from tkinter import messagebox

from database.db_connection import connect_db
from ui.navigation import open_register, open_dashboard


# ---------------- APPEARANCE ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- LOGIN FUNCTION ----------------

def login_user():

    user = user_entry.get().strip()
    password = password_entry.get()

    if user == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields!"
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

        query = """
        SELECT
            user_id,
            full_name,
            password_hash
        FROM users
        WHERE email = %s
           OR phone_number = %s
        """

        cursor.execute(
            query,
            (user, user)
        )

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

        # Convert stored password hash to bytes
        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        # Verify password
        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):

            messagebox.showinfo(
                "Success",
                f"Welcome {full_name}!"
            )

            print("LOGIN SUCCESS")
            print("USER ID:", user_id)

            open_dashboard(user_id)
            app.destroy()

            print("DASHBOARD COMMAND SENT")

            app.destroy()

        else:

            messagebox.showerror(
                "Login Failed",
                "Incorrect Password!"
            )

    except Exception as e:

        print("LOGIN ERROR:", repr(e))

        messagebox.showerror(
            "Login Error",
            repr(e)
        )

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ---------------- REGISTER BUTTON ----------------

def go_to_register():
    open_register()


# ---------------- OPEN LOGIN ----------------

def open_login():

    app.mainloop()


# ---------------- APPLICATION ----------------

app = ctk.CTk()

app.title(
    "LLM-Based Conversational Financial Advisor"
)

app.geometry("700x500")


# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    app,
    text="Welcome Back",
    font=("Arial", 28, "bold")
)

title.pack(pady=30)


# ---------------- LOGIN FRAME ----------------

login_frame = ctk.CTkFrame(
    app,
    width=450,
    height=250
)

login_frame.pack(pady=20)

login_frame.pack_propagate(False)


# ---------------- USER LABEL ----------------

user_label = ctk.CTkLabel(
    login_frame,
    text="Email / Phone Number",
    font=("Arial", 16)
)

user_label.grid(
    row=0,
    column=0,
    padx=20,
    pady=20,
    sticky="w"
)


# ---------------- USER ENTRY ----------------

user_entry = ctk.CTkEntry(
    login_frame,
    width=250,
    placeholder_text="Enter email or phone number"
)

user_entry.grid(
    row=0,
    column=1,
    padx=20,
    pady=20
)


# ---------------- PASSWORD LABEL ----------------

password_label = ctk.CTkLabel(
    login_frame,
    text="Password",
    font=("Arial", 16)
)

password_label.grid(
    row=1,
    column=0,
    padx=20,
    pady=20,
    sticky="w"
)


# ---------------- PASSWORD ENTRY ----------------

password_entry = ctk.CTkEntry(
    login_frame,
    width=250,
    show="*",
    placeholder_text="Enter password"
)

password_entry.grid(
    row=1,
    column=1,
    padx=20,
    pady=20
)


# ---------------- LOGIN BUTTON ----------------

login_button = ctk.CTkButton(
    login_frame,
    text="Login",
    width=180,
    command=login_user
)

login_button.grid(
    row=2,
    column=0,
    columnspan=2,
    pady=30
)


# ---------------- REGISTER BUTTON ----------------

register_button = ctk.CTkButton(
    login_frame,
    text="Create New Account",
    width=180,
    command=go_to_register
)

register_button.grid(
    row=3,
    column=0,
    columnspan=2,
    pady=10
)


# ---------------- START LOGIN ----------------

if __name__ == "__main__":
    open_login()