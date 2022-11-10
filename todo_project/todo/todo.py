"""This module provides the todo model-controller"""
# todo/todo.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todo import DB_READ_ERROR, ID_ERROR, SUCCESS, MAX_PRIORITY, MIN_PRIORITY, RANGE_ERROR
from todo.database import DatabaseHandler


class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int


class CurrentList(NamedTuple):
    todo_list: List[Dict[str, Any]]
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

    def get_todo_list(self) -> CurrentList:
        """Return the current todo list."""
        read = self._db_handler.read_todos()
        # should pass back the error code in case the JSON isn't formatted correctly.
        return CurrentList(read.todo_list, read.error)

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
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)

    def remove_all(self) -> CurrentTodo:
        """Removes all todos from the database"""
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)

    def remove_all_done(self) -> List[CurrentTodo]:
        """Removes all todos that are done from the database"""
        """TODO: Make more efficient. Bad thing about this implementation is that after each remove it rechecks the 
        incomplete tasks it passed the prior run.  Each remove is another read and write to the db."""
        complete = False
        removed_list: List[CurrentTodo] = []
        while not complete:
            read = self._db_handler.read_todos()
            if len(read.todo_list) == 0:
                return removed_list
            # what if list is empty?
            if read.error:
                return [CurrentTodo({}, read.error)]
            for i, todo in enumerate(read.todo_list):
                print(i, todo)
                if todo["done"]:
                    removed_list.append(self.remove((i + 1)))
                    print(removed_list)
                    if removed_list[(len(removed_list) - 1)].error != SUCCESS:
                        removed_list.pop((len(removed_list) - 1))  # removes the dummy
                        return removed_list
                    else:
                        break
                if i == (len(read.todo_list) - 1):  # checks if was last element
                    print("end of list")
                    complete = True
        return removed_list

    def change_priority(self, todo_id: int, new_priority: int) -> CurrentTodo:
        """Changes the priority of todo list"""
        if (new_priority < MIN_PRIORITY) or (new_priority > MAX_PRIORITY):
            return CurrentTodo({}, RANGE_ERROR)

        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["priority"] = new_priority
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)
