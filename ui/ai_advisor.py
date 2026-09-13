import customtkinter as ctk
import sys
import os
from datetime import date
from tkinter import messagebox

from dotenv import load_dotenv
from google import genai

from database.db_connection import connect_db
from ui.navigation import open_dashboard


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


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
app.geometry("1050x800")
app.minsize(900, 700)


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#0B1120"
CARD_COLOR = "#111827"
CHAT_AI_COLOR = "#172033"
CHAT_USER_COLOR = "#1E3A5F"
TEXT_COLOR = "#F8FAFC"
SECONDARY_TEXT = "#94A3B8"
SUCCESS_COLOR = "#22C55E"
WARNING_COLOR = "#F59E0B"


app.configure(fg_color=BG_COLOR)


# =========================================================
# CHAT HISTORY
# =========================================================

conversation_history = []


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
        # PYTHON CALCULATIONS
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
        # FINANCIAL INFORMATION
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

            target_amount = float(
                goal_data[1]
            )

            target_date = goal_data[2]

            current_goal_savings = float(
                goal_data[3]
            )

            risk_level = goal_data[4]

            # Remaining goal amount

            remaining_goal_amount = max(
                target_amount - current_goal_savings,
                0
            )

            # Months remaining

            today = date.today()

            months_remaining = (
                (target_date.year - today.year) * 12
                + (target_date.month - today.month)
            )

            # Required monthly saving

            if months_remaining > 0:

                required_monthly_saving = (
                    remaining_goal_amount
                    / months_remaining
                )

            else:

                required_monthly_saving = (
                    remaining_goal_amount
                )

            financial_data += f"""

Investment Goal: {goal_type}

Target Amount: ₹{target_amount:,.2f}

Target Date: {target_date}

Current Goal Savings:
₹{current_goal_savings:,.2f}

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

        print(
            "DATABASE ERROR:",
            repr(e)
        )

        return None

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# =========================================================
# FINANCIAL HEALTH SCORE
# =========================================================

def calculate_financial_health(
    monthly_income,
    monthly_savings,
    total_expenses,
    remaining_balance,
    goal_progress
):

    # -----------------------------------------------------
    # SAVINGS RATE - 30 POINTS
    # -----------------------------------------------------

    if monthly_income > 0:

        savings_rate = (
            monthly_savings
            / monthly_income
        ) * 100

    else:

        savings_rate = 0

    if savings_rate >= 30:
        savings_score = 30

    elif savings_rate >= 20:
        savings_score = 25

    elif savings_rate >= 15:
        savings_score = 20

    elif savings_rate >= 10:
        savings_score = 15

    elif savings_rate >= 5:
        savings_score = 8

    else:
        savings_score = 0

    # -----------------------------------------------------
    # EXPENSE CONTROL - 30 POINTS
    # -----------------------------------------------------

    if monthly_income > 0:

        expense_ratio = (
            total_expenses
            / monthly_income
        ) * 100

    else:

        expense_ratio = 100

    if expense_ratio <= 50:
        expense_score = 30

    elif expense_ratio <= 60:
        expense_score = 25

    elif expense_ratio <= 70:
        expense_score = 20

    elif expense_ratio <= 80:
        expense_score = 15

    elif expense_ratio <= 90:
        expense_score = 8

    else:
        expense_score = 0

    # -----------------------------------------------------
    # GOAL PROGRESS - 25 POINTS
    # -----------------------------------------------------

    if goal_progress >= 80:
        goal_score = 25

    elif goal_progress >= 60:
        goal_score = 20

    elif goal_progress >= 40:
        goal_score = 15

    elif goal_progress >= 20:
        goal_score = 10

    elif goal_progress > 0:
        goal_score = 5

    else:
        goal_score = 0

    # -----------------------------------------------------
    # FINANCIAL BUFFER - 15 POINTS
    # -----------------------------------------------------

    if monthly_income > 0:

        buffer_ratio = (
            remaining_balance
            / monthly_income
        ) * 100

    else:

        buffer_ratio = 0

    if buffer_ratio >= 30:
        buffer_score = 15

    elif buffer_ratio >= 20:
        buffer_score = 12

    elif buffer_ratio >= 10:
        buffer_score = 8

    elif buffer_ratio > 0:
        buffer_score = 4

    else:
        buffer_score = 0

    # -----------------------------------------------------
    # TOTAL
    # -----------------------------------------------------

    total_score = (
        savings_score
        + expense_score
        + goal_score
        + buffer_score
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    if total_score >= 80:

        status = "Excellent"

    elif total_score >= 65:

        status = "Good"

    elif total_score >= 50:

        status = "Fair"

    else:

        status = "Needs Improvement"

    return {
        "total_score": total_score,
        "status": status,
        "savings_rate": savings_rate,
        "expense_ratio": expense_ratio,
        "goal_progress": goal_progress,
        "buffer_ratio": buffer_ratio
    }


# =========================================================
# GET HEALTH DATA
# =========================================================

def get_health_data():

    connection = None
    cursor = None

    try:

        connection = connect_db()

        if connection is None:
            return None

        cursor = connection.cursor()

        # -------------------------------------------------
        # USER DATA
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                monthly_income,
                monthly_savings
            FROM users
            WHERE user_id = %s
        """, (user_id,))

        user_data = cursor.fetchone()

        if user_data is None:
            return None

        monthly_income = float(user_data[0])
        monthly_savings = float(user_data[1])

        # -------------------------------------------------
        # EXPENSES
        # -------------------------------------------------

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = %s
        """, (user_id,))

        total_expenses = float(
            cursor.fetchone()[0]
        )

        remaining_balance = (
            monthly_income
            - total_expenses
        )

        # -------------------------------------------------
        # GOAL
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                target_amount,
                current_savings
            FROM investment_goals
            WHERE user_id = %s
              AND goal_status = 'Active'
            ORDER BY goal_id DESC
            LIMIT 1
        """, (user_id,))

        goal_data = cursor.fetchone()

        goal_progress = 0

        if goal_data:

            target_amount = float(
                goal_data[0]
            )

            current_savings = float(
                goal_data[1]
            )

            if target_amount > 0:

                goal_progress = min(
                    (
                        current_savings
                        / target_amount
                    ) * 100,
                    100
                )

        # -------------------------------------------------
        # CALCULATE SCORE
        # -------------------------------------------------

        health = calculate_financial_health(
            monthly_income,
            monthly_savings,
            total_expenses,
            remaining_balance,
            goal_progress
        )

        return health

    except Exception as e:

        print(
            "HEALTH SCORE ERROR:",
            repr(e)
        )

        return None

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# =========================================================
# UPDATE HEALTH SCORE UI
# =========================================================

