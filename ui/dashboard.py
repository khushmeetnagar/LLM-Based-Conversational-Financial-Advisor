import customtkinter as ctk
import sys
from database.db_connection import connect_db
from ui.navigation import (
    open_add_expense,
    open_view_expenses,
    open_analytics,
    open_goals,
    open_ai_advisor
)
from tkinter import messagebox


# =========================================================
# USER ID
# =========================================================

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1


# =========================================================
# APPEARANCE
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# APP
# =========================================================

app = ctk.CTk()

app.title("Financial Advisor Dashboard")
app.geometry("1100x780")
app.minsize(1000, 700)


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#111827"
HEADER_COLOR = "#172033"
CARD_COLOR = "#1B2638"
CARD_HOVER = "#243249"
ACCENT_COLOR = "#3B82F6"
SUCCESS_COLOR = "#22C55E"
DANGER_COLOR = "#EF4444"
TEXT_COLOR = "#F9FAFB"
SECONDARY_TEXT = "#9CA3AF"


# =========================================================
# MAIN CONTAINER
# =========================================================

main_frame = ctk.CTkFrame(
    app,
    fg_color=BG_COLOR,
    corner_radius=0
)

main_frame.pack(
    fill="both",
    expand=True
)


# =========================================================
# HEADER
# =========================================================

header_frame = ctk.CTkFrame(
    main_frame,
    height=80,
    fg_color=HEADER_COLOR,
    corner_radius=0
)

header_frame.pack(
    fill="x"
)

header_frame.pack_propagate(False)


# ---------------- LOGO / TITLE ----------------

brand_frame = ctk.CTkFrame(
    header_frame,
    fg_color="transparent"
)

brand_frame.pack(
    side="left",
    padx=30
)


brand_label = ctk.CTkLabel(
    brand_frame,
    text="💰  Financial Advisor",
    font=("Arial", 23, "bold"),
    text_color=TEXT_COLOR
)

brand_label.pack(
    pady=8
)


brand_subtitle = ctk.CTkLabel(
    brand_frame,
    text="Smart financial planning",
    font=("Arial", 11),
    text_color=SECONDARY_TEXT
)

brand_subtitle.pack()


# ---------------- WELCOME ----------------

welcome_label = ctk.CTkLabel(
    header_frame,
    text="Welcome, User 👋",
    font=("Arial", 16, "bold"),
    text_color=TEXT_COLOR
)

welcome_label.pack(
    side="right",
    padx=35
)


# =========================================================
# CONTENT AREA
# =========================================================

content_frame = ctk.CTkFrame(
    main_frame,
    fg_color=BG_COLOR,
    corner_radius=0
)

content_frame.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=25
)


# =========================================================
# SECTION TITLE
# =========================================================

overview_title = ctk.CTkLabel(
    content_frame,
    text="Financial Overview",
    font=("Arial", 22, "bold"),
    text_color=TEXT_COLOR
)

overview_title.pack(
    anchor="w",
    pady=(0, 15)
)


# =========================================================
# SUMMARY CARDS
# =========================================================

summary_frame = ctk.CTkFrame(
    content_frame,
    fg_color="transparent"
)

summary_frame.pack(
    fill="x"
)


for column in range(4):
    summary_frame.grid_columnconfigure(
        column,
        weight=1
    )


# =========================================================
# CARD CREATION FUNCTION
# =========================================================

def create_summary_card(
    parent,
    column,
    title,
    icon,
    value,
    icon_color
):

    card = ctk.CTkFrame(
        parent,
        height=125,
        fg_color=CARD_COLOR,
        corner_radius=15
    )

    card.grid(
        row=0,
        column=column,
        padx=7,
        sticky="nsew"
    )

    card.grid_propagate(False)


    # ---------------- TOP ----------------

    top_frame = ctk.CTkFrame(
        card,
        fg_color="transparent"
    )

    top_frame.pack(
        fill="x",
        padx=18,
        pady=(15, 5)
    )


    icon_label = ctk.CTkLabel(
        top_frame,
        text=icon,
        font=("Arial", 20),
        text_color=icon_color
    )

    icon_label.pack(
        side="left"
    )


    title_label = ctk.CTkLabel(
        top_frame,
        text=title,
        font=("Arial", 12, "bold"),
        text_color=SECONDARY_TEXT
    )

    title_label.pack(
        side="left",
        padx=8
    )


    # ---------------- VALUE ----------------

    value_label = ctk.CTkLabel(
        card,
        text=value,
        font=("Arial", 22, "bold"),
        text_color=TEXT_COLOR
    )

    value_label.pack(
        anchor="w",
        padx=18,
        pady=(3, 10)
    )


    return value_label


