import subprocess
import os


def open_login():
    subprocess.Popen(["python", os.path.join("ui", "login.py")])


def open_register():
    subprocess.Popen(["python", os.path.join("ui", "register.py")])


def open_dashboard():
    subprocess.Popen(["python", os.path.join("ui", "dashboard.py")])