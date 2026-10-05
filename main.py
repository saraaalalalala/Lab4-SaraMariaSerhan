"""Launcher: choose which interface to open.

Usage:
    python main.py           -> shows a small Tkinter launcher window
    python main.py tkinter   -> opens the Tkinter interface directly
    python main.py pyqt      -> opens the PyQt interface directly
"""

import subprocess
import sys
import os
import tkinter as tk
from tkinter import ttk

HERE = os.path.dirname(os.path.abspath(__file__))


def run_tkinter():
    import tkinter_app
    tkinter_app.main()


def run_pyqt():
    import pyqt_app
    pyqt_app.main()


def open_in_new_process(script):
    # Each GUI toolkit gets its own process so both windows can be open at once.
    subprocess.Popen([sys.executable, os.path.join(HERE, script)])


def launcher():
    root = tk.Tk()
    root.title("Task Manager Launcher")
    frame = ttk.Frame(root, padding=20)
    frame.pack()
    ttk.Label(frame, text="Choose an interface (both share the same tasks):").pack(pady=(0, 10))
    ttk.Button(frame, text="Open Tkinter UI", width=25,
               command=lambda: open_in_new_process("tkinter_app.py")).pack(pady=3)
    ttk.Button(frame, text="Open PyQt UI", width=25,
               command=lambda: open_in_new_process("pyqt_app.py")).pack(pady=3)
    root.mainloop()


if __name__ == "__main__":
    choice = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if choice == "tkinter":
        run_tkinter()
    elif choice == "pyqt":
        run_pyqt()
    else:
        launcher()