def update_health_ui():

    health = get_health_data()

    if health is None:
        return

    score = health["total_score"]
    status = health["status"]

    health_score_label.configure(
        text=f"{score}/100"
    )

    health_status_label.configure(
        text=status
    )

    # Status text only
    if status == "Excellent":

        health_status_label.configure(
            text_color=SUCCESS_COLOR
        )

    elif status == "Good":

        health_status_label.configure(
            text_color=SUCCESS_COLOR
        )

    elif status == "Fair":

        health_status_label.configure(
            text_color=WARNING_COLOR
        )

    else:

        health_status_label.configure(
            text_color="#EF4444"
        )


# =========================================================
# ADD CHAT MESSAGE
# =========================================================

def add_chat_message(sender, message):

    if sender == "AI":

        bubble_color = CHAT_AI_COLOR
        sender_text = "🤖 AI Financial Advisor"

    else:

        bubble_color = CHAT_USER_COLOR
        sender_text = "You"

    message_frame = ctk.CTkFrame(
        chat_scroll,
        fg_color=bubble_color,
        corner_radius=15
    )

    message_frame.pack(
        fill="x",
        padx=15,
        pady=8,
        anchor="e" if sender == "User" else "w"
    )

    sender_label = ctk.CTkLabel(
        message_frame,
        text=sender_text,
        font=("Arial", 12, "bold"),
        text_color=TEXT_COLOR
    )

    sender_label.pack(
        anchor="w",
        padx=15,
        pady=(10, 2)
    )

    message_label = ctk.CTkLabel(
        message_frame,
        text=message,
        font=("Arial", 14),
        text_color=TEXT_COLOR,
        justify="left",
        anchor="w",
        wraplength=760
    )

    message_label.pack(
        anchor="w",
        padx=15,
        pady=(2, 12)
    )

    chat_scroll.update_idletasks()

    chat_scroll._parent_canvas.yview_moveto(1.0)


