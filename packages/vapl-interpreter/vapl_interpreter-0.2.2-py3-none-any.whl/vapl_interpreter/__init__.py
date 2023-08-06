import vapl_interpreter.errors as errors


class COMPILER():
    def __init__(self, code):
        self.code = code
        self.memory = {}
        self.functionmemory = {}
        self.mailbox = ""
        self.inloop = 0
        self.compilecode(self.code)

    def compilecode(self, src: str, note=""):
        src = src.splitlines()
        for num in range(len(src)):
            self.compileline(src[num], num)

    def compileline(self, line, num):
        if line.startswith("!!"):  #comment
            print("", end="")
        if line == "%":
            if self.inloop == 0:
                errors.error("outofloop", line, num, "")
            self.mailbox = "break"
        if line == "&":
            if self.inloop == 0:
                errors.error("outofloop", line, num, "")
            self.mailbox = "continue"
        if self.mailbox != "":
            return

        if line.startswith("!P"):  #print
            if line[3:].startswith("(") and line[3:].endswith(")"):
                print(line[4:-1], end="")
            elif line[3:] == "@N":
                print()
            else:
                try:
                    if type(self.memory[line[3:]]) is list:
                        print("[" + ", ".join(self.memory[line[3:]]) + "]",
                              end="")
                except KeyError:
                    errors.error("name", line, num, line[3:])
                print(self.memory[line[3:]], end="")
        if line.startswith("!I"):  #input
            if line[3:].startswith("(") and line[3:].endswith(")"):
                tmp = input(line[4:-1])
                return tmp
            else:
                tmp = input(self.compileline(line[3:]))
                return tmp
        if line.startswith("!DV"):  #define variable
            if ":" not in line[4:]:
                errors.error("syntax", line, num, line)
            name = line[4:].split(":", 1)[0]
            try:
                var = self.compileline(line[4:].split(":", 1)[1], 1)
            except IndexError:
                errors.error("syntax", line, num, line)
            self.memory[name] = var
        if line.startswith("!F"):  #function
            if "}" not in line:
                errors.error("syntax", line, num, line)
            name = line[4:].split("}", 1)[0]
            function = line[4:].split("} ", 1)[1]
            self.functionmemory[name] = function
        if line.startswith("!E"):  #execute function
            name = line[3:]
            try:
                function = self.functionmemory[name]
            except KeyError:
                errors.error("function", line, num, name)
            self.compilecode("\n".join(function.split(";")))
        if line.startswith("!DC"):  #do calculation
            templine = line[4:]
            if templine.startswith("$V"):  #variables only
                listints = self.splitchars(["+", "-", "*", "/"], templine[3:])
                listops = self.findchars(["+", "-", "*", "/"], templine[3:])
                if listops == [] or self.allequal(listints, ""):
                    errors.error("nocalculation", line, num, templine[3:])
                if "" in listints:
                    errors.error("nocalculation", line, num, templine[3:])
                try:
                    curans = 0
                    curans += int(self.memory[listints[0]])
                    for i in range(0, len(listops)):
                        if listops[i] == "+":
                            curans += int(self.memory[listints[i + 1]])
                        if listops[i] == "-":
                            curans -= int(self.memory[listints[i + 1]])
                        if listops[i] == "*":
                            curans *= int(self.memory[listints[i + 1]])
                        if listops[i] == "/":
                            curans /= int(self.memory[listints[i + 1]])
                except KeyError:
                    errors.error("name", line, num, listints[0])
                except ValueError:
                    errors.error("nan", line, num, listints[0])
                return curans
            if templine.startswith("$N"):  #numbers only
                listints = self.splitchars(["+", "-", "*", "/"], templine[3:])
                listops = self.findchars(["+", "-", "*", "/"], templine[3:])
                if listops == [] or listints == []:
                    errors.error("nocalculation", line, num, templine[3:])
                if "" in listints:
                    errors.error("nocalculation", line, num, templine[3:])
                try:
                    curans = 0
                    curans += int(listints[0])
                    for i in range(0, len(listops)):
                        if listops[i] == "+":
                            curans += int(listints[i + 1])
                        if listops[i] == "-":
                            curans -= int(listints[i + 1])
                        if listops[i] == "*":
                            curans *= int(listints[i + 1])
                        if listops[i] == "/":
                            curans /= int(listints[i + 1])
                except ValueError:
                    errors.error("nan", line, num, listints[0])
                return curans
        if line.startswith("!R"):  #repeat (for loop)
            templine = line[3:]
            if templine.startswith(
                    "$N"):  #number (repeating factor is a number)
                templine = templine[4:]
                if "}" not in templine:
                    errors.error("syntax", templine, num, templine)
                try:
                    num_ = int(templine.split("}", 1)[0])
                except ValueError:
                    errors.error("nan", templine, num,
                                 templine.split("}", 1)[0])
            if templine.startswith("$V"):  #variable
                templine = templine[4:]
                if "}" not in templine:
                    errors.error("syntax", templine, num, templine)
                try:
                    num_ = int(self.memory[templine.split("}", 1)[0]])
                except ValueError:
                    errors.error("nan", templine, num,
                                 templine.split("}", 1)[0])
                except KeyError:
                    errors.error("name", templine, num,
                                 templine.split("}", 1)[0])
            todo = templine.split("} ", 1)[1]
            self.inloop = 1
            for i in range(num_):
                self.compilecode("\n".join(todo.split(";")))
                if self.mailbox != "":
                    if self.mailbox == "break":
                        self.mailbox = ""
                        break
                    self.mailbox = ""

        if line.startswith("?IF"):  #if
            templine = line[4:]
            if templine.startswith("$E"):  #equal
                templine = templine[4:]
                if "} " not in templine or "=" not in templine:
                    errors.error("syntax", templine, num, templine)
                statement = templine.split("} ")[0]
                code = templine.split("} ")[1]
                arg1 = statement.split("=", 1)[0]
                arg2 = statement.split("=", 1)[1]
                try:
                    if int(self.memory[arg1]) == int(self.memory[arg2]):
                        self.compilecode("\n".join(code.split(";")))
                except KeyError:
                    errors.error("name", line, num, arg1 + "' and/or '" + arg2)
                except ValueError:
                    errors.error("nan", line, num, arg1 + "' and/or '" + arg2)
            if templine.startswith("$N"):  #not equal
                templine = templine[4:]
                if "} " not in templine or "=" not in templine:
                    errors.error("syntax", templine, num, templine)
                statement = templine.split("} ")[0]
                code = templine.split("} ")[1]
                arg1 = statement.split("=", 1)[0]
                arg2 = statement.split("=", 1)[1]
                try:
                    if int(self.memory[arg1]) != int(self.memory[arg2]):
                        self.compilecode("\n".join(code.split(";")))
                except KeyError:
                    errors.error("name", line, num, arg1 + "' and/or '" + arg2)
                except ValueError:
                    errors.error("nan", line, num, arg1 + "' and/or '" + arg2)
            if templine.startswith("$GT"):  #greater than
                templine = templine[5:]
                if "} " not in templine or "=" not in templine:
                    errors.error("syntax", templine, num, templine)
                statement = templine.split("} ")[0]
                code = templine.split("} ")[1]
                arg1 = statement.split("=", 1)[0]
                arg2 = statement.split("=", 1)[1]
                try:
                    if int(self.memory[arg1]) > int(self.memory[arg2]):
                        self.compilecode("\n".join(code.split(";")))
                except KeyError:
                    errors.error("name", line, num, arg1 + "' and/or '" + arg2)
                except ValueError:
                    errors.error("nan", line, num, arg1 + "' and/or '" + arg2)
            if templine.startswith("$LT"):  #less than
                templine = templine[5:]
                if "} " not in templine or "=" not in templine:
                    errors.error("syntax", templine, num, templine)
                statement = templine.split("} ")[0]
                code = templine.split("} ")[1]
                arg1 = statement.split("=", 1)[0]
                arg2 = statement.split("=", 1)[1]
                try:
                    if int(self.memory[arg1]) < int(self.memory[arg2]):
                        self.compilecode("\n".join(code.split(";")))
                except KeyError:
                    errors.error("name", line, num, arg1 + "' and/or '" + arg2)
                except ValueError:
                    errors.error("nan", line, num, arg1 + "' and/or '" + arg2)
            if templine.startswith("$GE"):  #greater than or equal to
                templine = templine[5:]
                if "} " not in templine or "=" not in templine:
                    errors.error("syntax", templine, num, templine)
                statement = templine.split("} ")[0]
                code = templine.split("} ")[1]
                arg1 = statement.split("=", 1)[0]
                arg2 = statement.split("=", 1)[1]
                try:
                    if int(self.memory[arg1]) >= int(self.memory[arg2]):
                        self.compilecode("\n".join(code.split(";")))
                except KeyError:
                    errors.error("name", line, num, arg1 + "' and/or '" + arg2)
                except ValueError:
                    errors.error("nan", line, num, arg1 + "' and/or '" + arg2)
            if templine.startswith("$LE"):  #less than or equal to
                templine = templine[5:]
                if "} " not in templine or "=" not in templine:
                    errors.error("syntax", templine, num, templine)
                statement = templine.split("} ")[0]
                code = templine.split("} ")[1]
                arg1 = statement.split("=", 1)[0]
                arg2 = statement.split("=", 1)[1]
                try:
                    if int(self.memory[arg1]) <= int(self.memory[arg2]):
                        self.compilecode("\n".join(code.split(";")))
                except KeyError:
                    errors.error("name", line, num, arg1 + "' and/or '" + arg2)
                except ValueError:
                    errors.error("nan", line, num, arg1 + "' and/or '" + arg2)
        if line.startswith("!DL"):  #define list
            if ":" not in line[4:]:
                errors.error("syntax", line, num, line)
            lst = []
            for i in line[4:].split(":")[1].split(","):
                lst.append(i)
            self.memory[line[4:].split(":")[0]] = lst
        if line.startswith("!LO"):  #list operation
            if "}" not in templine or "]" not in templine:
                errors.error("syntax", line, num, line)
            templine = line[4:]
            varname = templine[1:].split("} ")[0]
            templine = templine.split("} ")[1]
            operation = templine[1:].split("] ")[0]
            todo = templine.split("] ")[1]
            try:
                lsttoworkon = self.memory[varname]
            except KeyError:
                errors.error("name", line, num, varname)
            if operation == "#A":  #add/append
                lsttoworkon.append(todo)
            if operation == "#R":  #remove
                lsttoworkon.remove(todo)
            if operation == "#G":  #get (index)
                try:
                    toreturn = lsttoworkon[int(todo)]
                except ValueError:
                    errors.error("nan", line, num, todo)
                return toreturn
            if operation == "#V":  #(get) variable (index)
                try:
                    toreturn = lsttoworkon[int(self.memory[todo])]
                except ValueError:
                    errors.error("nan", line, num, self.memory[todo])
                except KeyError:
                    errors.error("name", line, num, todo)
                return
            if operation == "#C":  #change (index)
                try:
                    if todo.startswith("$V"):  #variable
                        todo = todo[3:]
                        lsttoworkon[int(self.memory[todo.split(
                            ":")[0]])] = self.memory[todo.split(":")[1]]
                    if todo.startswith("$N"):  #no variable
                        todo = todo[3:]
                        lsttoworkon[int(
                            todo.split(":")[0])] = todo.split(":")[1]
                except:
                    errors.error("unknown", line, num, "")
            if operation == "#L":  #length
                return len(lsttoworkon)
        if line.startswith("!X"):  #exit
            exit()
        else:
            return line

    def splitchars(self, charlist: list, string: str):
        index = 0
        startindex = 0
        returnlist = []
        for i in string:
            if i in charlist:
                returnlist.append(string[startindex:index])
                startindex = index + 1
            index += 1
        returnlist.append(string[startindex:])
        return returnlist

    def findchars(self, charlist: list, string: str):
        returnlist = []
        for i in string:
            if i in charlist:
                returnlist.append(i)
        return returnlist

    def allequal(self, lst: list, string: str):
        for i in lst:
            if i != string:
                return False
        return True
