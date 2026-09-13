import customtkinter as ctk
import sys
from tkinter import messagebox
from datetime import datetime

from database.db_connection import connect_db
from ui.navigation import open_dashboard


# ==================================================
# USER ID
# ==================================================

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1


# ==================================================
# APPEARANCE
# ==================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==================================================
# COLORS
# ==================================================

BG_COLOR = "#0B1120"
CARD_COLOR = "#111827"
INPUT_COLOR = "#1F2937"

TEXT_COLOR = "#F9FAFB"
SECONDARY_TEXT = "#9CA3AF"

ACCENT_COLOR = "#2563EB"
ACCENT_HOVER = "#1D4ED8"

BORDER_COLOR = "#374151"

SUCCESS_COLOR = "#10B981"
WARNING_COLOR = "#F59E0B"


# ==================================================
# APPLICATION
# ==================================================

app = ctk.CTk()

app.title("Investment Goals - FinVest AI")

app.geometry("1100x750")

app.minsize(900, 650)

app.configure(
    fg_color=BG_COLOR
)


# ==================================================
# HEADER
# ==================================================

header_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header_frame.pack(
    fill="x",
    padx=40,
    pady=(25, 5)
)


title = ctk.CTkLabel(
    header_frame,
    text="Investment Goals",
    font=("Arial", 30, "bold"),
    text_color=TEXT_COLOR
)

title.pack(
    anchor="w"
)


subtitle = ctk.CTkLabel(
    header_frame,
    text="Set financial goals, track your progress, and stay focused on your future.",
    font=("Arial", 14),
    text_color=SECONDARY_TEXT
)

subtitle.pack(
    anchor="w",
    pady=(5, 0)
)


# ==================================================
# SCROLLABLE CONTENT
# ==================================================

scroll_frame = ctk.CTkScrollableFrame(
    app,
    fg_color="transparent"
)

scroll_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


# ==================================================
# GOAL FORM CARD
# ==================================================

goal_frame = ctk.CTkFrame(
    scroll_frame,
    fg_color=CARD_COLOR,
    corner_radius=18,
    border_width=1,
    border_color=BORDER_COLOR
)

goal_frame.pack(
    fill="x",
    padx=25,
    pady=10
)


goal_frame.grid_columnconfigure(
    0,
    weight=1
)

goal_frame.grid_columnconfigure(
    1,
    weight=2
)


# ==================================================
# FORM HEADER
# ==================================================

form_title = ctk.CTkLabel(
    goal_frame,
    text="Create New Goal",
    font=("Arial", 21, "bold"),
    text_color=TEXT_COLOR
)

form_title.grid(
    row=0,
    column=0,
    columnspan=2,
    padx=35,
    pady=(28, 5),
    sticky="w"
)


form_subtitle = ctk.CTkLabel(
    goal_frame,
    text="Define what you want to achieve and how much you need to save.",
    font=("Arial", 13),
    text_color=SECONDARY_TEXT
)

form_subtitle.grid(
    row=1,
    column=0,
    columnspan=2,
    padx=35,
    pady=(0, 22),
    sticky="w"
)


# ==================================================
# GOAL NAME
# ==================================================

