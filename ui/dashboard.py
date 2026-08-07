import customtkinter as ctk


app = ctk.CTk()
app.title("Dashboard")
app.geometry("1000x700")

title = ctk.CTkLabel(
    app,
    text="Dashboard",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)
welcome_label = ctk.CTkLabel(
    app,
    text="Welcome, User 👋",
    font=("Arial", 22, "bold")
)
welcome_label.pack(pady=10)
summary_frame = ctk.CTkFrame(
    app,
    width=900,
    height=180
)
summary_frame.pack(pady=20)

summary_frame.pack_propagate(False)
button_frame = ctk.CTkFrame(
    app,
    width=900,
    height=250
)
button_frame.pack(pady=20)

button_frame.pack_propagate(False)
add_expense_btn = ctk.CTkButton(
    button_frame,
    text="➕ Add Expense",
    width=180,
    height=45
)

add_expense_btn.grid(row=0, column=0, padx=20, pady=20)
view_btn = ctk.CTkButton(
    button_frame,
    text="📋 View Expenses",
    width=180,
    height=45
)

view_btn.grid(row=0, column=1, padx=20, pady=20)
analytics_btn = ctk.CTkButton(
    button_frame,
    text="📊 Analytics",
    width=180,
    height=45
)

analytics_btn.grid(row=0, column=2, padx=20, pady=20)
goal_btn = ctk.CTkButton(
    button_frame,
    text="🎯 Investment Goals",
    width=180,
    height=45
)

goal_btn.grid(row=1, column=0, padx=20, pady=20)
ai_btn = ctk.CTkButton(
    button_frame,
    text="🤖 AI Advisor",
    width=180,
    height=45
)

ai_btn.grid(row=1, column=1, padx=20, pady=20)

income_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)
income_frame.grid(row=0, column=0, padx=15, pady=25)

income_label = ctk.CTkLabel(
    income_frame,
    text="💰 Monthly Income\n₹0",
    font=("Arial", 18, "bold")
)
income_label.pack(expand=True)
expense_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)
expense_frame.grid(row=0, column=1, padx=15, pady=25)

expense_label = ctk.CTkLabel(
    expense_frame,
    text="💸 Total Expenses\n₹0",
    font=("Arial", 18, "bold")
)
expense_label.pack(expand=True)
balance_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)
balance_frame.grid(row=0, column=2, padx=15, pady=25)

balance_label = ctk.CTkLabel(
    balance_frame,
    text="💵 Remaining Balance\n₹0",
    font=("Arial", 18, "bold")
)
balance_label.pack(expand=True)
goal_frame = ctk.CTkFrame(
    summary_frame,
    width=200,
    height=120
)
goal_frame.grid(row=0, column=3, padx=15, pady=25)

goal_label = ctk.CTkLabel(
    goal_frame,
    text="🎯 Goal Progress\n0%",
    font=("Arial", 18, "bold")
)
goal_label.pack(expand=True)


if __name__ == "__main__":
    app.mainloop()