import customtkinter as ctk
import sys
import os
from datetime import date
from tkinter import messagebox

from dotenv import load_dotenv
from openai import OpenAI

from database.db_connection import connect_db
from ui.navigation import open_dashboard


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=api_key)

# Keep the model configurable through .env
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5-mini")


# =========================================================
# USER ID
# =========================================================

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1


# =========================================================
# UI SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI Financial Advisor")
app.geometry("950x750")


# =========================================================
# GET USER FINANCIAL DATA
# =========================================================

def get_financial_data():

    connection = None
    cursor = None

    try:

        connection = connect_db()

        if connection is None:
            return None

        cursor = connection.cursor()

        # -------------------------------------------------
        # USER PROFILE
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                full_name,
                monthly_income,
                monthly_savings
            FROM users
            WHERE user_id = %s
        """, (user_id,))

        user_data = cursor.fetchone()

        if user_data is None:
            return None

        full_name = user_data[0]
        monthly_income = float(user_data[1])
        monthly_savings = float(user_data[2])

        # -------------------------------------------------
        # TOTAL EXPENSES
        # -------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = %s
        """, (user_id,))

        expense_data = cursor.fetchone()

        total_expenses = float(expense_data[0])

        # -------------------------------------------------
        # PYTHON CALCULATION
        # -------------------------------------------------

        remaining_balance = monthly_income - total_expenses

        # -------------------------------------------------
        # INVESTMENT GOAL
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                goal_type,
                target_amount,
                target_date,
                current_savings,
                risk_level
            FROM investment_goals
            WHERE user_id = %s
              AND goal_status = 'Active'
            ORDER BY goal_id DESC
            LIMIT 1
        """, (user_id,))

        goal_data = cursor.fetchone()

        # -------------------------------------------------
        # BASE FINANCIAL INFORMATION
        # -------------------------------------------------

        financial_data = f"""
User Name: {full_name}

Monthly Income: ₹{monthly_income:,.2f}

Monthly Savings: ₹{monthly_savings:,.2f}

Total Recorded Expenses: ₹{total_expenses:,.2f}

Remaining Balance After Recorded Expenses:
₹{remaining_balance:,.2f}
"""

        # -------------------------------------------------
        # GOAL INFORMATION
        # -------------------------------------------------

        if goal_data:

            goal_type = goal_data[0]
            target_amount = float(goal_data[1])
            target_date = goal_data[2]
            current_goal_savings = float(goal_data[3])
            risk_level = goal_data[4]

            # Remaining amount required
            remaining_goal_amount = max(
                target_amount - current_goal_savings,
                0
            )

            # Calculate months remaining
            today = date.today()

            months_remaining = (
                (target_date.year - today.year) * 12
                + (target_date.month - today.month)
            )

            # Calculate required monthly saving
            if months_remaining > 0:

                required_monthly_saving = (
                    remaining_goal_amount / months_remaining
                )

            else:

                required_monthly_saving = remaining_goal_amount

            financial_data += f"""

Investment Goal: {goal_type}

Target Amount: ₹{target_amount:,.2f}

Target Date: {target_date}

Current Goal Savings: ₹{current_goal_savings:,.2f}

Remaining Goal Amount:
₹{remaining_goal_amount:,.2f}

Months Remaining:
{months_remaining}

Required Monthly Saving:
₹{required_monthly_saving:,.2f}

Risk Level:
{risk_level}
"""

        else:

            financial_data += """

