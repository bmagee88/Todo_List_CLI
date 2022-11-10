"""This module provides the to-do CLI"""
# todo/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from todo import ERRORS, __app_name__, __version__, config, database, todo, SUCCESS

from todo import __app_name__, __version__

app = typer.Typer()


@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            "--db-path",
            "-db",
            prompt="todo database location (hit enter to continue)?",
        ),
) -> None:
    """Initialize the todo database."""

    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"The todo database is {db_path}",
            fg=typer.colors.GREEN
        )


def get_todoer() -> todo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found.  Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return todo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "todo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def add(
        description: List[str] = typer.Argument(...),
        priority: int = typer.Option(
            2,
            "--priority",
            "-p",
            min=1,
            max=3),
) -> None:
    """Add a new todo with a description."""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding todo failed with {ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""todo: "{todo['description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )


@app.command(name="list")
def list_all() -> None:
    """List all todos."""
    todoer = get_todoer()
    todo_list, error = todoer.get_todo_list()

    if error:
        typer.secho(
            f'database read failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    if len(todo_list) == 0:
        typer.secho(
            "There are no tasks in the todo list.",
            fg=typer.colors.RED,
        )
        raise typer.Exit()

    typer.secho(
        "\ntodo list:\n",
        fg=typer.colors.BLUE,
        bold=True
    )

    columns = (
        "Id.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )

    headers = "".join(columns)

    typer.secho(
        headers,
        fg=typer.colors.BLUE,
        bold=True
    )

    typer.secho(
        "-" * len(headers),
        fg=typer.colors.BLUE
    )
    for id, todo in enumerate(todo_list, 1):
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho(
        "-" * len(headers) + "\n",
        fg=typer.colors.BLUE
    )


@app.command(name="complete")
def set_done(todo_id: int = typer.Argument(...)) -> None:
    """Completes a todo by setting it to done using its todo_id"""
    todoer = get_todoer()
    todo, error = todoer.set_done(todo_id)
    if error:
        typer.secho(
            f'Completing todo # {todo_id} failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""todo # {todo_id} "{todo["description"]}" completed!""",
            fg=typer.colors.GREEN,
        )


@app.command()
def remove(
        todo_id: int = typer.Argument(...),
        force: bool = typer.Option(
            False,
            "--force",
            "-f",
            help="Force deletion without confirmation",
        ),
) -> None:
    """Remove a todo using its todo id or index"""
    todoer = get_todoer()

    def _remove():
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'Removing todo # {todo_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""todo # {todo_id}: '{todo["description"]}' was removed""",
                fg=typer.colors.GREEN,
            )

    if force:
        _remove()
    else:
        todo_list = todoer.get_todo_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho(
                "Invalid TODO_ID",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete todo # {todo_id}: {todo['description']}?"
        )
        if delete:
            _remove()
        else:
            typer.echo("Operation canceled")


@app.command(name="clear")
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt="Delete all todos?",
        help="Force deletion without confirmation",
    ),
) -> None:
    """Removes all todos"""
    todoer = get_todoer()
    if force:
        error = todoer.remove_all().error
        if error:
            typer.secho(
                f'Removing todos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                "All todos were removed",
                fg=typer.colors.GREEN,
            )
    else:
        typer.echo("Operation Cancelled")


@app.command(name="rmdone")
def remove_all_done(
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        prompt="Delete all done todos?",
        help="Force deletion of all done todos without confirmation"
    ),
) -> None:
    """Removes all done todos"""
    todoer = get_todoer()
    if force:
        removed_done: List[CurrentTodo] = todoer.remove_all_done()
        if len(removed_done) <= 0:
            typer.secho(
                "List is empty; Nothing to remove",
                fg=typer.colors.GREEN,
            )
            return None
        elif len(removed_done) > 0:
            error = removed_done[(len(removed_done) - 1)].error
        else:
            error = 0
        if error:
            typer.secho(
                f'Removing todos failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                "All done todos were removed",
                fg=typer.colors.GREEN,
            )
    else:
        typer.echo("Operation Cancelled")


@app.command(name="chp")
def change_priority(
        todo_id: int = typer.Argument(
            ...
        ),
        new_priority: int = typer.Argument(
            ...
        ),
) -> None:
    """Changes priority of todo_id to the new priority"""
    todoer = get_todoer()
    error = todoer.change_priority(todo_id, new_priority).error
    if error:
        typer.secho(
            f'changing id # {todo_id} failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""priority of todo # {todo_id} changed to {new_priority}""",
            fg=typer.colors.GREEN,
        )


@app.command(name="chdb")
def change_database(db_path: str = typer.Argument(...)) -> None:
    error = config.change_database(db_path)
    if error:
        typer.secho(
            f'changing database to {db_path} failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""database changed to {db_path}""",
            fg=typer.colors.GREEN,
        )


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return



