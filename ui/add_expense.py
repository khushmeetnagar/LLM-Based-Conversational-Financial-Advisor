import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Add Expense")
app.geometry("900x600")

title = ctk.CTkLabel(
    app,
    text="Add Expense",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)

form_frame = ctk.CTkFrame(
    app,
    width=500,
    height=350
)

form_frame.pack(pady=20)
form_frame.pack_propagate(False)
category_label = ctk.CTkLabel(
    form_frame,
    text="Category",
    font=("Arial", 16)
)
category_label.grid(
    row=0,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

category_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="e.g. Food, Travel, Shopping"
)
category_entry.grid(
    row=0,
    column=1,
    padx=20,
    pady=15
)
amount_label = ctk.CTkLabel(
    form_frame,
    text="Amount",
    font=("Arial", 16)
)
amount_label.grid(
    row=1,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

amount_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter amount"
)
amount_entry.grid(
    row=1,
    column=1,
    padx=20,
    pady=15
)
description_label = ctk.CTkLabel(
    form_frame,
    text="Description",
    font=("Arial", 16)
)
description_label.grid(
    row=2,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

description_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="Enter description"
)
description_entry.grid(
    row=2,
    column=1,
    padx=20,
    pady=15
)
date_label = ctk.CTkLabel(
    form_frame,
    text="Date",
    font=("Arial", 16)
)
date_label.grid(
    row=3,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)

date_entry = ctk.CTkEntry(
    form_frame,
    width=250,
    placeholder_text="DD-MM-YYYY"
)
date_entry.grid(
    row=3,
    column=1,
    padx=20,
    pady=15
)
save_button = ctk.CTkButton(
    form_frame,
    text="Save Expense",
    width=180
)

save_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=20
)

back_button = ctk.CTkButton(
    form_frame,
    text="Back",
    width=180
)

back_button.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=10
)
if __name__ == "__main__":
    app.mainloop()