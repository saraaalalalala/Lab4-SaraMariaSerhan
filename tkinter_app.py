"""Tkinter interface for the Task Manager."""

import tkinter as tk
from tkinter import ttk, messagebox

from backend import TaskManager, PRIORITIES


class TkTaskApp:
    def __init__(self, root, manager=None):
        self.root = root
        self.manager = manager or TaskManager()
        root.title("Task Manager - Tkinter")
        root.geometry("520x420")

        # Input row
        top = ttk.Frame(root, padding=10)
        top.pack(fill="x")
        ttk.Label(top, text="Task:").pack(side="left")
        self.title_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=self.title_var, width=28)
        entry.pack(side="left", padx=5)
        entry.bind("<Return>", lambda e: self.add_task())
        self.priority_var = tk.StringVar(value="Medium")
        ttk.Combobox(top, textvariable=self.priority_var, values=PRIORITIES,
                     state="readonly", width=8).pack(side="left", padx=5)
        ttk.Button(top, text="Add", command=self.add_task).pack(side="left")

        # Task list
        self.tree = ttk.Treeview(root, columns=("title", "priority", "status"),
                                 show="headings", height=12)
        self.tree.heading("title", text="Title")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("status", text="Status")
        self.tree.column("title", width=260)
        self.tree.column("priority", width=90, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10)

        # Buttons
        bottom = ttk.Frame(root, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Toggle Done", command=self.toggle_done).pack(side="left")
        ttk.Button(bottom, text="Delete", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(bottom, text="Clear Completed", command=self.clear_completed).pack(side="left")
        ttk.Button(bottom, text="Reload", command=self.reload).pack(side="left", padx=5)
        self.stats_label = ttk.Label(bottom, text="")
        self.stats_label.pack(side="right")

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for task in self.manager.tasks:
            status = "Done" if task.done else "Pending"
            self.tree.insert("", "end", iid=str(task.id),
                             values=(task.title, task.priority, status))
        s = self.manager.stats()
        self.stats_label.config(text=f"{s['done']}/{s['total']} done")

    def selected_id(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("No selection", "Please select a task first.")
            return None
        return int(selection[0])

    def add_task(self):
        try:
            self.manager.add_task(self.title_var.get(), self.priority_var.get())
        except ValueError as e:
            messagebox.showwarning("Invalid task", str(e))
            return
        self.title_var.set("")
        self.refresh()

    def toggle_done(self):
        task_id = self.selected_id()
        if task_id is not None:
            self.manager.toggle_done(task_id)
            self.refresh()

    def delete_task(self):
        task_id = self.selected_id()
        if task_id is not None:
            self.manager.delete_task(task_id)
            self.refresh()

    def clear_completed(self):
        self.manager.clear_completed()
        self.refresh()

    def reload(self):
        """Re-read the shared file (picks up changes made in the PyQt app)."""
        self.manager.load()
        self.refresh()


def main():
    root = tk.Tk()
    TkTaskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
