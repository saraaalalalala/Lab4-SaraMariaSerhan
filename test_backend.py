import os
import tempfile
import unittest

from backend import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)
        self.manager = TaskManager(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_task(self):
        task = self.manager.add_task("Study Git", "High")
        self.assertEqual(task.id, 1)
        self.assertEqual(self.manager.stats(), {"total": 1, "done": 0, "pending": 1})

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("   ")

    def test_invalid_priority_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("Task", "Urgent")

    def test_toggle_and_clear_completed(self):
        a = self.manager.add_task("A")
        self.manager.add_task("B")
        self.manager.toggle_done(a.id)
        self.assertEqual(self.manager.clear_completed(), 1)
        self.assertEqual([t.title for t in self.manager.tasks], ["B"])

    def test_delete_task(self):
        a = self.manager.add_task("A")
        self.manager.delete_task(a.id)
        self.assertEqual(self.manager.tasks, [])
        with self.assertRaises(KeyError):
            self.manager.delete_task(a.id)

    def test_data_shared_between_instances(self):
        # Simulates the Tkinter and PyQt apps reading the same file.
        self.manager.add_task("Shared task")
        other = TaskManager(self.path)
        self.assertEqual(other.tasks[0].title, "Shared task")


class GuiSmokeTests(unittest.TestCase):
    """Builds both GUIs on top of the same backend to check they integrate."""

    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_tkinter_ui(self):
        import tkinter as tk
        from tkinter_app import TkTaskApp
        try:
            root = tk.Tk()
        except tk.TclError:
            self.skipTest("No display available")
        root.withdraw()
        app = TkTaskApp(root, TaskManager(self.path))
        app.title_var.set("From Tkinter")
        app.add_task()
        self.assertEqual(len(app.tree.get_children()), 1)
        root.destroy()

    def test_pyqt_ui(self):
        try:
            from PyQt6.QtWidgets import QApplication
        except ImportError:
            self.skipTest("PyQt6 not installed")
        from pyqt_app import QtTaskApp
        app = QApplication.instance() or QApplication([])
        TaskManager(self.path).add_task("From Tkinter")
        window = QtTaskApp(TaskManager(self.path))
        self.assertEqual(window.table.rowCount(), 1)
        window.title_edit.setText("From PyQt")
        window.add_task()
        self.assertEqual(window.table.rowCount(), 2)
        window.close()


if __name__ == "__main__":
    unittest.main()