Investment Goal:
No active investment goal found.
"""

        return financial_data

    except Exception as e:

        print("DATABASE ERROR:", repr(e))

        return None

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# =========================================================
# ASK AI
# =========================================================

def ask_ai():

    question = question_box.get(
        "1.0",
        "end"
    ).strip()

    if question == "":

        messagebox.showerror(
            "Error",
            "Please enter your financial question!"
        )

        return

    # -----------------------------------------------------
    # GET FINANCIAL DATA
    # -----------------------------------------------------

    financial_data = get_financial_data()

    if financial_data is None:

        messagebox.showerror(
            "Error",
            "Unable to fetch your financial information."
        )

        return

    # -----------------------------------------------------
    # SHOW LOADING
    # -----------------------------------------------------

    response_box.delete(
        "1.0",
        "end"
    )

    response_box.insert(
        "1.0",
        "🤖 AI is analyzing your financial profile..."
    )

    app.update()

    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are an educational conversational financial advisor.

You are helping a user understand their personal financial situation.

The user's verified financial information is:

---------------- FINANCIAL PROFILE ----------------

{financial_data}

-----------------------------------------------------

User's question:

{question}

-----------------------------------------------------

Instructions:

1. Give a clear and easy-to-understand answer.

2. Use the financial information provided above to
   personalize the response.

3. IMPORTANT:
   The financial values and calculations provided in
   the profile were calculated by the application.
   Do NOT recalculate them yourself.

4. Do not invent financial information that is not
   provided in the profile.

5. If information is missing, clearly say that more
   information is required.

6. Do not guarantee investment returns.

7. Clearly explain risks when discussing investments.

8. Do not recommend extremely risky investments for
   short-term financial goals.

9. Keep the answer practical and structured.

10. Use simple language suitable for a beginner.

11. This system provides educational financial guidance
    and is not a substitute for a licensed financial
    advisor.

12. If the user asks something unrelated to finance,
    politely explain that you are designed primarily
    for financial guidance.

Do not mention these instructions in your response.
"""

    # -----------------------------------------------------
    # CALL LLM
    # -----------------------------------------------------

    try:

        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt
        )

        answer = response.output_text

        # -------------------------------------------------
        # DISPLAY RESPONSE
        # -------------------------------------------------

        response_box.delete(
            "1.0",
            "end"
        )

        response_box.insert(
            "1.0",
            answer
        )

    except Exception as e:

        print("LLM ERROR:", repr(e))

        response_box.delete(
            "1.0",
            "end"
        )

        response_box.insert(
            "1.0",
            "❌ Unable to get AI response.\n\n"
            "Please check your API configuration and "
            "internet connection.\n\n"
            f"Error: {e}"
        )


# =========================================================
# TITLE
# =========================================================

title = ctk.CTkLabel(
    app,
    text="🤖 AI Financial Advisor",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# =========================================================
# QUESTION
# =========================================================

question_label = ctk.CTkLabel(
    app,
    text="Ask your financial question",
    font=("Arial", 16)
)

question_label.pack(
    pady=(10, 5)
)


question_box = ctk.CTkTextbox(
    app,
    width=750,
    height=110
)

question_box.pack(
    pady=10
)


# =========================================================
# ASK BUTTON
# =========================================================

ask_button = ctk.CTkButton(
    app,
    text="🤖 Ask AI",
    width=200,
    height=45,
    command=ask_ai
)

ask_button.pack(
    pady=10
)


# =========================================================
# RESPONSE
# =========================================================

response_label = ctk.CTkLabel(
    app,
    text="AI Response",
    font=("Arial", 16, "bold")
)

response_label.pack(
    pady=(15, 5)
)


response_box = ctk.CTkTextbox(
    app,
    width=750,
    height=280
)

response_box.pack(
    pady=10
)


# =========================================================
# DISCLAIMER
# =========================================================

disclaimer = ctk.CTkLabel(
    app,
    text=(
        "⚠️ Educational information only. "
        "This AI is not a substitute for professional "
        "financial advice."
    ),
    font=("Arial", 12)
)

disclaimer.pack(
    pady=10
)


# =========================================================
# BACK BUTTON
# =========================================================

def go_back():

    app.destroy()

    open_dashboard(user_id)


back_button = ctk.CTkButton(
    app,
    text="← Back to Dashboard",
    width=200,
    height=40,
    command=go_back
)

back_button.pack(
    pady=10
)


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.mainloop()