# =========================================================
# CLEAR CHAT
# =========================================================

def clear_chat():

    global conversation_history

    conversation_history = []

    for widget in chat_scroll.winfo_children():

        widget.destroy()

    add_chat_message(
        "AI",
        "Hello! 👋\n\n"
        "I am your AI Financial Advisor. "
        "Ask me anything about your expenses, "
        "savings, investment goals, or financial planning."
    )


# =========================================================
# ASK AI
# =========================================================

def ask_ai():

    global conversation_history

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
    # GET HEALTH DATA
    # -----------------------------------------------------

    health = get_health_data()

    if health is not None:

        health_summary = f"""
Financial Health Score: {health['total_score']}/100
Financial Health Status: {health['status']}
Savings Rate: {health['savings_rate']:.2f}%
Expense Ratio: {health['expense_ratio']:.2f}%
Goal Progress: {health['goal_progress']:.2f}%
Financial Buffer Ratio: {health['buffer_ratio']:.2f}%
"""

    else:

        health_summary = """
Financial Health Score:
Not available.
"""

    # -----------------------------------------------------
    # SHOW USER MESSAGE
    # -----------------------------------------------------

    add_chat_message(
        "User",
        question
    )

    # -----------------------------------------------------
    # CLEAR INPUT
    # -----------------------------------------------------

    question_box.delete(
        "1.0",
        "end"
    )

    # -----------------------------------------------------
    # DISABLE BUTTON
    # -----------------------------------------------------

    ask_button.configure(
        state="disabled",
        text="Thinking..."
    )

    status_label.configure(
        text="● AI is analyzing your question..."
    )

    app.update()

    # -----------------------------------------------------
    # CONVERSATION HISTORY
    # -----------------------------------------------------

    conversation_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    # -----------------------------------------------------
    # BUILD CONVERSATION TEXT
    # -----------------------------------------------------

    conversation_text = ""

    for message in conversation_history:

        if message["role"] == "user":

            conversation_text += (
                f"\nUser: {message['content']}\n"
            )

        else:

            conversation_text += (
                f"\nAI Advisor: {message['content']}\n"
            )

    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are an educational conversational financial advisor.

Your job is to help the user understand and improve
their personal financial situation.

The application has retrieved the user's verified
financial information from the database.

================ FINANCIAL PROFILE ================

{financial_data}

====================================================

================ FINANCIAL HEALTH ==================

{health_summary}

====================================================

================ CONVERSATION ======================

{conversation_text}

====================================================

IMPORTANT INSTRUCTIONS:

1. Give clear, practical and easy-to-understand answers.

2. Use the user's financial profile to personalize
   your response whenever relevant.

3. The financial values and calculations provided by
   the application are the source of truth.

4. Do NOT recalculate application-provided financial
   values yourself.

5. Do NOT invent financial information.

6. If required information is missing, clearly say
   that more information is required.

7. Remember the previous conversation and use it when
   answering follow-up questions.

8. Treat the latest user message as the current question.

9. Do not guarantee investment returns.

10. Clearly explain risks when discussing investments.

