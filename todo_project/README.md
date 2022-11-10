CLI Todo List
=============
+Completed Nov, 9th, 2022
+project instructions found at https://realpython.com/python-typer-cli/
+please note that I hand typed all of the instructions to ensure I learned something and didn't just copy the repo.  PLEASE, check what I have added as well.  Logs below.

Run the program type;
  python -m todo [COMMANDS]

Users can easily install all dependencies for the project with this command;
  python -m pip install -r requirements.txt

Things I've learned;
  -easily install dependencies
  -how to set up a cli project in python.
  -setting up a MVC (design pattern) project
  -using a JSON file to 
  -introduction to libraries;
    -typer, 
    -typing,
    -references to the project itself, 
    -configparser, 
    -JSON, 
    -Path, 
    -pytest
      -pytest.mark.parameterize
      -pytest.fixture
  -creating unit tests with pytest
  -python class argument types (surprise, not actually type checked its just for inline documentation) 
    ex. def add(self, <var_name>: <var_type> = <default_val>, <var_name>: <var_type>) -> <return_type>
  -return function annotation(->) 
  -<function_name>.__annotations__ (a dictionary)
  -Python classes and constructor and function syntax
  -custom error codes
  -try except
  -changing text colors with typer
  -@app.command()
  -typer.Option, typer.CliRunner, typer.Argument
  -json.dump
  -Path.write_text()
  -what to put in the __init__.py

_________________________________________________
|Features to include (not from the tutorial)	|
|_______________________________________________|________________________________
|Feature					|Completion Date		|
|+++++++++++++++++++++++++++++++++++++++++++++++|++++++++++++++++++++++++++++++++
|  -remove_all_done				|Nov 10, 2022
|  -sort (-priority|-alpha|-done) (-asc|-desc)	|
|  -modify priority of index			|Nov 10, 2022
|  -Have multiple todo lists one can load	|
|  -list files in a given folder (databases)	|
|  -Add more exhaustive tests			|
|  -get_todo_list return error code		|Nov 10, 2022
|  -change location of database storage		|Nov 10, 2022
|  -If changing location of db and it doesnt	|
|    exist, ask user if they would like to init	|---
|    at that location				|---
|  -change default db location to databases	|
|    folder in project folder			|---
|  -init path-to-db-folder db-name		|
|  -config file saves path-to-db-folder and	|
|    db_path					|---