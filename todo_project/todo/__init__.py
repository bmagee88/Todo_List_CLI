"""Top-level package for To-do cli application"""
# to-do/__init__.py

__app_name__ = "todo"
__version__ = "0.1.0"
MAX_PRIORITY = 3
MIN_PRIORITY = 1

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    RANGE_ERROR,
    ID_ERROR,
) = range(8)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    JSON_ERROR: "JSON format",
    RANGE_ERROR: "number out of range",
    ID_ERROR: "to-do id error"
}

