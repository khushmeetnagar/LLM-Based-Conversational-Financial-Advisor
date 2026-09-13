import customtkinter as ctk
import sys
from tkinter import messagebox
from database.db_connection import connect_db
from ui.navigation import open_dashboard

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- USER ID ----------------

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1


# ---------------- APPEARANCE ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- APP ----------------

app = ctk.CTk()
app.title("Analytics")
app.geometry("1100x750")


# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    app,
    text="Analytics",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# ---------------- SUMMARY FRAME ----------------

summary_frame = ctk.CTkFrame(
    app,
    width=1000,
    height=120
)

summary_frame.pack(pady=10)
summary_frame.pack_propagate(False)


# ---------------- INCOME ----------------

income_label = ctk.CTkLabel(
    summary_frame,
    text="Monthly Income\n₹0",
    font=("Arial", 18, "bold")
)

income_label.grid(
    row=0,
    column=0,
    padx=50,
    pady=30
)


# ---------------- EXPENSE ----------------

expense_label = ctk.CTkLabel(
    summary_frame,
    text="Total Expenses\n₹0",
    font=("Arial", 18, "bold")
)

expense_label.grid(
    row=0,
    column=1,
    padx=50,
    pady=30
)


# ---------------- BALANCE ----------------

balance_label = ctk.CTkLabel(
    summary_frame,
    text="Remaining Balance\n₹0",
    font=("Arial", 18, "bold")
)

balance_label.grid(
    row=0,
    column=2,
    padx=50,
    pady=30
)


# ---------------- CHART FRAME ----------------

chart_frame = ctk.CTkFrame(
    app,
    width=1000,
    height=450
)

chart_frame.pack(pady=20)
chart_frame.pack_propagate(False)


# ---------------- CREATE CHARTS ----------------

def create_charts(category_data, monthly_data):

    # Remove previous charts
    for widget in chart_frame.winfo_children():
        widget.destroy()

    figure = plt.Figure(
        figsize=(10, 4.2)
    )


    # ==================================================
    # PIE CHART
    # ==================================================

    pie_axis = figure.add_subplot(121)

    if len(category_data) > 0:

        categories = []
        amounts = []

        for row in category_data:

            categories.append(row[0])
            amounts.append(float(row[1]))

        pie_axis.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%"
        )

        pie_axis.set_title(
            "Expense By Category"
        )

    else:

        pie_axis.text(
            0.5,
            0.5,
            "No Expense Data",
            ha="center",
            va="center"
        )

        pie_axis.set_title(
            "Expense By Category"
        )


    # ==================================================
    # MONTHLY TREND
    # ==================================================

    trend_axis = figure.add_subplot(122)

    if len(monthly_data) > 0:

        months = []
        amounts = []

        for row in monthly_data:

            months.append(row[0])
            amounts.append(float(row[1]))

        trend_axis.plot(
            months,
            amounts,
            marker="o"
        )

        trend_axis.set_title(
            "Monthly Expense Trend"
        )

        trend_axis.set_xlabel(
            "Month"
        )

        trend_axis.set_ylabel(
            "Expense"
        )

        trend_axis.tick_params(
            axis="x",
            rotation=45
        )

    else:

        trend_axis.text(
            0.5,
            0.5,
            "No Expense Data",
            ha="center",
            va="center"
        )

        trend_axis.set_title(
            "Monthly Expense Trend"
        )


    figure.tight_layout()


    # ---------------- DISPLAY CHART ----------------

    canvas = FigureCanvasTkAgg(
        figure,
        master=chart_frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# ---------------- LOAD ANALYTICS DATA ----------------

def load_analytics_data():

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


        # ==================================================
        # MONTHLY INCOME
        # ==================================================

        cursor.execute(
            """
            SELECT monthly_income
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

        monthly_income = float(
            user_data[0]
        )


        # ==================================================
        # TOTAL EXPENSES
        # ==================================================

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = %s
            """,
            (user_id,)
        )

        expense_data = cursor.fetchone()

        total_expenses = float(
            expense_data[0]
        )


        # ==================================================
        # REMAINING BALANCE
        # ==================================================

        remaining_balance = (
            monthly_income - total_expenses
        )


        # ==================================================
        # CATEGORY-WISE EXPENSES
        # ==================================================

        cursor.execute(
            """
            SELECT
                categories.category_name,
                SUM(expenses.amount)
            FROM expenses
            JOIN categories
                ON expenses.category_id =
                   categories.category_id
            WHERE expenses.user_id = %s
            GROUP BY categories.category_name
            """,
            (user_id,)
        )

        category_data = cursor.fetchall()


        # ==================================================
        # MONTHLY EXPENSE DATA
        # ==================================================

        cursor.execute(
            """
            SELECT
                DATE_FORMAT(
                    expense_date,
                    '%Y-%m'
                ) AS month,
                SUM(amount)
            FROM expenses
            WHERE user_id = %s
            GROUP BY DATE_FORMAT(
                expense_date,
                '%Y-%m'
            )
            ORDER BY month
            """,
            (user_id,)
        )

        monthly_data = cursor.fetchall()


        # ==================================================
        # UPDATE SUMMARY
        # ==================================================

        income_label.configure(
            text=f"Monthly Income\n₹{monthly_income:,.2f}"
        )

        expense_label.configure(
            text=f"Total Expenses\n₹{total_expenses:,.2f}"
        )

        balance_label.configure(
            text=f"Remaining Balance\n₹{remaining_balance:,.2f}"
        )


        # ==================================================
        # CREATE CHARTS
        # ==================================================

        create_charts(
            category_data,
            monthly_data
        )


    except Exception as e:

        print(
            "ANALYTICS ERROR:",
            repr(e)
        )

        messagebox.showerror(
            "Analytics Error",
            repr(e)
        )


    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ---------------- BACK BUTTON ----------------

def go_back():

    app.destroy()

    open_dashboard(user_id)


back_button = ctk.CTkButton(
    app,
    text="Back",
    width=180,
    command=go_back
)

back_button.pack(pady=10)


# ---------------- LOAD DATA ----------------

load_analytics_data()


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":
    app.mainloop()