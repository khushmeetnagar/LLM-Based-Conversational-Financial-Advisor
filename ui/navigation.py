import subprocess
import os
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)


def open_login():
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "ui.login"
        ],
        cwd=PROJECT_DIR
    )


def open_register():
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "ui.register"
        ],
        cwd=PROJECT_DIR
    )


def open_dashboard(user_id):
    print("Starting dashboard...")
    print("Python:", sys.executable)
    print("Project:", PROJECT_DIR)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ui.dashboard",
            str(user_id)
        ],
        cwd=PROJECT_DIR
    )

    print("Dashboard exited with:", result.returncode)
def open_add_expense(user_id):
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "ui.add_expense",
            str(user_id)
        ],
        cwd=PROJECT_DIR
    )


def open_view_expenses(user_id):
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "ui.view_expenses",
            str(user_id)
        ],
        cwd=PROJECT_DIR
    )
def open_analytics(user_id):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ui.analytics",
            str(user_id)
        ],
        cwd=PROJECT_DIR
    )

def open_goals(user_id):
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ui.goals",
            str(user_id)
        ],
        cwd=PROJECT_DIR
    )
def open_ai_advisor(user_id):
    subprocess.run(
        [sys.executable, "-m", "ui.ai_advisor", str(user_id)],
        cwd=PROJECT_DIR
    )