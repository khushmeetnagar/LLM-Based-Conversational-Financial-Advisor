import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Analytics")
app.geometry("1000x700")

title = ctk.CTkLabel(
    app,
    text="Analytics",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)
summary_frame = ctk.CTkFrame(
    app,
    width=800,
    height=120
)
summary_frame.pack(pady=20)
summary_frame.pack_propagate(False)
expense_label = ctk.CTkLabel(
    summary_frame,
    text="Total Expenses\n₹0",
    font=("Arial", 18, "bold")
)
expense_label.grid(
    row=0,
    column=1,
    padx=40,
    pady=30
)
chart_frame = ctk.CTkFrame(
    app,
    width=900,
    height=300
)

chart_frame.pack(pady=20)
chart_frame.pack_propagate(False)
pie_frame = ctk.CTkFrame(
    chart_frame,
    width=350,
    height=220
)

pie_frame.grid(row=0, column=0, padx=30, pady=25)
pie_frame.pack_propagate(False)

pie_title = ctk.CTkLabel(
    pie_frame,
    text="Expense By Category",
    font=("Arial", 18, "bold")
)
pie_title.pack(pady=15)

pie_placeholder = ctk.CTkLabel(
    pie_frame,
    text="📊 Chart Placeholder"
)
pie_placeholder.pack(expand=True)

trend_frame = ctk.CTkFrame(
    chart_frame,
    width=350,
    height=220
)

trend_frame.grid(row=0, column=1, padx=30, pady=25)
trend_frame.pack_propagate(False)

trend_title = ctk.CTkLabel(
    trend_frame,
    text="Monthly Trend",
    font=("Arial", 18, "bold")
)
trend_title.pack(pady=15)

trend_placeholder = ctk.CTkLabel(
    trend_frame,
    text="📈 Chart Placeholder"
)
trend_placeholder.pack(expand=True)

back_button = ctk.CTkButton(
    app,
    text="Back",
    width=180
)

back_button.pack(pady=10)


income_label = ctk.CTkLabel(
    summary_frame,
    text="Monthly Income\n₹0",
    font=("Arial", 18, "bold")
)


income_label.grid(row=0, column=0, padx=40, pady=30)


balance_label = ctk.CTkLabel(
    summary_frame,
    text="Remaining Balance\n₹0",
    font=("Arial", 18, "bold")
)

balance_label.grid(row=0, column=2, padx=40, pady=30)



if __name__ == "__main__":
    app.mainloop()
