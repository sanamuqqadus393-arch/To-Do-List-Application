# ✅ To-Do List Application

A command-line task manager built in Python. Supports task categories, due dates, completion tracking, category filtering, and persistent storage — all without any external dependencies.

## Features

- Add tasks with a name, category, and due date
- Four categories: Personal, Work, Shopping, Wishlist
- Mark tasks as done or remove them
- Filter tasks by category
- View all completed tasks separately
- Saves tasks to `tasks.txt` automatically on every change
- Input validation on all user inputs
- Fully unit-tested with pytest

## Demo

```
===================================
         TO-DO LIST APPLICATION
===================================
  1. Add Task
  2. View Pending Tasks
  3. Mark Task as Done
  4. Remove Task
  5. Show Completed Tasks
  6. Filter by Category
  7. Exit
===================================
Choose an option (1-7): 1

── Add Task ──
  Task name: Study for exam
  Categories: Personal, Work, Shopping, Wishlist
  Category: Work
  Due date (DD-MM-YYYY): 30-06-2025
  ✅ Added: [Work] Study for exam — Due: 30-06-2025 | ⏳ Pending
```

## Getting Started

### Prerequisites

- Python 3.10 or higher

### Installation

```bash
git clone https://github.com/sanamuqqadus393-arch/To-Do-List-Application.git
cd To-Do-List-Application
```

### Run the app

```bash
python todo_app.py
```

### Run the tests

```bash
pip install pytest
pytest test_todo_app.py -v
```

## Project Structure

```
To-Do-List-Application/
├── todo_app.py        # Main application (Task class + TaskManager + CLI)
├── test_todo_app.py   # 17 unit tests covering all core logic
├── requirements.txt   # Dependencies
├── .gitignore         # Excludes tasks.txt and Python artifacts
└── README.md
```

> **Note:** `tasks.txt` is auto-generated at runtime and is excluded from version control via `.gitignore`.

## Technologies Used

- Python 3.10+
- `os`, `datetime` (standard library)
- `pytest` (testing)

## What I Learned

- Object-oriented design with Python classes
- File I/O with error handling
- Separating data logic from UI logic
- Writing unit tests with `pytest` and fixtures

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

**Sana Muqqadus** — [LinkedIn](https://www.linkedin.com/in/sana-muqqadus-9b5a35348) · [Fiverr](https://www.fiverr.com/s/KeKgrpV)
