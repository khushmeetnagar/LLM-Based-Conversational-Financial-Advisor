import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("View Expenses")
app.geometry("900x600")

title = ctk.CTkLabel(
    app,
    text="View Expenses",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)
table_frame = ctk.CTkFrame(
    app,
    width=800,
    height=400
)

table_frame.pack(pady=20)
table_frame.pack_propagate(False)
category_header = ctk.CTkLabel(
    table_frame,
    text="Category",
    font=("Arial", 16, "bold")
)
category_header.grid(row=0, column=0, padx=35, pady=20)
amount_header = ctk.CTkLabel(
    table_frame,
    text="Amount",
    font=("Arial", 16, "bold")
)
separator = ctk.CTkFrame(
    table_frame,
    height=2
)
separator.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="ew",
    padx=10,
    pady=5
)
no_data = ctk.CTkLabel(
    table_frame,
    text="No expenses found",
    font=("Arial", 14)
)

no_data.grid(
    row=2,
    column=0,
    columnspan=4,
    pady=30
)
back_button = ctk.CTkButton(
    app,
    text="Back",
    width=180
)

back_button.pack(pady=20)
amount_header.grid(row=0, column=1, padx=35, pady=20)
description_header = ctk.CTkLabel(
    table_frame,
    text="Description",
    font=("Arial", 16, "bold")
)
description_header.grid(row=0, column=2, padx=35, pady=20)
date_header = ctk.CTkLabel(
    table_frame,
    text="Date",
    font=("Arial", 16, "bold")
)
date_header.grid(row=0, column=3, padx=35, pady=20)

if __name__ == "__main__":
    app.mainloop()