goal_label = ctk.CTkLabel(
    goal_frame,
    text="Goal Name *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

goal_label.grid(
    row=2,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


goal_entry = ctk.CTkEntry(
    goal_frame,
    height=42,
    placeholder_text="e.g. Buy Laptop",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

goal_entry.grid(
    row=2,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# ==================================================
# TARGET AMOUNT
# ==================================================

target_label = ctk.CTkLabel(
    goal_frame,
    text="Target Amount *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

target_label.grid(
    row=3,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


target_entry = ctk.CTkEntry(
    goal_frame,
    height=42,
    placeholder_text="Enter target amount (₹)",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

target_entry.grid(
    row=3,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# ==================================================
# DEADLINE
# ==================================================

deadline_label = ctk.CTkLabel(
    goal_frame,
    text="Deadline *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

deadline_label.grid(
    row=4,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


deadline_entry = ctk.CTkEntry(
    goal_frame,
    height=42,
    placeholder_text="DD-MM-YYYY",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

deadline_entry.grid(
    row=4,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# ==================================================
# CURRENT SAVINGS
# ==================================================

saved_label = ctk.CTkLabel(
    goal_frame,
    text="Current Savings *",
    font=("Arial", 14, "bold"),
    text_color=TEXT_COLOR
)

saved_label.grid(
    row=5,
    column=0,
    padx=(35, 15),
    pady=8,
    sticky="w"
)


saved_entry = ctk.CTkEntry(
    goal_frame,
    height=42,
    placeholder_text="Enter amount already saved (₹)",
    fg_color=INPUT_COLOR,
    border_color=BORDER_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text_color=SECONDARY_TEXT
)

saved_entry.grid(
    row=5,
    column=1,
    padx=(15, 35),
    pady=8,
    sticky="ew"
)


# ==================================================
# SAVE GOAL FUNCTION
# ==================================================

def save_goal():

    goal_name = goal_entry.get().strip()

    target_amount = target_entry.get().strip()

    deadline = deadline_entry.get().strip()

    current_saved = saved_entry.get().strip()


    # ------------------------------------------------
    # VALIDATION
    # ------------------------------------------------

    if (
        goal_name == ""
        or target_amount == ""
        or deadline == ""
        or current_saved == ""
    ):

        messagebox.showerror(
            "Missing Information",
            "Please fill all required fields."
        )

        return


    # ------------------------------------------------
    # TARGET AMOUNT
    # ------------------------------------------------

    try:

        target_amount = float(target_amount)

        if target_amount <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Target amount must be greater than 0."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid target amount."
        )

        return


    # ------------------------------------------------
    # CURRENT SAVINGS
    # ------------------------------------------------

    try:

        current_saved = float(current_saved)

        if current_saved < 0:

            messagebox.showerror(
                "Invalid Savings",
                "Current saved amount cannot be negative."
            )

            return


        if current_saved > target_amount:

            messagebox.showerror(
                "Invalid Savings",
                "Current saved amount cannot be greater than target amount."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Invalid Savings",
            "Please enter a valid saved amount."
        )

        return


    # ------------------------------------------------
    # DEADLINE
    # ------------------------------------------------

    try:

        formatted_deadline = datetime.strptime(
            deadline,
            "%d-%m-%Y"
        ).strftime("%Y-%m-%d")

    except ValueError:

        messagebox.showerror(
            "Invalid Date",
            "Deadline must be in DD-MM-YYYY format."
        )

        return


    # ------------------------------------------------
    # DATABASE
    # ------------------------------------------------

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


        # ------------------------------------------------
        # INSERT GOAL
        # ------------------------------------------------

        query = """
        INSERT INTO investment_goals
        (
            user_id,
            goal_type,
            target_amount,
            target_date,
            current_savings,
            risk_level,
            goal_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """


        cursor.execute(
            query,
            (
                user_id,
                goal_name,
                target_amount,
                formatted_deadline,
                current_saved,
                "Medium",
                "Active"
            )
        )


        connection.commit()


        # ------------------------------------------------
        # SUCCESS
        # ------------------------------------------------

        messagebox.showinfo(
            "Goal Created",
            "Investment goal saved successfully!"
        )


        # ------------------------------------------------
        # CLEAR FORM
        # ------------------------------------------------

        goal_entry.delete(
            0,
            "end"
        )

        target_entry.delete(
            0,
            "end"
        )

        deadline_entry.delete(
            0,
            "end"
        )

        saved_entry.delete(
            0,
            "end"
        )


        # Refresh goals

        load_goals()


    except Exception as e:

        if connection:

            connection.rollback()


        print(
            "GOAL ERROR:",
            repr(e)
        )


        messagebox.showerror(
            "Database Error",
            str(e)
        )


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()


# ==================================================
# SAVE BUTTON
# ==================================================

save_button = ctk.CTkButton(
    goal_frame,
    text="Create Goal",
    width=220,
    height=45,
    corner_radius=10,
    font=("Arial", 15, "bold"),
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    command=save_goal
)

save_button.grid(
    row=6,
    column=0,
    columnspan=2,
    pady=(25, 30)
)


# ==================================================
# EXISTING GOALS SECTION
# ==================================================

section_header = ctk.CTkFrame(
    scroll_frame,
    fg_color="transparent"
)

section_header.pack(
    fill="x",
    padx=25,
    pady=(25, 5)
)


existing_title = ctk.CTkLabel(
    section_header,
    text="Your Investment Goals",
    font=("Arial", 21, "bold"),
    text_color=TEXT_COLOR
)

existing_title.pack(
    anchor="w"
)


existing_subtitle = ctk.CTkLabel(
    section_header,
    text="Track your current progress toward each financial goal.",
    font=("Arial", 13),
    text_color=SECONDARY_TEXT
)

existing_subtitle.pack(
    anchor="w",
    pady=(4, 0)
)


# ==================================================
# GOALS DISPLAY CONTAINER
# ==================================================

goals_display_frame = ctk.CTkFrame(
    scroll_frame,
    fg_color="transparent"
)

goals_display_frame.pack(
    fill="x",
    padx=25,
    pady=5
)


# ==================================================
# LOAD GOALS
# ==================================================

def load_goals():

    # Remove old goal cards

    for widget in goals_display_frame.winfo_children():

        widget.destroy()


    connection = None

    cursor = None


    try:

        connection = connect_db()


        if connection is None:

            return


        cursor = connection.cursor()


        query = """
        SELECT
            goal_type,
            target_amount,
            target_date,
            current_savings,
            goal_status
        FROM investment_goals
        WHERE user_id = %s
        ORDER BY goal_id DESC
        """


        cursor.execute(
            query,
            (user_id,)
        )


        goals = cursor.fetchall()


        # ------------------------------------------------
        # NO GOALS
        # ------------------------------------------------

        if len(goals) == 0:

            empty_card = ctk.CTkFrame(
                goals_display_frame,
                fg_color=CARD_COLOR,
                corner_radius=16,
                border_width=1,
                border_color=BORDER_COLOR
            )

            empty_card.pack(
                fill="x",
                pady=8
            )


            empty_label = ctk.CTkLabel(
                empty_card,
                text="No investment goals yet.\nCreate your first goal above!",
                font=("Arial", 14),
                text_color=SECONDARY_TEXT,
                justify="center"
            )

            empty_label.pack(
                pady=35
            )


            return


        # ------------------------------------------------
        # GOAL CARDS
        # ------------------------------------------------

        for goal in goals:

            goal_type = goal[0]

            target_amount = float(goal[1])

            target_date = goal[2]

            current_savings = float(goal[3])

            goal_status = goal[4]


            # ------------------------------------------------
            # PROGRESS
            # ------------------------------------------------

            if target_amount > 0:

                progress = (
                    current_savings / target_amount
                ) * 100

            else:

                progress = 0


            progress = min(
                progress,
                100
            )


            progress_value = progress / 100


            # ------------------------------------------------
            # GOAL CARD
            # ------------------------------------------------

            goal_card = ctk.CTkFrame(
                goals_display_frame,
                fg_color=CARD_COLOR,
                corner_radius=16,
                border_width=1,
                border_color=BORDER_COLOR
            )

            goal_card.pack(
                fill="x",
                pady=8
            )


            # ------------------------------------------------
            # TOP ROW
            # ------------------------------------------------

            top_frame = ctk.CTkFrame(
                goal_card,
                fg_color="transparent"
            )

            top_frame.pack(
                fill="x",
                padx=25,
                pady=(20, 5)
            )


            goal_name_label = ctk.CTkLabel(
                top_frame,
                text=f"🎯  {goal_type}",
                font=("Arial", 18, "bold"),
                text_color=TEXT_COLOR
            )

            goal_name_label.pack(
                side="left"
            )


            status_text = str(goal_status)


            if status_text.lower() == "active":

                status_color = SUCCESS_COLOR

            else:

                status_color = WARNING_COLOR


            status_label = ctk.CTkLabel(
                top_frame,
                text=status_text,
                font=("Arial", 12, "bold"),
                text_color=status_color
            )

            status_label.pack(
                side="right"
            )


            # ------------------------------------------------
            # PROGRESS TEXT
            # ------------------------------------------------

            progress_text_frame = ctk.CTkFrame(
                goal_card,
                fg_color="transparent"
            )

            progress_text_frame.pack(
                fill="x",
                padx=25,
                pady=(10, 5)
            )


            saved_text = ctk.CTkLabel(
                progress_text_frame,
                text=f"Saved: ₹{current_savings:,.2f}",
                font=("Arial", 13),
                text_color=TEXT_COLOR
            )

            saved_text.pack(
                side="left"
            )


            progress_label = ctk.CTkLabel(
                progress_text_frame,
                text=f"{progress:.1f}%",
                font=("Arial", 13, "bold"),
                text_color=ACCENT_COLOR
            )

            progress_label.pack(
                side="right"
            )


            # ------------------------------------------------
            # PROGRESS BAR
            # ------------------------------------------------

            progress_bar = ctk.CTkProgressBar(
                goal_card,
                height=10,
                corner_radius=5,
                fg_color=INPUT_COLOR,
                progress_color=ACCENT_COLOR
            )

            progress_bar.pack(
                fill="x",
                padx=25,
                pady=(5, 15)
            )


            progress_bar.set(
                progress_value
            )


            # ------------------------------------------------
            # INFORMATION FRAME
            # ------------------------------------------------

            info_frame = ctk.CTkFrame(
                goal_card,
                fg_color=INPUT_COLOR,
                corner_radius=10
            )

            info_frame.pack(
                fill="x",
                padx=25,
                pady=(0, 20)
            )


            # Target

            target_info = ctk.CTkLabel(
                info_frame,
                text=f"Target\n₹{target_amount:,.2f}",
                font=("Arial", 12),
                text_color=SECONDARY_TEXT,
                justify="left"
            )

            target_info.pack(
                side="left",
                padx=20,
                pady=12
            )


            # Remaining

            remaining = max(
                target_amount - current_savings,
                0
            )


            remaining_info = ctk.CTkLabel(
                info_frame,
                text=f"Remaining\n₹{remaining:,.2f}",
                font=("Arial", 12),
                text_color=SECONDARY_TEXT,
                justify="left"
            )

            remaining_info.pack(
                side="left",
                padx=20,
                pady=12
            )


            # Deadline

            deadline_info = ctk.CTkLabel(
                info_frame,
                text=f"Deadline\n{target_date}",
                font=("Arial", 12),
                text_color=SECONDARY_TEXT,
                justify="left"
            )

            deadline_info.pack(
                side="right",
                padx=20,
                pady=12
            )


    except Exception as e:

        print(
            "LOAD GOALS ERROR:",
            repr(e)
        )


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()


# ==================================================
# BACK TO DASHBOARD
# ==================================================

def go_back():

    app.destroy()

    open_dashboard(user_id)


back_button = ctk.CTkButton(
    scroll_frame,
    text="←  Back to Dashboard",
    width=220,
    height=45,
    corner_radius=10,
    font=("Arial", 14, "bold"),
    fg_color=INPUT_COLOR,
    hover_color=BORDER_COLOR,
    border_width=1,
    border_color=BORDER_COLOR,
    command=go_back
)

back_button.pack(
    pady=(20, 30)
)


# ==================================================
# KEYBOARD SHORTCUT
# ==================================================

app.bind(
    "<Return>",
    lambda event: save_goal()
)


# ==================================================
# LOAD EXISTING GOALS
# ==================================================

load_goals()


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    app.mainloop()