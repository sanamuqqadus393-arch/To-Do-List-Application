"""
Unit tests for todo_app.py
Run with: pytest test_todo_app.py -v
"""

import os
import pytest
from todo_app import Task, TaskManager


# ─── Task tests ───────────────────────────────────────────────────────────────

class TestTask:
    def test_default_status_is_pending(self):
        task = Task("Buy groceries", "Shopping", "01-06-2025")
        assert task.done is False

    def test_mark_done(self):
        task = Task("Buy groceries", "Shopping", "01-06-2025")
        task.mark_done()
        assert task.done is True

    def test_to_file_line_pending(self):
        task = Task("Study Python", "Work", "15-06-2025")
        assert task.to_file_line() == "Study Python|Work|15-06-2025|pending"

    def test_to_file_line_done(self):
        task = Task("Study Python", "Work", "15-06-2025", done=True)
        assert task.to_file_line() == "Study Python|Work|15-06-2025|done"

    def test_from_file_line(self):
        task = Task.from_file_line("Read book|Personal|20-06-2025|pending")
        assert task.name == "Read book"
        assert task.category == "Personal"
        assert task.done is False

    def test_from_file_line_done(self):
        task = Task.from_file_line("Call doctor|Personal|10-06-2025|done")
        assert task.done is True

    def test_from_file_line_invalid_raises(self):
        with pytest.raises(ValueError):
            Task.from_file_line("bad line without pipes")


# ─── TaskManager tests ────────────────────────────────────────────────────────

@pytest.fixture
def tmp_manager(tmp_path):
    """A fresh TaskManager using a temporary file for each test."""
    filepath = str(tmp_path / "test_tasks.txt")
    return TaskManager(filepath)


class TestTaskManager:
    def test_add_task(self, tmp_manager):
        task = tmp_manager.add_task("Write tests", "Work", "01-07-2025")
        assert len(tmp_manager.tasks) == 1
        assert task.name == "Write tests"

    def test_add_task_saves_to_file(self, tmp_manager):
        tmp_manager.add_task("Check email", "Work", "05-07-2025")
        assert os.path.exists(tmp_manager.filepath)

    def test_remove_task(self, tmp_manager):
        tmp_manager.add_task("Task A", "Personal", "01-07-2025")
        tmp_manager.remove_task(1)
        assert len(tmp_manager.tasks) == 0

    def test_remove_task_invalid_index_raises(self, tmp_manager):
        with pytest.raises(IndexError):
            tmp_manager.remove_task(99)

    def test_mark_done(self, tmp_manager):
        tmp_manager.add_task("Fix bug", "Work", "01-07-2025")
        tmp_manager.mark_done(1)
        assert tmp_manager.tasks[0].done is True

    def test_get_pending(self, tmp_manager):
        tmp_manager.add_task("A", "Work", "01-07-2025")
        tmp_manager.add_task("B", "Work", "02-07-2025")
        tmp_manager.mark_done(1)
        assert len(tmp_manager.get_pending()) == 1

    def test_get_completed(self, tmp_manager):
        tmp_manager.add_task("A", "Work", "01-07-2025")
        tmp_manager.mark_done(1)
        assert len(tmp_manager.get_completed()) == 1

    def test_filter_by_category(self, tmp_manager):
        tmp_manager.add_task("Buy milk", "Shopping", "01-07-2025")
        tmp_manager.add_task("Fix bug", "Work", "02-07-2025")
        result = tmp_manager.filter_by_category("Shopping")
        assert len(result) == 1
        assert result[0].name == "Buy milk"

    def test_persistence(self, tmp_path):
        filepath = str(tmp_path / "tasks.txt")
        m1 = TaskManager(filepath)
        m1.add_task("Persist me", "Work", "01-08-2025")

        m2 = TaskManager(filepath)
        assert len(m2.tasks) == 1
        assert m2.tasks[0].name == "Persist me"
