"""
To-Do List Application
----------------------
A command-line task manager that supports categories, due dates,
task completion, filtering, and persistent file storage.
"""

import os
from datetime import datetime


TASKS_FILE = "tasks.txt"
VALID_CATEGORIES = ["Personal", "Work", "Shopping", "Wishlist"]
DATE_FORMAT = "%d-%m-%Y"


class Task:
    """Represents a single task with a name, category, due date, and status."""

    def __init__(self, name: str, category: str, due_date: str, done: bool = False):
        self.name = name
        self.category = category
        self.due_date = due_date
        self.done = done

    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.done = True

    def to_file_line(self) -> str:
        """Serialize the task to a string for file storage."""
        status = "done" if self.done else "pending"
        return f"{self.name}|{self.category}|{self.due_date}|{status}"

    @classmethod
    def from_file_line(cls, line: str) -> "Task":
        """Deserialize a task from a file line.

        Args:
            line: A pipe-separated string from tasks.txt.

        Returns:
            A Task instance.

        Raises:
            ValueError: If the line format is invalid.
        """
        parts = line.strip().split("|")
        if len(parts) != 4:
            raise ValueError(f"Invalid task format: {line!r}")
        name, category, due_date, status = parts
        return cls(name, category, due_date, done=(status == "done"))

    def __str__(self) -> str:
        status = "✅ Done" if self.done else "⏳ Pending"
        return f"[{self.category}] {self.name} — Due: {self.due_date} | {status}"


