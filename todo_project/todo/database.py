"""This module provides the todo database functions"""
# todo/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from todo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

from todo import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the todo database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the todo database"""
    try:
        db_path.write_text("[]")  # empty todo list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # catch wrong json format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # catches file io problems
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]):
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError:  # catch file io problems
            return DBResponse(todo_list, DB_WRITE_ERROR)
