import os as _os
import SimpleWorkspace as _sw

def LevelPrint(level, msg=None):
    for i in range(level):
        print("    ", end="", flush=True)
    if msg != None:
        print(msg)


def LevelInput(level, msg=""):
    LevelPrint(level)
    return input(msg)


def AnyKeyDialog(msg=""):
    if msg != "":
        msg += " - "
    msg += "Press enter to continue..."
    input(msg)


def ClearConsoleWindow():
    _os.system("cls" if _os.name == "nt" else "clear")
    return

def _stdin_tolist(inputString):
    """
        Takes an input string that is space delimetered and splits it into list of strings.
        strings can be escaped with quotes to allow space inside of values
        example of valid command:
            "value 1" value2 'value3'
    """
    spaceSplit = inputString.split(" ")
    valueEscapeChars = "\"'"
    values = []
    pathBuilder = ""
    for i in range(len(spaceSplit)):
        testPath = spaceSplit[i].strip("\n")
        if(pathBuilder == ""):
            if(testPath in ["", " "]):
                continue
        else:
            if(len(testPath) == 0):
                pathBuilder += " "
                continue
        
        if(len(testPath) == 1):
            if(testPath[0] in valueEscapeChars):
                if(pathBuilder == ""):
                    pathBuilder += testPath + " "
                    continue
        else:
            if(testPath[0] in valueEscapeChars and not testPath[-1] in valueEscapeChars):
                pathBuilder += testPath + " "

        if(pathBuilder != ""):
            if(testPath[-1] in valueEscapeChars):
                pathBuilder += testPath
                testPath = pathBuilder
                pathBuilder = ""
            elif(testPath[0] not in valueEscapeChars):
                pathBuilder += testPath + " "

        if(pathBuilder == ""):
            values.append(testPath.strip(valueEscapeChars))
    return values

def Print_SelectFileDialog(message="Enter File Path",printlevel=1) -> list[str]|None:
    LevelPrint(printlevel, f"-{message} (Separate multiple paths with space)")
    filepathString = LevelInput(printlevel, "-")
    filepaths = _stdin_tolist(filepathString)
    if(len(filepaths) == 0):
        return None
    return filepaths

