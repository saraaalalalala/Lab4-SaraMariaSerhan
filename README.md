# Lab 4 – Task Manager (Tkinter & PyQt)

**Student:** Sara Maria Serhan (solo project)
**Course:** Software Tools Lab – Fall 2026-2027, American University of Beirut

A small to-do / task manager with **two graphical interfaces**: one built with
**Tkinter** and one built with **PyQt6**. Both interfaces use the same backend
(`backend.py`) and save to the same data file (`tasks.json`), so a task added
in one interface shows up in the other.

## Project structure

```
Lab4-SaraMariaSerhan/
├── backend.py        # Shared logic: Task model + TaskManager (JSON storage)
├── tkinter_app.py    # Tkinter interface
├── pyqt_app.py       # PyQt6 interface
├── main.py           # Launcher to pick an interface
├── test_backend.py   # Unit tests (backend + both GUIs)
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9+ (Tkinter is included with Python)
- PyQt6

```bash
pip install -r requirements.txt
```

## How to run

```bash
python main.py            # launcher window with buttons for both interfaces
python main.py tkinter    # open the Tkinter interface directly
python main.py pyqt       # open the PyQt interface directly
```

You can also run `python tkinter_app.py` or `python pyqt_app.py`.

## How to use

Both interfaces have the same features:

| Action          | How                                                         |
|-----------------|-------------------------------------------------------------|
| Add a task      | Type a title, pick a priority (Low/Medium/High), click **Add** or press Enter |
| Mark done/undone| Select a task and click **Toggle Done**                     |
| Delete a task   | Select a task and click **Delete**                          |
| Clear completed | Click **Clear Completed**                                   |
| Sync            | Click **Reload** to load changes saved by the other interface |

### How Tkinter and PyQt are used together

- `tkinter_app.py` uses `ttk.Treeview`, `ttk.Entry`, `ttk.Combobox` and `messagebox`.
- `pyqt_app.py` uses `QTableWidget`, `QLineEdit`, `QComboBox` and `QMessageBox`.
- Neither interface stores data itself. Both call `TaskManager` in `backend.py`,
  which writes to `tasks.json`.
- The launcher (`main.py`) opens each interface in its own process, so both
  windows can be open at the same time. Add a task in one, then click **Reload**
  in the other to see it.

## Testing

```bash
python -m unittest -v
```

The tests check the backend (add, toggle, delete, clear, validation, shared file)
and build both GUIs on the same data file to check that they work together.

## Git workflow

This is a solo project, so following the lab instructions all work was committed
directly to `main`. No feature branches or pull requests were needed. The final
version is tagged `v1.0`.