# =========================================================
# SUMMARY CARD LABELS
# =========================================================

income_label = create_summary_card(
    summary_frame,
    0,
    "MONTHLY INCOME",
    "₹",
    "₹0",
    ACCENT_COLOR
)


expense_label = create_summary_card(
    summary_frame,
    1,
    "TOTAL EXPENSES",
    "↘",
    "₹0",
    DANGER_COLOR
)


balance_label = create_summary_card(
    summary_frame,
    2,
    "REMAINING BALANCE",
    "✓",
    "₹0",
    SUCCESS_COLOR
)


goal_label = create_summary_card(
    summary_frame,
    3,
    "GOAL PROGRESS",
    "🎯",
    "0%",
    ACCENT_COLOR
)


# =========================================================
# GOAL SECTION
# =========================================================

goal_section = ctk.CTkFrame(
    content_frame,
    height=155,
    fg_color=CARD_COLOR,
    corner_radius=15
)

goal_section.pack(
    fill="x",
    pady=22
)

goal_section.pack_propagate(False)


# ---------------- GOAL HEADER ----------------

goal_header = ctk.CTkFrame(
    goal_section,
    fg_color="transparent"
)

goal_header.pack(
    fill="x",
    padx=22,
    pady=(15, 0)
)


goal_title = ctk.CTkLabel(
    goal_header,
    text="🎯  Investment Goal",
    font=("Arial", 17, "bold"),
    text_color=TEXT_COLOR
)

goal_title.pack(
    side="left"
)


goal_percentage = ctk.CTkLabel(
    goal_header,
    text="0%",
    font=("Arial", 16, "bold"),
    text_color=ACCENT_COLOR
)

goal_percentage.pack(
    side="right"
)


# ---------------- GOAL DETAILS ----------------

goal_details = ctk.CTkLabel(
    goal_section,
    text="No active investment goal",
    font=("Arial", 12),
    text_color=SECONDARY_TEXT
)

goal_details.pack(
    anchor="w",
    padx=22,
    pady=(8, 5)
)


# ---------------- PROGRESS BAR ----------------

goal_progress_bar = ctk.CTkProgressBar(
    goal_section,
    width=900,
    height=14,
    corner_radius=8,
    progress_color=ACCENT_COLOR
)

goal_progress_bar.pack(
    fill="x",
    padx=22,
    pady=(5, 8)
)

goal_progress_bar.set(0)


# ---------------- GOAL AMOUNT ----------------

goal_amount_label = ctk.CTkLabel(
    goal_section,
    text="₹0 / ₹0",
    font=("Arial", 11),
    text_color=SECONDARY_TEXT
)

goal_amount_label.pack(
    anchor="w",
    padx=22
)


# =========================================================
# QUICK ACTIONS TITLE
# =========================================================

actions_title = ctk.CTkLabel(
    content_frame,
    text="Quick Actions",
    font=("Arial", 22, "bold"),
    text_color=TEXT_COLOR
)

actions_title.pack(
    anchor="w",
    pady=(0, 12)
)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = ctk.CTkFrame(
    content_frame,
    fg_color="transparent"
)

button_frame.pack(
    fill="x"
)


# =========================================================
# BUTTON FUNCTION
# =========================================================

def create_action_button(
    parent,
    row,
    column,
    text,
    command
):

    button = ctk.CTkButton(
        parent,
        text=text,
        width=200,
        height=58,
        corner_radius=12,
        fg_color=CARD_COLOR,
        hover_color=CARD_HOVER,
        text_color=TEXT_COLOR,
        font=("Arial", 14, "bold"),
        command=command
    )

    button.grid(
        row=row,
        column=column,
        padx=7,
        pady=7,
        sticky="ew"
    )

    return button


