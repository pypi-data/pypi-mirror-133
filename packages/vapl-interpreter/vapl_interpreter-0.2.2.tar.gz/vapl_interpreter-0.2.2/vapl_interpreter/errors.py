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
    if typeoferror == "syntax":
        return "Traceback:\n\tLine " + str(
            num + 1
        ) + ":\n\t\t" + line + "\nSyntaxError: invalid syntax: '" + var + "'"
    if typeoferror == "nocalculation":
        return "Traceback:\n\tLine " + str(
            num + 1
        ) + ":\n\t\t" + line + "\nNoCalculationError: cannot do calculation: '" + var + "'"
    if typeoferror == "outofloop":
        return "Traceback:\n\tLine " + str(
            num + 1
        ) + ":\n\t\t" + line + "\nOutOfLoopError: break or continue outside of loop"
    if typeoferror == "unknown":
        return "Traceback:\n\tLine " + str(
            num + 1
        ) + ":\n\t\t" + line + "\nUnknownError: this is a placeholder for errors I have not figured out yet"


def exitandraise(line, num, var, typeoferror):
    print(colored(makeerrstring(line, num, var, typeoferror), "red"))
    os._exit(1)


def error(name, line, num, var):
    if name == "name":
        exitandraise(line, num, var, "variable")
    if name == "function":
        exitandraise(line, num, var, "function")
    if name == "nocalculation":
        exitandraise(line, num, var, "nocalculation")
    if name == "nan":
        exitandraise(line, num, var, "nan")
    if name == "syntax":
        exitandraise(line, num, var, "syntax")
    if name == "outofloop":
        exitandraise(line, num, var, "outofloop")
    if name == "unknown":
        exitandraise(line, num, var, "unknown")
