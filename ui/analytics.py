import customtkinter as ctk
import sys
from tkinter import messagebox

from database.db_connection import connect_db
from ui.navigation import open_dashboard

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#EF4444"


# =========================================================
# APP
# =========================================================

app = ctk.CTk()

app.title("Financial Analytics")
app.geometry("1200x800")
app.minsize(850, 600)

app.configure(
    fg_color=BG_COLOR
)


# =========================================================
# MAIN SCROLLABLE CONTAINER
# =========================================================

main_scroll = ctk.CTkScrollableFrame(
    app,
    fg_color=BG_COLOR,
    scrollbar_fg_color=BG_COLOR,
    scrollbar_button_color=BORDER_COLOR,
    scrollbar_button_hover_color=ACCENT_COLOR
)

main_scroll.pack(
    fill="both",
    expand=True,
    padx=0,
    pady=0
)


# =========================================================
# HEADER
# =========================================================

header_frame = ctk.CTkFrame(
    main_scroll,
    fg_color="transparent"
)

header_frame.pack(
    fill="x",
    padx=35,
    pady=(25, 10)
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

title = ctk.CTkLabel(
    header_frame,
    text="Financial Analytics",
    font=("Arial", 30, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

title.pack(
    anchor="w"
)


# ---------------------------------------------------------
# SUBTITLE
# ---------------------------------------------------------

subtitle = ctk.CTkLabel(
    header_frame,
    text="Understand your spending patterns and financial position",
    font=("Arial", 14),
    text_color=SECONDARY_TEXT,
    anchor="w"
)

subtitle.pack(
    anchor="w",
    pady=(4, 0)
)


# =========================================================
# SUMMARY CARDS
# =========================================================

summary_frame = ctk.CTkFrame(
    main_scroll,
    fg_color="transparent"
)

summary_frame.pack(
    fill="x",
    padx=35,
    pady=15
)


summary_frame.grid_columnconfigure(
    0,
    weight=1
)

summary_frame.grid_columnconfigure(
    1,
    weight=1
)

summary_frame.grid_columnconfigure(
    2,
    weight=1
)


# =========================================================
# CARD CREATOR
# =========================================================

def create_summary_card(
    parent,
    title_text,
    value_text,
    subtitle_text,
    column
):

    card = ctk.CTkFrame(
        parent,
        fg_color=CARD_COLOR,
        corner_radius=16,
        border_width=1,
        border_color=BORDER_COLOR,
        height=135
    )

    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=7
    )

    card.grid_propagate(False)

    # Title
    label_title = ctk.CTkLabel(
        card,
        text=title_text,
        font=("Arial", 13),
        text_color=SECONDARY_TEXT,
        anchor="w"
    )

    label_title.pack(
        anchor="w",
        padx=20,
        pady=(18, 4)
    )

    # Value
    label_value = ctk.CTkLabel(
        card,
        text=value_text,
        font=("Arial", 25, "bold"),
        text_color=TEXT_COLOR,
        anchor="w"
    )

    label_value.pack(
        anchor="w",
        padx=20
    )

    # Subtitle
    label_subtitle = ctk.CTkLabel(
        card,
        text=subtitle_text,
        font=("Arial", 11),
        text_color=SECONDARY_TEXT,
        anchor="w"
    )

    label_subtitle.pack(
        anchor="w",
        padx=20,
        pady=(3, 0)
    )

    return card, label_value


# =========================================================
# SUMMARY CARDS
# =========================================================

income_card, income_label = create_summary_card(
    summary_frame,
    "MONTHLY INCOME",
    "₹0",
    "Your registered monthly income",
    0
)


expense_card, expense_label = create_summary_card(
    summary_frame,
    "TOTAL EXPENSES",
    "₹0",
    "Total recorded expenses",
    1
)


balance_card, balance_label = create_summary_card(
    summary_frame,
    "REMAINING BALANCE",
    "₹0",
    "Income minus recorded expenses",
    2
)


# =========================================================
# CHART SECTION
# =========================================================

charts_title = ctk.CTkLabel(
    main_scroll,
    text="Spending Overview",
    font=("Arial", 21, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

charts_title.pack(
    anchor="w",
    padx=35,
    pady=(15, 8)
)


charts_frame = ctk.CTkFrame(
    main_scroll,
    fg_color="transparent"
)

charts_frame.pack(
    fill="x",
    padx=28,
    pady=5
)


charts_frame.grid_columnconfigure(
    0,
    weight=1
)

charts_frame.grid_columnconfigure(
    1,
    weight=1
)


# =========================================================
# PIE CHART CARD
# =========================================================

pie_card = ctk.CTkFrame(
    charts_frame,
    fg_color=CARD_COLOR,
    corner_radius=16,
    border_width=1,
    border_color=BORDER_COLOR,
    height=430
)

pie_card.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=7
)

pie_card.grid_propagate(False)


pie_title = ctk.CTkLabel(
    pie_card,
    text="Expense Distribution",
    font=("Arial", 18, "bold"),
    text_color=TEXT_COLOR
)

pie_title.pack(
    anchor="w",
    padx=20,
    pady=(15, 0)
)


pie_subtitle = ctk.CTkLabel(
    pie_card,
    text="Where your money is being spent",
    font=("Arial", 11),
    text_color=SECONDARY_TEXT
)

pie_subtitle.pack(
    anchor="w",
    padx=20,
    pady=(2, 5)
)


pie_chart_frame = ctk.CTkFrame(
    pie_card,
    fg_color="transparent"
)

pie_chart_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


# =========================================================
# TREND CHART CARD
# =========================================================

trend_card = ctk.CTkFrame(
    charts_frame,
    fg_color=CARD_COLOR,
    corner_radius=16,
    border_width=1,
    border_color=BORDER_COLOR,
    height=430
)

trend_card.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=7
)

trend_card.grid_propagate(False)


trend_title = ctk.CTkLabel(
    trend_card,
    text="Monthly Expense Trend",
    font=("Arial", 18, "bold"),
    text_color=TEXT_COLOR
)

trend_title.pack(
    anchor="w",
    padx=20,
    pady=(15, 0)
)


trend_subtitle = ctk.CTkLabel(
    trend_card,
    text="Track how your expenses change over time",
    font=("Arial", 11),
    text_color=SECONDARY_TEXT
)

trend_subtitle.pack(
    anchor="w",
    padx=20,
    pady=(2, 5)
)


trend_chart_frame = ctk.CTkFrame(
    trend_card,
    fg_color="transparent"
)

trend_chart_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=5
)


# =========================================================
# INSIGHTS SECTION
# =========================================================

insights_title = ctk.CTkLabel(
    main_scroll,
    text="Financial Insights",
    font=("Arial", 21, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

insights_title.pack(
    anchor="w",
    padx=35,
    pady=(20, 8)
)


insights_card = ctk.CTkFrame(
    main_scroll,
    fg_color=CARD_COLOR,
    corner_radius=16,
    border_width=1,
    border_color=BORDER_COLOR
)

insights_card.pack(
    fill="x",
    padx=35,
    pady=5
)


insights_content = ctk.CTkFrame(
    insights_card,
    fg_color="transparent"
)

insights_content.pack(
    fill="x",
    padx=20,
    pady=18
)


# =========================================================
# INSIGHT LABELS
# =========================================================

expense_ratio_label = ctk.CTkLabel(
    insights_content,
    text="Expense Ratio: 0%",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

expense_ratio_label.pack(
    anchor="w",
    pady=5
)


highest_category_label = ctk.CTkLabel(
    insights_content,
    text="Highest Spending Category: No data",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

highest_category_label.pack(
    anchor="w",
    pady=5
)


spending_status_label = ctk.CTkLabel(
    insights_content,
    text="Spending Status: No data",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

spending_status_label.pack(
    anchor="w",
    pady=5
)


balance_status_label = ctk.CTkLabel(
    insights_content,
    text="Balance Status: No data",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR,
    anchor="w"
)

balance_status_label.pack(
    anchor="w",
    pady=5
)


# =========================================================
# CHART FUNCTIONS
# =========================================================

def create_charts(category_data, monthly_data):

    # -----------------------------------------------------
    # REMOVE OLD CHARTS
    # -----------------------------------------------------

    for widget in pie_chart_frame.winfo_children():
        widget.destroy()

    for widget in trend_chart_frame.winfo_children():
        widget.destroy()


    # -----------------------------------------------------
    # MATPLOTLIB DARK BACKGROUND
    # -----------------------------------------------------

    figure = plt.Figure(
        figsize=(9, 3.6),
        dpi=100
    )

    figure.patch.set_facecolor(CARD_COLOR)


    # =====================================================
    # PIE / DONUT CHART
    # =====================================================

    pie_axis = figure.add_subplot(111)

    pie_axis.set_facecolor(CARD_COLOR)


    if len(category_data) > 0:

        categories = []
        amounts = []

        for row in category_data:

            categories.append(
                str(row[0])
            )

            amounts.append(
                float(row[1])
            )


        pie_axis.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.78,
            wedgeprops={
                "width": 0.42,
                "edgecolor": CARD_COLOR
            },
            textprops={
                "color": TEXT_COLOR,
                "fontsize": 9
            }
        )

        pie_axis.set_title(
            "Expense By Category",
            color=TEXT_COLOR,
            fontsize=13,
            pad=8
        )


    else:

        pie_axis.text(
            0.5,
            0.5,
            "No Expense Data",
            ha="center",
            va="center",
            color=TEXT_COLOR,
            fontsize=13
        )

        pie_axis.set_title(
            "Expense By Category",
            color=TEXT_COLOR,
            fontsize=13
        )


    pie_axis.axis("equal")


    figure.tight_layout()


    pie_canvas = FigureCanvasTkAgg(
        figure,
        master=pie_chart_frame
    )

    pie_canvas.draw()

    pie_canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )


    # =====================================================
    # MONTHLY TREND
    # =====================================================

    trend_figure = plt.Figure(
        figsize=(9, 3.6),
        dpi=100
    )

    trend_figure.patch.set_facecolor(CARD_COLOR)

    trend_axis = trend_figure.add_subplot(111)

    trend_axis.set_facecolor(CARD_COLOR)


    if len(monthly_data) > 0:

        months = []
        amounts = []

        for row in monthly_data:

            months.append(
                str(row[0])
            )

            amounts.append(
                float(row[1])
            )


        x_positions = list(
            range(len(months))
        )


        # -------------------------------------------------
        # AREA
        # -------------------------------------------------

        trend_axis.fill_between(
            x_positions,
            amounts,
            alpha=0.25
        )


        # -------------------------------------------------
        # LINE
        # -------------------------------------------------

        trend_axis.plot(
            x_positions,
            amounts,
            marker="o",
            linewidth=2
        )


        # -------------------------------------------------
        # X AXIS
        # -------------------------------------------------

        trend_axis.set_xticks(
            x_positions
        )

        trend_axis.set_xticklabels(
            months,
            rotation=45,
            ha="right"
        )


        # -------------------------------------------------
        # LABELS
        # -------------------------------------------------

        trend_axis.set_xlabel(
            "Month",
            color=TEXT_COLOR
        )

        trend_axis.set_ylabel(
            "Expense (₹)",
            color=TEXT_COLOR
        )


        trend_axis.set_title(
            "Monthly Expense Trend",
            color=TEXT_COLOR,
            fontsize=13
        )


        # -------------------------------------------------
        # TICKS
        # -------------------------------------------------

        trend_axis.tick_params(
            axis="x",
            colors=TEXT_COLOR
        )

        trend_axis.tick_params(
            axis="y",
            colors=TEXT_COLOR
        )


        # -------------------------------------------------
        # GRID
        # -------------------------------------------------

        trend_axis.grid(
            axis="y",
            alpha=0.2
        )


        # -------------------------------------------------
        # SPINES
        # -------------------------------------------------

        trend_axis.spines[
            "top"
        ].set_visible(False)

        trend_axis.spines[
            "right"
        ].set_visible(False)


    else:

        trend_axis.text(
            0.5,
            0.5,
            "No Expense Data",
            ha="center",
            va="center",
            color=TEXT_COLOR,
            fontsize=13
        )

        trend_axis.set_title(
            "Monthly Expense Trend",
            color=TEXT_COLOR,
            fontsize=13
        )


    trend_figure.tight_layout()


    trend_canvas = FigureCanvasTkAgg(
        trend_figure,
        master=trend_chart_frame
    )

    trend_canvas.draw()

    trend_canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )


# =========================================================
# LOAD ANALYTICS DATA
# =========================================================

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


        # =================================================
        # MONTHLY INCOME
        # =================================================

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

        expense_data = cursor.fetchone()


        total_expenses = float(
            expense_data[0]
        )


        # =================================================
        # REMAINING BALANCE
        # =================================================

        remaining_balance = (
            monthly_income -
            total_expenses
        )


        # =================================================
        # CATEGORY-WISE EXPENSES
        # =================================================

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
            ORDER BY SUM(expenses.amount) DESC
            """,
            (user_id,)
        )

        category_data = cursor.fetchall()


        # =================================================
        # MONTHLY EXPENSE DATA
        # =================================================

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


        # =================================================
        # EXPENSE RATIO
        # =================================================

        if monthly_income > 0:

            expense_ratio = (
                total_expenses /
                monthly_income
            ) * 100

        else:

            expense_ratio = 0


        expense_ratio_label.configure(
            text=f"Expense Ratio: {expense_ratio:.1f}%"
        )


        # =================================================
        # HIGHEST CATEGORY
        # =================================================

        if len(category_data) > 0:

            highest_category = category_data[0][0]
            highest_amount = float(
                category_data[0][1]
            )

            highest_category_label.configure(
                text=(
                    f"Highest Spending Category: "
                    f"{highest_category} "
                    f"(₹{highest_amount:,.2f})"
                )
            )

        else:

            highest_category_label.configure(
                text="Highest Spending Category: No data"
            )


        # =================================================
        # SPENDING STATUS
        # =================================================

        if expense_ratio <= 50:

            spending_status = "Healthy"
            spending_color = SUCCESS_COLOR

        elif expense_ratio <= 70:

            spending_status = "Moderate"
            spending_color = WARNING_COLOR

        elif expense_ratio <= 90:

            spending_status = "High"
            spending_color = WARNING_COLOR

        else:

            spending_status = "Very High"
            spending_color = DANGER_COLOR


        spending_status_label.configure(
            text=f"Spending Status: {spending_status}",
            text_color=spending_color
        )


        # =================================================
        # BALANCE STATUS
        # =================================================

        if remaining_balance > 0:

            balance_status = (
                f"Positive balance of "
                f"₹{remaining_balance:,.2f}"
            )

            balance_color = SUCCESS_COLOR

        elif remaining_balance == 0:

            balance_status = (
                "No remaining balance"
            )

            balance_color = WARNING_COLOR

        else:

            balance_status = (
                f"Expenses exceed income by "
                f"₹{abs(remaining_balance):,.2f}"
            )

            balance_color = DANGER_COLOR


        balance_status_label.configure(
            text=f"Balance Status: {balance_status}",
            text_color=balance_color
        )


        # =================================================
        # CREATE CHARTS
        # =================================================

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
            f"Something went wrong:\n{e}"
        )


    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# =========================================================
# BOTTOM NAVIGATION
# =========================================================

bottom_frame = ctk.CTkFrame(
    main_scroll,
    fg_color="transparent"
)

bottom_frame.pack(
    fill="x",
    padx=35,
    pady=(20, 30)
)


back_button = ctk.CTkButton(
    bottom_frame,
    text="←  Back to Dashboard",
    width=220,
    height=42,
    corner_radius=9,
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    font=("Arial", 13, "bold"),
    command=lambda: go_back()
)

back_button.pack(
    anchor="e"
)


# =========================================================
# BACK FUNCTION
# =========================================================

def go_back():

    app.destroy()

    open_dashboard(user_id)


# =========================================================
# LOAD DATA
# =========================================================

load_analytics_data()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    print("ANALYTICS WINDOW STARTED")

    app.mainloop()

    print("ANALYTICS WINDOW CLOSED")