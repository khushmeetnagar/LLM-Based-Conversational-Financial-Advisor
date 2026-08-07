import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Investment Goals")
app.geometry("900x600")

title = ctk.CTkLabel(
    app,
    text="Investment Goals",
    font=("Arial", 28, "bold")
)
title.pack(pady=20)


goal_frame = ctk.CTkFrame(
    app,
    width=500,
    height=350
)

goal_frame.pack(pady=20)
goal_frame.pack_propagate(False)

goal_label = ctk.CTkLabel(
    goal_frame,
    text="Goal Name",
    font=("Arial", 16)
)
goal_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

goal_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="e.g. Buy Laptop"
)
goal_entry.grid(row=0, column=1, padx=20, pady=15)

target_label = ctk.CTkLabel(
    goal_frame,
    text="Target Amount",
    font=("Arial", 16)
)
target_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")

target_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="Enter target amount"
)
target_entry.grid(row=1, column=1, padx=20, pady=15)

deadline_label = ctk.CTkLabel(
    goal_frame,
    text="Deadline",
    font=("Arial", 16)
)
deadline_label.grid(row=2, column=0, padx=20, pady=15, sticky="w")

deadline_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="DD-MM-YYYY"
)
deadline_entry.grid(row=2, column=1, padx=20, pady=15)

saved_label = ctk.CTkLabel(
    goal_frame,
    text="Current Saved",
    font=("Arial", 16)
)
saved_label.grid(row=3, column=0, padx=20, pady=15, sticky="w")

saved_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="Enter saved amount"
)
saved_entry.grid(row=3, column=1, padx=20, pady=15)

save_button = ctk.CTkButton(
    goal_frame,
    text="Save Goal",
    width=180
)

save_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=20
)

back_button = ctk.CTkButton(
    goal_frame,
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