class TaskManager:
    """Manages a list of tasks with load, save, add, remove, and filter operations."""

    def __init__(self, filepath: str = TASKS_FILE):
        self.filepath = filepath
        self.tasks: list[Task] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load tasks from the file. Skips malformed lines silently."""
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        self.tasks.append(Task.from_file_line(line))
                    except ValueError:
                        pass  # skip corrupted lines

    def save_tasks(self) -> None:
        """Write all tasks to the file."""
        with open(self.filepath, "w", encoding="utf-8") as f:
            for task in self.tasks:
                f.write(task.to_file_line() + "\n")

    def add_task(self, name: str, category: str, due_date: str) -> Task:
        """Create and store a new task.

        Args:
            name: Task description.
            category: One of the valid categories.
            due_date: Due date string in DD-MM-YYYY format.

        Returns:
            The newly created Task.
        """
        task = Task(name, category, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def remove_task(self, index: int) -> Task:
        """Remove a task by its 1-based index.

        Args:
            index: 1-based position of the task.

        Returns:
            The removed Task.

        Raises:
            IndexError: If the index is out of range.
        """
        if not (1 <= index <= len(self.tasks)):
            raise IndexError(f"No task at position {index}.")
        task = self.tasks.pop(index - 1)
        self.save_tasks()
        return task

    def mark_done(self, index: int) -> Task:
        """Mark a task as completed by its 1-based index.

        Args:
            index: 1-based position of the task.

        Returns:
            The updated Task.

        Raises:
            IndexError: If the index is out of range.
        """
        if not (1 <= index <= len(self.tasks)):
            raise IndexError(f"No task at position {index}.")
        self.tasks[index - 1].mark_done()
        self.save_tasks()
        return self.tasks[index - 1]

    def get_pending(self) -> list[Task]:
        """Return all tasks that are not yet done."""
        return [t for t in self.tasks if not t.done]

    def get_completed(self) -> list[Task]:
        """Return all completed tasks."""
        return [t for t in self.tasks if t.done]

    def filter_by_category(self, category: str) -> list[Task]:
        """Return tasks matching a given category (case-insensitive).

        Args:
            category: Category name to filter by.

        Returns:
            List of matching tasks.
        """
        return [t for t in self.tasks if t.category.lower() == category.lower()]


# ─── Input helpers ────────────────────────────────────────────────────────────

def get_task_index(prompt: str, max_index: int) -> int:
    """Prompt the user for a task number and validate it."""
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= max_index:
                return value
            print(f"  Please enter a number between 1 and {max_index}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_valid_category() -> str:
    """Prompt the user to pick a category from the valid list."""
    print("  Categories:", ", ".join(VALID_CATEGORIES))
    while True:
        choice = input("  Category: ").strip().title()
        if choice in VALID_CATEGORIES:
            return choice
        print(f"  Invalid category. Choose from: {', '.join(VALID_CATEGORIES)}")


def get_valid_date() -> str:
    """Prompt the user for a date in DD-MM-YYYY format."""
    while True:
        date_str = input("  Due date (DD-MM-YYYY): ").strip()
        try:
            datetime.strptime(date_str, DATE_FORMAT)
            return date_str
        except ValueError:
            print("  Invalid date. Use DD-MM-YYYY format (e.g. 30-06-2025).")


# ─── Menu actions ─────────────────────────────────────────────────────────────

def display_task_list(tasks: list[Task], title: str) -> None:
    """Print a numbered list of tasks under a section title."""
    print(f"\n── {title} ──")
    if not tasks:
        print("  (none)")
        return
    for i, task in enumerate(tasks, start=1):
        print(f"  {i}. {task}")


def handle_add(manager: TaskManager) -> None:
    name = input("  Task name: ").strip()
    if not name:
        print("  Task name cannot be empty.")
        return
    category = get_valid_category()
    due_date = get_valid_date()
    task = manager.add_task(name, category, due_date)
    print(f"  ✅ Added: {task}")


def handle_view(manager: TaskManager) -> None:
    display_task_list(manager.get_pending(), "Pending Tasks")


def handle_mark_done(manager: TaskManager) -> None:
    pending = manager.get_pending()
    display_task_list(pending, "Pending Tasks")
    if not pending:
        return
    idx = get_task_index("  Enter task number to mark as done: ", len(manager.tasks))
    try:
        task = manager.mark_done(idx)
        print(f"  ✅ Marked as done: {task.name}")
    except IndexError as e:
        print(f"  Error: {e}")


def handle_remove(manager: TaskManager) -> None:
    display_task_list(manager.tasks, "All Tasks")
    if not manager.tasks:
        return
    idx = get_task_index("  Enter task number to remove: ", len(manager.tasks))
    try:
        task = manager.remove_task(idx)
        print(f"  🗑️  Removed: {task.name}")
    except IndexError as e:
        print(f"  Error: {e}")


def handle_completed(manager: TaskManager) -> None:
    display_task_list(manager.get_completed(), "Completed Tasks")


def handle_filter(manager: TaskManager) -> None:
    category = get_valid_category()
    filtered = manager.filter_by_category(category)
    display_task_list(filtered, f"Tasks in '{category}'")


# ─── Main menu ────────────────────────────────────────────────────────────────

MENU = {
    "1": ("Add Task", handle_add),
    "2": ("View Pending Tasks", handle_view),
    "3": ("Mark Task as Done", handle_mark_done),
    "4": ("Remove Task", handle_remove),
    "5": ("Show Completed Tasks", handle_completed),
    "6": ("Filter by Category", handle_filter),
    "7": ("Exit", None),
}


def print_menu() -> None:
    print("\n" + "=" * 35)
    print("         TO-DO LIST APPLICATION")
    print("=" * 35)
    for key, (label, _) in MENU.items():
        print(f"  {key}. {label}")
    print("=" * 35)


def run() -> None:
    """Start the To-Do List application."""
    manager = TaskManager()
    print("\nWelcome to your To-Do List!")

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice not in MENU:
            print("  Invalid option. Please choose 1–7.")
            continue

        label, action = MENU[choice]

        if choice == "7":
            print("\nGoodbye! Your tasks have been saved. 👋")
            break

        print(f"\n── {label} ──")
        action(manager)


if __name__ == "__main__":
    run()
