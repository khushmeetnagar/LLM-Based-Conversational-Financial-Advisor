import customtkinter as ctk
import bcrypt
from tkinter import messagebox

from database.db_connection import connect_db
from ui.navigation import open_register, open_dashboard


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


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login_user():

    user = user_entry.get().strip()
    password = password_entry.get()

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if user == "" or password == "":
        messagebox.showerror(
            "Missing Information",
            "Please fill in all fields."
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

        # -------------------------------------------------
        # FIND USER
        # -------------------------------------------------

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
                "No account found with this email or phone number."
            )

            return

        user_id = result[0]
        full_name = result[1]
        stored_password = result[2]

        # -------------------------------------------------
        # PASSWORD HASH
        # -------------------------------------------------

        if isinstance(stored_password, str):
            stored_password = stored_password.encode("utf-8")

        # -------------------------------------------------
        # VERIFY PASSWORD
        # -------------------------------------------------

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):

            print("LOGIN SUCCESS")
            print("USER ID:", user_id)

            messagebox.showinfo(
                "Login Successful",
                f"Welcome back, {full_name}! 👋"
            )

            # Open dashboard first
            open_dashboard(user_id)

            # Destroy login window
            app.destroy()

        else:

            messagebox.showerror(
                "Login Failed",
                "Incorrect password. Please try again."
            )

    except Exception as e:

        print("LOGIN ERROR:", repr(e))

        messagebox.showerror(
            "Login Error",
            f"Something went wrong:\n\n{e}"
        )

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# =========================================================
# GO TO REGISTER
# =========================================================

def go_to_register():
    print("CREATE ACCOUNT CLICKED")
    open_register()


# =========================================================
# OPEN LOGIN
# =========================================================

def open_login():

    app.mainloop()


# =========================================================
# APPLICATION WINDOW
# =========================================================

app = ctk.CTk()

app.title(
    "FinVest AI - Login"
)

app.geometry(
    "1000x650"
)

app.configure(
    fg_color=BG_COLOR
)

app.resizable(
    False,
    False
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
    expand=True
)


# =========================================================
# LEFT SIDE - BRANDING
# =========================================================

left_frame = ctk.CTkFrame(
    main_frame,
    width=470,
    fg_color=BG_COLOR
)

left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(45, 20),
    pady=45
)

left_frame.pack_propagate(False)


# ---------------------------------------------------------
# LOGO
# ---------------------------------------------------------

logo = ctk.CTkLabel(
    left_frame,
    text="💰",
    font=("Arial", 55)
)

logo.pack(
    pady=(70, 10)
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
    text="Your Personal Financial Assistant",
    font=("Arial", 17),
    text_color=SECONDARY_TEXT
)

brand_subtitle.pack(
    pady=5
)


# ---------------------------------------------------------
# DESCRIPTION
# ---------------------------------------------------------

description = ctk.CTkLabel(
    left_frame,
    text=(
        "Track your expenses,\n"
        "manage your financial goals,\n"
        "and get AI-powered financial guidance."
    ),
    font=("Arial", 15),
    text_color=SECONDARY_TEXT,
    justify="center"
)

description.pack(
    pady=30
)


# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------

features = ctk.CTkLabel(
    left_frame,
    text=(
        "✓ Expense Tracking\n"
        "✓ Investment Goals\n"
        "✓ Financial Analytics\n"
        "✓ AI Financial Advisor"
    ),
    font=("Arial", 14),
    text_color=TEXT_COLOR,
    justify="left"
)

features.pack(
    pady=10
)


# =========================================================
# RIGHT SIDE - LOGIN CARD
# =========================================================

card = ctk.CTkFrame(
    main_frame,
    width=430,
    height=500,
    fg_color=CARD_COLOR,
    corner_radius=20,
    border_width=1,
    border_color=BORDER_COLOR
)

card.pack(
    side="right",
    padx=(20, 55),
    pady=75
)

card.pack_propagate(False)


# =========================================================
# LOGIN TITLE
# =========================================================

login_title = ctk.CTkLabel(
    card,
    text="Welcome Back 👋",
    font=("Arial", 27, "bold"),
    text_color=TEXT_COLOR
)

login_title.pack(
    pady=(38, 5)
)


# =========================================================
# LOGIN SUBTITLE
# =========================================================

login_subtitle = ctk.CTkLabel(
    card,
    text="Login to continue to your financial dashboard",
    font=("Arial", 13),
    text_color=SECONDARY_TEXT
)

login_subtitle.pack(
    pady=(0, 28)
)


# =========================================================
# USER LABEL
# =========================================================

user_label = ctk.CTkLabel(
    card,
    text="Email or Phone Number",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

user_label.pack(
    fill="x",
    padx=45,
    pady=(0, 7)
)


# =========================================================
# USER ENTRY
# =========================================================

user_entry = ctk.CTkEntry(
    card,
    width=330,
    height=45,
    corner_radius=10,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    text_color=TEXT_COLOR,
    placeholder_text="Enter email or phone number",
    placeholder_text_color="#6B7280",
    font=("Arial", 13)
)

user_entry.pack(
    padx=45,
    pady=(0, 20)
)


# =========================================================
# PASSWORD LABEL
# =========================================================

password_label = ctk.CTkLabel(
    card,
    text="Password",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

password_label.pack(
    fill="x",
    padx=45,
    pady=(0, 7)
)


# =========================================================
# PASSWORD ENTRY
# =========================================================

password_entry = ctk.CTkEntry(
    card,
    width=330,
    height=45,
    corner_radius=10,
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    border_width=1,
    text_color=TEXT_COLOR,
    placeholder_text="Enter your password",
    placeholder_text_color="#6B7280",
    show="*",
    font=("Arial", 13)
)

password_entry.pack(
    padx=45,
    pady=(0, 25)
)


# =========================================================
# LOGIN BUTTON
# =========================================================

login_button = ctk.CTkButton(
    card,
    text="Login →",
    width=330,
    height=46,
    corner_radius=10,
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    text_color="white",
    font=("Arial", 15, "bold"),
    command=login_user
)

login_button.pack(
    padx=45,
    pady=5
)


# =========================================================
# DIVIDER TEXT
# =========================================================

account_label = ctk.CTkLabel(
    card,
    text="Don't have an account?",
    font=("Arial", 13),
    text_color=SECONDARY_TEXT
)

account_label.pack(
    pady=(28, 5)
)


# =========================================================
# CREATE ACCOUNT BUTTON
# =========================================================

register_button = ctk.CTkButton(
    card,
    text="Create New Account",
    width=330,
    height=42,
    corner_radius=10,
    fg_color="transparent",
    hover_color=INPUT_COLOR,
    border_width=1,
    border_color=ACCENT_COLOR,
    text_color="#60A5FA",
    font=("Arial", 14, "bold"),
    command=go_to_register
)

register_button.pack(
    padx=45,
    pady=5
)


# =========================================================
# FOOTER
# =========================================================

footer = ctk.CTkLabel(
    app,
    text="Secure • Smart • Personalized Financial Planning",
    font=("Arial", 11),
    text_color="#6B7280"
)

footer.place(
    relx=0.5,
    rely=0.965,
    anchor="center"
)


# =========================================================
# ENTER KEY LOGIN
# =========================================================

app.bind(
    "<Return>",
    lambda event: login_user()
)


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    open_login()