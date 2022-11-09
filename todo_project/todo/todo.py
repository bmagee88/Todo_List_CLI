"""This module provides the todo model-controller"""
# todo/todo.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todo import DB_READ_ERROR, ID_ERROR
from todo.database import DatabaseHandler


class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:
        """Add a new todo to the database."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "description": description_text,
            "priority": priority,
            "done": False,
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return Currenttodo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return the current todo list."""
        read = self._db_handler.read_todos()
        return read.todo_list

    def set_done(self, todo_id: int) -> CurrentTodo:
        """Set a todo as done"""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["done"] = True
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove(self, todo_id: int) -> CurrentTodo:
        """Removes a todo from the database using its id or index"""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list.pop(todo_id -1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove_all(self) -> CurrentTodo:
        """Removes all todos from the database"""
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)
