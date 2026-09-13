import customtkinter as ctk
import sys
from tkinter import messagebox
from datetime import datetime

from database.db_connection import connect_db
from ui.navigation import open_dashboard


# ---------------- USER ID ----------------

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1


# ---------------- APPEARANCE ----------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- APPLICATION ----------------

app = ctk.CTk()
app.title("Investment Goals")
app.geometry("1000x700")


# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    app,
    text="Investment Goals",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# ---------------- FORM FRAME ----------------

goal_frame = ctk.CTkFrame(
    app,
    width=500,
    height=350
)

goal_frame.pack(pady=10)
goal_frame.pack_propagate(False)


# ---------------- GOAL NAME ----------------

goal_label = ctk.CTkLabel(
    goal_frame,
    text="Goal Name",
    font=("Arial", 16)
)

goal_label.grid(
    row=0,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)


goal_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="e.g. Buy Laptop"
)

goal_entry.grid(
    row=0,
    column=1,
    padx=20,
    pady=15
)


# ---------------- TARGET AMOUNT ----------------

target_label = ctk.CTkLabel(
    goal_frame,
    text="Target Amount",
    font=("Arial", 16)
)

target_label.grid(
    row=1,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)


target_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="Enter target amount"
)

target_entry.grid(
    row=1,
    column=1,
    padx=20,
    pady=15
)


# ---------------- DEADLINE ----------------

deadline_label = ctk.CTkLabel(
    goal_frame,
    text="Deadline",
    font=("Arial", 16)
)

deadline_label.grid(
    row=2,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)


deadline_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="DD-MM-YYYY"
)

deadline_entry.grid(
    row=2,
    column=1,
    padx=20,
    pady=15
)


# ---------------- CURRENT SAVINGS ----------------

saved_label = ctk.CTkLabel(
    goal_frame,
    text="Current Saved",
    font=("Arial", 16)
)

saved_label.grid(
    row=3,
    column=0,
    padx=20,
    pady=15,
    sticky="w"
)


saved_entry = ctk.CTkEntry(
    goal_frame,
    width=250,
    placeholder_text="Enter saved amount"
)

saved_entry.grid(
    row=3,
    column=1,
    padx=20,
    pady=15
)


# ---------------- SAVE GOAL FUNCTION ----------------

def save_goal():

    goal_name = goal_entry.get().strip()
    target_amount = target_entry.get().strip()
    deadline = deadline_entry.get().strip()
    current_saved = saved_entry.get().strip()


    # ---------------- VALIDATION ----------------

    if (
        goal_name == ""
        or target_amount == ""
        or deadline == ""
        or current_saved == ""
    ):
        messagebox.showerror(
            "Error",
            "Please fill all fields!"
        )
        return


    # ---------------- TARGET AMOUNT ----------------

    try:

        target_amount = float(target_amount)

        if target_amount <= 0:

            messagebox.showerror(
                "Error",
                "Target amount must be greater than 0."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter a valid target amount."
        )

        return


    # ---------------- CURRENT SAVINGS ----------------

    try:

        current_saved = float(current_saved)

        if current_saved < 0:

            messagebox.showerror(
                "Error",
                "Current saved amount cannot be negative."
            )

            return

        if current_saved > target_amount:

            messagebox.showerror(
                "Error",
                "Current saved amount cannot be greater than target amount."
            )

            return

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter a valid saved amount."
        )

        return


    # ---------------- DEADLINE ----------------

    try:

        formatted_deadline = datetime.strptime(
            deadline,
            "%d-%m-%Y"
        ).strftime("%Y-%m-%d")

    except ValueError:

        messagebox.showerror(
            "Error",
            "Deadline must be in DD-MM-YYYY format."
        )

        return


    # ---------------- DATABASE ----------------

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


        # ---------------- INSERT GOAL ----------------

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


        # ---------------- SUCCESS ----------------

        messagebox.showinfo(
            "Success",
            "Investment goal saved successfully!"
        )


        # ---------------- CLEAR FORM ----------------

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


        # Refresh existing goals
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
            repr(e)
        )


    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()


# ---------------- SAVE BUTTON ----------------

save_button = ctk.CTkButton(
    goal_frame,
    text="Save Goal",
    width=180,
    command=save_goal
)

save_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=20
)


# ---------------- EXISTING GOALS FRAME ----------------

goals_display_frame = ctk.CTkFrame(
    app,
    width=850,
    height=180
)

goals_display_frame.pack(
    pady=10
)

goals_display_frame.pack_propagate(False)


# ---------------- EXISTING GOALS TITLE ----------------

existing_title = ctk.CTkLabel(
    goals_display_frame,
    text="Your Goals",
    font=("Arial", 20, "bold")
)

existing_title.pack(
    pady=10
)


# ---------------- LOAD GOALS ----------------

def load_goals():

    # Remove old goal labels
    for widget in goals_display_frame.winfo_children():

        if widget != existing_title:

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


        if len(goals) == 0:

            no_goal_label = ctk.CTkLabel(
                goals_display_frame,
                text="No investment goals found.",
                font=("Arial", 14)
            )

            no_goal_label.pack(
                pady=20
            )

            return


        for goal in goals:

            goal_type = goal[0]
            target_amount = float(goal[1])
            target_date = goal[2]
            current_savings = float(goal[3])
            goal_status = goal[4]


            # ---------------- PROGRESS ----------------

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


            # ---------------- GOAL TEXT ----------------

            goal_text = (
                f"🎯 {goal_type}   |   "
                f"Target: ₹{target_amount:,.2f}   |   "
                f"Saved: ₹{current_savings:,.2f}   |   "
                f"Progress: {progress:.1f}%   |   "
                f"Deadline: {target_date}   |   "
                f"Status: {goal_status}"
            )


            goal_label_display = ctk.CTkLabel(
                goals_display_frame,
                text=goal_text,
                font=("Arial", 13)
            )

            goal_label_display.pack(
                pady=5
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


# ---------------- BACK BUTTON ----------------

def go_back():

    app.destroy()

    open_dashboard(user_id)


back_button = ctk.CTkButton(
    app,
    text="Back",
    width=180,
    command=go_back
)

back_button.pack(
    pady=10
)


# ---------------- LOAD EXISTING GOALS ----------------

load_goals()


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":

    app.mainloop()