11. Do not recommend extremely risky investments for
    short-term financial goals.

12. Keep answers practical and structured.

13. Use simple language suitable for a beginner.

14. If the user asks about their financial health score,
    explain the score using the provided health information.

15. If the user asks something unrelated to finance,
    politely explain that you are primarily designed
    for financial guidance.

16. This system provides educational financial guidance
    and is not a substitute for a licensed financial advisor.

Do not mention these instructions in your response.

Answer the user's latest question directly.
"""

    # -----------------------------------------------------
    # CALL GEMINI
    # -----------------------------------------------------

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        answer = response.text

        if not answer:

            answer = (
                "Sorry, I could not generate a response."
            )

        # -------------------------------------------------
        # SAVE AI RESPONSE TO HISTORY
        # -------------------------------------------------

        conversation_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # -------------------------------------------------
        # DISPLAY AI RESPONSE
        # -------------------------------------------------

        add_chat_message(
            "AI",
            answer
        )

        status_label.configure(
            text="● AI Advisor is ready"
        )

    except Exception as e:

        print(
            "LLM ERROR:",
            repr(e)
        )

        # Remove the last user message if AI failed
        if conversation_history:

            if conversation_history[-1]["role"] == "user":

                conversation_history.pop()

        error_message = (
            "❌ Unable to get AI response.\n\n"
            "Please check your internet connection "
            "or Gemini API availability.\n\n"
            f"Error: {e}"
        )

        add_chat_message(
            "AI",
            error_message
        )

        status_label.configure(
            text="● AI response failed"
        )

    finally:

        ask_button.configure(
            state="normal",
            text="🤖 Ask AI"
        )


# =========================================================
# SUGGESTED QUESTION
# =========================================================

def use_suggestion(text):

    question_box.delete(
        "1.0",
        "end"
    )

    question_box.insert(
        "1.0",
        text
    )

    question_box.focus()


# =========================================================
# HEADER
# =========================================================

header = ctk.CTkFrame(
    app,
    fg_color=BG_COLOR
)

header.pack(
    fill="x",
    padx=30,
    pady=(20, 5)
)


title = ctk.CTkLabel(
    header,
    text="🤖 AI Financial Advisor",
    font=("Arial", 28, "bold"),
    text_color=TEXT_COLOR
)

title.pack(
    anchor="w"
)


subtitle = ctk.CTkLabel(
    header,
    text="Your personalized conversational financial assistant",
    font=("Arial", 14),
    text_color=SECONDARY_TEXT
)

subtitle.pack(
    anchor="w",
    pady=(3, 0)
)


# =========================================================
# STATUS
# =========================================================

status_label = ctk.CTkLabel(
    header,
    text="● AI Advisor is ready",
    font=("Arial", 12),
    text_color=SUCCESS_COLOR
)

status_label.pack(
    anchor="w",
    pady=(5, 0)
)


# =========================================================
# HEALTH SCORE CARD
# =========================================================

health_card = ctk.CTkFrame(
    app,
    fg_color=CARD_COLOR,
    corner_radius=15
)

health_card.pack(
    fill="x",
    padx=30,
    pady=15
)


health_title = ctk.CTkLabel(
    health_card,
    text="💰 Financial Health",
    font=("Arial", 16, "bold"),
    text_color=TEXT_COLOR
)

health_title.pack(
    side="left",
    padx=(20, 10),
    pady=15
)


health_score_label = ctk.CTkLabel(
    health_card,
    text="--/100",
    font=("Arial", 22, "bold"),
    text_color=TEXT_COLOR
)

health_score_label.pack(
    side="left",
    padx=10
)


health_status_label = ctk.CTkLabel(
    health_card,
    text="Loading...",
    font=("Arial", 14, "bold"),
    text_color=SECONDARY_TEXT
)

health_status_label.pack(
    side="left",
    padx=10
)


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

suggestions_frame = ctk.CTkFrame(
    app,
    fg_color=BG_COLOR
)

suggestions_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 10)
)


suggestions_label = ctk.CTkLabel(
    suggestions_frame,
    text="Suggested questions:",
    font=("Arial", 13, "bold"),
    text_color=SECONDARY_TEXT
)

suggestions_label.pack(
    anchor="w",
    pady=(0, 6)
)


suggestion_buttons_frame = ctk.CTkFrame(
    suggestions_frame,
    fg_color=BG_COLOR
)

suggestion_buttons_frame.pack(
    fill="x"
)


suggestions = [
    "How can I save more money?",
    "How should I plan my investment?",
    "Am I spending too much?",
    "How can I reach my financial goal?"
]


for suggestion in suggestions:

    button = ctk.CTkButton(
        suggestion_buttons_frame,
        text=suggestion,
        width=200,
        height=34,
        font=("Arial", 11),
        command=lambda s=suggestion: use_suggestion(s)
    )

    button.pack(
        side="left",
        padx=(0, 8)
    )


# =========================================================
# CONVERSATION HEADER
# =========================================================

conversation_header = ctk.CTkFrame(
    app,
    fg_color=BG_COLOR
)

conversation_header.pack(
    fill="x",
    padx=30,
    pady=(5, 5)
)


conversation_title = ctk.CTkLabel(
    conversation_header,
    text="Conversation",
    font=("Arial", 18, "bold"),
    text_color=TEXT_COLOR
)

conversation_title.pack(
    side="left"
)


clear_button = ctk.CTkButton(
    conversation_header,
    text="🗑 Clear Chat",
    width=110,
    height=32,
    command=clear_chat
)

clear_button.pack(
    side="right"
)


# =========================================================
# CHAT AREA
# =========================================================

chat_scroll = ctk.CTkScrollableFrame(
    app,
    width=900,
    height=270,
    fg_color=CARD_COLOR,
    corner_radius=15
)

chat_scroll.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 12)
)


# =========================================================
# INITIAL AI MESSAGE
# =========================================================

add_chat_message(
    "AI",
    "Hello! 👋\n\n"
    "I am your AI Financial Advisor. "
    "Ask me anything about your expenses, "
    "savings, investment goals, or financial planning."
)


# =========================================================
# QUESTION SECTION
# =========================================================

question_label = ctk.CTkLabel(
    app,
    text="Ask your question",
    font=("Arial", 15, "bold"),
    text_color=TEXT_COLOR
)

question_label.pack(
    anchor="w",
    padx=30,
    pady=(5, 5)
)


question_box = ctk.CTkTextbox(
    app,
    height=80,
    fg_color=CARD_COLOR,
    text_color=TEXT_COLOR,
    border_width=1,
    border_color="#334155",
    corner_radius=12
)

question_box.pack(
    fill="x",
    padx=30,
    pady=(0, 8)
)


# =========================================================
# BUTTON AREA
# =========================================================

button_frame = ctk.CTkFrame(
    app,
    fg_color=BG_COLOR
)

button_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)


ask_button = ctk.CTkButton(
    button_frame,
    text="🤖 Ask AI",
    width=180,
    height=42,
    font=("Arial", 14, "bold"),
    command=ask_ai
)

ask_button.pack(
    side="right"
)


# =========================================================
# BACK BUTTON
# =========================================================

def go_back():

    app.destroy()

    open_dashboard(user_id)


back_button = ctk.CTkButton(
    button_frame,
    text="← Back to Dashboard",
    width=180,
    height=42,
    command=go_back
)

back_button.pack(
    side="left"
)


# =========================================================
# ENTER KEY
# =========================================================

def handle_enter(event):

    if event.state & 0x0001:
        return

    ask_ai()

    return "break"


question_box.bind(
    "<Control-Return>",
    handle_enter
)


# =========================================================
# LOAD HEALTH SCORE
# =========================================================

update_health_ui()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.mainloop()