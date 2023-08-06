import os
from termcolor import colored


def makeerrstring(line, num, var, typeoferror):
    if typeoferror == "variable":
        return "Traceback:\n\tLine " + str(
            num + 1
        ) + ":\n\t\t" + line + "\nVariableError: the variable '" + var + "' is not defined"
    if typeoferror == "nan":
        return "Traceback:\n\tLine " + str(
            num + 1
        ) + ":\n\t\t" + line + "\nNotANumberError: the value of '" + var + "' is not a number"
    if typeoferror == "function":
        return "Traceback:\n\tLine " + str(
            num + 1
        ) + ":\n\t\t" + line + "\nFunctionError: the function '" + var + "' is not defined"


def exitandraise(line, num, var, typeoferror):
    print(colored(makeerrstring(line, num, var, typeoferror), "red"))
    os._exit(1)


def error(name, line, num, var):
    if name == "name":
        exitandraise(line, num, var, "variable")
    if name == "function":
        exitandraise(line, num, var, "function")
    if name == "emptylisttodocalculations":
        print()
    if name == "nan":
        exitandraise(line, num, var, "nan")
