import customtkinter as ctk
import sys
from database.db_connection import connect_db
from ui.navigation import (
    open_add_expense,
    open_view_expenses,
    open_analytics,
    open_goals ,
    open_ai_advisor
)
from tkinter import messagebox


# ---------------- USER ID ----------------

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1


# ---------------- APP SETUP ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Dashboard")
app.geometry("1000x700")


# ---------------- GET DASHBOARD DATA ----------------

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

        # ---------------- USER INFORMATION ----------------

        cursor.execute(
            """
            SELECT full_name, monthly_income
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

        # ---------------- TOTAL EXPENSES ----------------

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = %s
            """,
            (user_id,)
        )

        expense_result = cursor.fetchone()

        total_expenses = float(expense_result[0])

        # ---------------- REMAINING BALANCE ----------------

        remaining_balance = (
            monthly_income - total_expenses
        )

        # ---------------- GOAL PROGRESS ----------------

        cursor.execute(
            """
            SELECT
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

            target_amount = float(goal_data[0])
            current_savings = float(goal_data[1])

            if target_amount > 0:

                goal_progress = (
                    current_savings / target_amount
                ) * 100

            else:

                goal_progress = 0

            goal_progress = min(
                goal_progress,
                100
            )

        else:

            goal_progress = 0

        # ---------------- UPDATE UI ----------------

        welcome_label.configure(
            text=f"Welcome, {full_name} 👋"
        )

        income_label.configure(
            text=f"💰 Monthly Income\n₹{monthly_income:,.2f}"
        )

        expense_label.configure(
            text=f"💸 Total Expenses\n₹{total_expenses:,.2f}"
        )

        balance_label.configure(
            text=f"💵 Remaining Balance\n₹{remaining_balance:,.2f}"
        )

        goal_label.configure(
            text=f"🎯 Goal Progress\n{goal_progress:.1f}%"
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


# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    app,
    text="Dashboard",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# ---------------- WELCOME ----------------

welcome_label = ctk.CTkLabel(
    app,
    text="Welcome, User 👋",
    font=("Arial", 22, "bold")
)

welcome_label.pack(pady=10)


# ---------------- SUMMARY FRAME ----------------

summary_frame = ctk.CTkFrame(
    app,
    width=900,
    height=180
)

summary_frame.pack(pady=20)
summary_frame.pack_propagate(False)


# ---------------- INCOME CARD ----------------

income_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)

income_frame.grid(
    row=0,
    column=0,
    padx=15,
    pady=25
)

income_frame.grid_propagate(False)

income_label = ctk.CTkLabel(
    income_frame,
    text="💰 Monthly Income\n₹0",
    font=("Arial", 18, "bold")
)

income_label.pack(expand=True)


# ---------------- EXPENSE CARD ----------------

expense_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)

expense_frame.grid(
    row=0,
    column=1,
    padx=15,
    pady=25
)

expense_frame.grid_propagate(False)

expense_label = ctk.CTkLabel(
    expense_frame,
    text="💸 Total Expenses\n₹0",
    font=("Arial", 18, "bold")
)

expense_label.pack(expand=True)


# ---------------- BALANCE CARD ----------------

balance_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)

balance_frame.grid(
    row=0,
    column=2,
    padx=15,
    pady=25
)

balance_frame.grid_propagate(False)

balance_label = ctk.CTkLabel(
    balance_frame,
    text="💵 Remaining Balance\n₹0",
    font=("Arial", 18, "bold")
)

balance_label.pack(expand=True)


# ---------------- GOAL CARD ----------------

goal_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)

goal_frame.grid(
    row=0,
    column=3,
    padx=15,
    pady=25
)

goal_frame.grid_propagate(False)

goal_label = ctk.CTkLabel(
    goal_frame,
    text="🎯 Goal Progress\n0%",
    font=("Arial", 18, "bold")
)

goal_label.pack(expand=True)


# ---------------- BUTTON FRAME ----------------

button_frame = ctk.CTkFrame(
    app,
    width=900,
    height=250
)

button_frame.pack(pady=20)
button_frame.pack_propagate(False)


# ---------------- ADD EXPENSE ----------------

add_expense_btn = ctk.CTkButton(
    button_frame,
    text="➕ Add Expense",
    width=180,
    height=45,
    command=lambda: open_add_expense(user_id)
)

add_expense_btn.grid(
    row=0,
    column=0,
    padx=20,
    pady=20
)


# ---------------- VIEW EXPENSES ----------------

view_btn = ctk.CTkButton(
    button_frame,
    text="📋 View Expenses",
    width=180,
    height=45,
    command=lambda: open_view_expenses(user_id)
)

view_btn.grid(
    row=0,
    column=1,
    padx=20,
    pady=20
)


# ---------------- ANALYTICS ----------------

analytics_btn = ctk.CTkButton(
    button_frame,
    text="📊 Analytics",
    width=180,
    height=45,
    command=lambda: open_analytics(user_id)
)

analytics_btn.grid(
    row=0,
    column=2,
    padx=20,
    pady=20
)


# ---------------- INVESTMENT GOALS ----------------

goal_btn = ctk.CTkButton(
    button_frame,
    text="🎯 Investment Goals",
    width=180,
    height=45,
    command=lambda: open_goals(user_id)
)

goal_btn.grid(
    row=1,
    column=0,
    padx=20,
    pady=20
)


# ---------------- AI ADVISOR ----------------

ai_btn = ctk.CTkButton(
    button_frame,
    text="🤖 AI Advisor",
    width=180,
    height=45,
    command=lambda: open_ai_advisor(user_id)
)

ai_btn.grid(
    row=1,
    column=1,
    padx=20,
    pady=20
)


# ---------------- LOAD DATA ----------------

load_dashboard_data()


# ---------------- START APP ----------------

if __name__ == "__main__":
    app.mainloop()