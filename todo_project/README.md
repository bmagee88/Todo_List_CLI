CLI Todo List
=============
+Completed Nov, 9th, 2022
-project instructions found at https://realpython.com/python-typer-cli/

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
|  -remove_all_done				|
|  -sort (-priority|-alpha|-done) (-asc|-desc)	|
|  -modify priority of index			|
|  -Have multiple todo lists one can load	|
|  -
|