for column in range(3):
    button_frame.grid_columnconfigure(
        column,
        weight=1
    )


# =========================================================
# ACTION BUTTONS
# =========================================================

create_action_button(
    button_frame,
    0,
    0,
    "➕  Add Expense",
    lambda: open_add_expense(user_id)
)


create_action_button(
    button_frame,
    0,
    1,
    "📋  View Expenses",
    lambda: open_view_expenses(user_id)
)


create_action_button(
    button_frame,
    0,
    2,
    "📊  Analytics",
    lambda: open_analytics(user_id)
)


create_action_button(
    button_frame,
    1,
    0,
    "🎯  Investment Goals",
    lambda: open_goals(user_id)
)


create_action_button(
    button_frame,
    1,
    1,
    "🤖  AI Financial Advisor",
    lambda: open_ai_advisor(user_id)
)


# =========================================================
# GET DASHBOARD DATA
# =========================================================

def load_dashboard_data():

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


        # =================================================
        # USER INFORMATION
        # =================================================

        cursor.execute(
            """
            SELECT
                full_name,
                monthly_income
            FROM users
            WHERE user_id = %s
            """,
            (user_id,)
        )

        user_data = cursor.fetchone()


        if user_data is None:

            messagebox.showerror(
                "Error",
                "User not found!"
            )

            return


        full_name = user_data[0]
        monthly_income = float(user_data[1])


        # =================================================
        # TOTAL EXPENSES
        # =================================================

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = %s
            """,
            (user_id,)
        )

        expense_result = cursor.fetchone()

        total_expenses = float(
            expense_result[0]
        )


        # =================================================
        # REMAINING BALANCE
        # =================================================

        remaining_balance = (
            monthly_income - total_expenses
        )


        # =================================================
        # GOAL INFORMATION
        # =================================================

        cursor.execute(
            """
            SELECT
                goal_type,
                target_amount,
                current_savings
            FROM investment_goals
            WHERE user_id = %s
              AND goal_status = 'Active'
            ORDER BY goal_id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        goal_data = cursor.fetchone()


        if goal_data is not None:

            goal_type = goal_data[0]

            target_amount = float(
                goal_data[1]
            )

            current_savings = float(
                goal_data[2]
            )


            if target_amount > 0:

                goal_progress = (
                    current_savings /
                    target_amount
                ) * 100

            else:

                goal_progress = 0


            goal_progress = min(
                max(goal_progress, 0),
                100
            )

        else:

            goal_type = None
            target_amount = 0
            current_savings = 0
            goal_progress = 0


        # =================================================
        # UPDATE HEADER
        # =================================================

        welcome_label.configure(
            text=f"Welcome, {full_name} 👋"
        )


        # =================================================
        # UPDATE SUMMARY CARDS
        # =================================================

        income_label.configure(
            text=f"₹{monthly_income:,.2f}"
        )


        expense_label.configure(
            text=f"₹{total_expenses:,.2f}"
        )


        balance_label.configure(
            text=f"₹{remaining_balance:,.2f}"
        )


        goal_label.configure(
            text=f"{goal_progress:.1f}%"
        )


        # =================================================
        # UPDATE GOAL SECTION
        # =================================================

        goal_percentage.configure(
            text=f"{goal_progress:.1f}%"
        )


        goal_progress_bar.set(
            goal_progress / 100
        )


        if goal_type is not None:

            goal_details.configure(
                text=f"Goal: {goal_type}"
            )

            goal_amount_label.configure(
                text=(
                    f"₹{current_savings:,.2f}"
                    f" / "
                    f"₹{target_amount:,.2f}"
                )
            )

        else:

            goal_details.configure(
                text="No active investment goal"
            )

            goal_amount_label.configure(
                text="Create a goal to start tracking progress"
            )


    except Exception as e:

        print(
            "DASHBOARD ERROR:",
            repr(e)
        )

        messagebox.showerror(
            "Dashboard Error",
            repr(e)
        )


    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# =========================================================
# LOAD DATA
# =========================================================

load_dashboard_data()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.mainloop()