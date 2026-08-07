import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI Financial Advisor")
app.geometry("900x650")

title = ctk.CTkLabel(
    app,
    text="AI Financial Advisor",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)

question_label = ctk.CTkLabel(
    app,
    text="Ask your financial question",
    font=("Arial", 16)
)

question_label.pack(pady=(20, 10))

question_box = ctk.CTkTextbox(
    app,
    width=700,
    height=120
)

question_box.pack(pady=10)

ask_button = ctk.CTkButton(
    app,
    text="Ask AI",
    width=180
)

ask_button.pack(pady=15)

response_label = ctk.CTkLabel(
    app,
    text="AI Response",
    font=("Arial", 16, "bold")
)

response_label.pack(pady=(20, 10))

response_box = ctk.CTkTextbox(
    app,
    width=700,
    height=180
)

response_box.pack(pady=10)


response_box.insert(
    "1.0",
    "Your financial advice will appear here..."
)

back_button = ctk.CTkButton(
    app,
    text="Back",
    width=180
)

back_button.pack(pady=20)


if __name__ == "__main__":
    app.mainloop()