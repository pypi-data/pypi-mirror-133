# VAPL Interpreter
This is an interpreter for my language VAPL (it stands for "Very Annoying Programming Language").

# How to use this
- To use, first import vapl_interpreter (don't forget to install it!)

- Then, take your code (it can be a string, a file that you opened, etc.) and assign a variable "code" to it.

- Lastly, just write ```vapl_interpreter.COMPILER(code)```. If you imported vapl_interpreter as a different name, replace the "vapl_interpreter" part with that name.

- Have fun!
# Syntax
- To print a string, type ```!P (Your string here)```
- To print a blank line, type ```!P @N```
- To print a variable, just type ```!P variable_name_here```
- To get an input, type ```!I (Your string here)``` or ```!I your_variable_name_here```
- To define a variable, type ```!DV name:value```. The value can also be a variable, but you have to define a variable "zero" as 0 and then type ```!DC $V name+zero``` for the value.
- More coming soon!