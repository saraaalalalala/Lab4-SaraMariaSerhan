"""PyQt6 interface for the Task Manager."""

import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox,
    QHeaderView, QAbstractItemView,
)

from backend import TaskManager, PRIORITIES


class QtTaskApp(QWidget):
    def __init__(self, manager=None):
        super().__init__()
        self.manager = manager or TaskManager()
        self.setWindowTitle("Task Manager - PyQt")
        self.resize(520, 420)

        layout = QVBoxLayout(self)

        # Input row
        top = QHBoxLayout()
        top.addWidget(QLabel("Task:"))
        self.title_edit = QLineEdit()
        self.title_edit.returnPressed.connect(self.add_task)
        top.addWidget(self.title_edit)
        self.priority_box = QComboBox()
        self.priority_box.addItems(PRIORITIES)
        self.priority_box.setCurrentText("Medium")
        top.addWidget(self.priority_box)
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_task)
        top.addWidget(add_btn)
        layout.addLayout(top)

        # Task table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Title", "Priority", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        # Buttons
        bottom = QHBoxLayout()
        for text, slot in (("Toggle Done", self.toggle_done), ("Delete", self.delete_task),
                           ("Clear Completed", self.clear_completed), ("Reload", self.reload)):
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            bottom.addWidget(btn)
        bottom.addStretch()
        self.stats_label = QLabel()
        bottom.addWidget(self.stats_label)
        layout.addLayout(bottom)

        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        for task in self.manager.tasks:
            row = self.table.rowCount()
            self.table.insertRow(row)
            title_item = QTableWidgetItem(task.title)
            title_item.setData(256, task.id)  # Qt.ItemDataRole.UserRole
            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, QTableWidgetItem(task.priority))
            self.table.setItem(row, 2, QTableWidgetItem("Done" if task.done else "Pending"))
        s = self.manager.stats()
        self.stats_label.setText(f"{s['done']}/{s['total']} done")

    def selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "No selection", "Please select a task first.")
            return None
        return self.table.item(row, 0).data(256)

    def add_task(self):
        try:
            self.manager.add_task(self.title_edit.text(), self.priority_box.currentText())
        except ValueError as e:
            QMessageBox.warning(self, "Invalid task", str(e))
            return
        self.title_edit.clear()
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
        """Re-read the shared file (picks up changes made in the Tkinter app)."""
        self.manager.load()
        self.refresh()


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    window = QtTaskApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
