import os as _os

def LevelPrint(level, msg=None):
    for i in range(level):
        print("    ",end="", flush=True)
    if(msg != None):
        print(msg)
        
def LevelInput(level, msg=""):
    LevelPrint(level)
    return input(msg)

def AnyKeyDialog(msg=""):
    if(msg == ""):
        input("Press enter to continue...")
    else:
        input(msg+ " - Press enter to continue...")

def ClearConsoleWindow():
    _os.system('cls' if _os.name=='nt' else 'clear')
    return

def Print_SelectFileDialog(printlevel=1):
    LevelPrint(printlevel, "-Enter File Path:")
    FilePath = LevelInput(printlevel, "-")
    if _os.path.exists(FilePath) == False:
        LevelPrint(printlevel+1, "-No such file found...")
        return None
    return FilePath
